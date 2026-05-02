#!/usr/bin/env python3
"""
convert.py — converte os .xls (HTML legado) da pasta uploads/ em JSONs por mês
em data/<YYYY-MM>.json + um manifesto data/index.json.

Estratégia:
- Lê TODOS os .xls em uploads/ (independente do nome).
- Cada .xls é um HTML com uma única <table>, com cabeçalho na 1ª linha:
  Mão de obra | Categoria | Nível | Ordem de Serviço | Tipo de Serviço |
  Tarefa | Data de Início | Horas Normais | Taxa | Aprovado
- Dedupa por (operador, OS, tipo, data, horas) — isso elimina sobreposição
  entre arquivos que cobrem o mesmo período.
- Particiona por mês e gera as agregações que a dashboard consome.

Idempotente: rodar 2x produz exatamente o mesmo resultado.
Compatível com Python 3.9+ e dependências mínimas (pandas + lxml ou bs4).
"""
from __future__ import annotations
import os, sys, json, glob, re
from datetime import datetime
from calendar import monthrange
from collections import defaultdict

import pandas as pd  # type: ignore

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(REPO_ROOT, "uploads")
DATA_DIR = os.path.join(REPO_ROOT, "data")

TIPOS_OPER = ["OPER"]
TIPOS_MANUT = ["CORR", "EM", "PRED", "PREV", "SERV", "MODI"]
ALL_TIPOS = TIPOS_OPER + TIPOS_MANUT

EXPECTED_COLS = [
    "operador", "categoria", "nivel", "os", "tipo",
    "tarefa", "data", "horas", "taxa", "aprovado",
]


# ───────────────────────── Parsing helpers ─────────────────────────
def hhmm_to_dec(v) -> float:
    """Converte '7:00' / '7:30' / '4.5' / NaN em decimal de horas."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return 0.0
    s = str(v).strip()
    if not s:
        return 0.0
    if ":" in s:
        try:
            h, m = s.split(":")
            return int(h) + int(m) / 60.0
        except Exception:
            return 0.0
    try:
        return float(s.replace(",", "."))
    except Exception:
        return 0.0


def parse_date(s):
    """Tenta dd/mm/yy, dd/mm/yyyy, yyyy-mm-dd. Retorna datetime ou None."""
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    s = str(s).strip()
    if not s:
        return None
    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def read_xls_html(path: str) -> pd.DataFrame:
    """Lê um arquivo .xls que na verdade é HTML (export do tipo SAP/sistemas
    de manutenção). Retorna DataFrame com colunas normalizadas."""
    tables = pd.read_html(path)
    if not tables:
        return pd.DataFrame(columns=EXPECTED_COLS)
    df = tables[0]
    # A primeira linha é o cabeçalho com nomes em PT-BR; descartamos.
    if len(df) >= 1 and len(df.columns) >= 10:
        df = df.iloc[1:].copy()
    df = df.iloc[:, :10]  # garante 10 colunas
    df.columns = EXPECTED_COLS
    return df


# ───────────────────────── Aggregation ─────────────────────────
def build_aggregates(df: pd.DataFrame) -> dict:
    """Recebe DataFrame consolidado e devolve a estrutura que a dashboard usa."""
    df = df.copy()
    df["horas_dec"] = df["horas"].apply(hhmm_to_dec)
    df["data_dt"] = df["data"].apply(parse_date)
    df = df.dropna(subset=["data_dt"]).reset_index(drop=True)

    # Dedup global
    df = df.drop_duplicates(
        subset=["operador", "os", "tipo", "data", "horas"]
    ).reset_index(drop=True)

    df["ym"] = df["data_dt"].dt.strftime("%Y-%m")
    df["dia"] = df["data_dt"].dt.day

    operadores = sorted(df["operador"].dropna().unique().tolist())
    meses = sorted(df["ym"].unique().tolist())

    out = {
        "operadores": operadores,
        "meses": meses,
        "tipos_oper": TIPOS_OPER,
        "tipos_manut": TIPOS_MANUT,
        "dados": {},
        "_generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    targets = meses + ["ANUAL"]
    for ym in targets:
        dfm = df if ym == "ANUAL" else df[df["ym"] == ym]
        bucket = {}
        for op in operadores + ["_ALL"]:
            dfo = dfm if op == "_ALL" else dfm[dfm["operador"] == op]

            tipos_h = {t: round(float(dfo[dfo["tipo"] == t]["horas_dec"].sum()), 2)
                       for t in ALL_TIPOS}
            h_oper = round(float(dfo[dfo["tipo"].isin(TIPOS_OPER)]["horas_dec"].sum()), 2)
            h_manut = round(float(dfo[dfo["tipo"].isin(TIPOS_MANUT)]["horas_dec"].sum()), 2)

            # por dia
            if ym == "ANUAL":
                key_series = dfo["data_dt"].dt.strftime("%m-%d")
            else:
                key_series = dfo["dia"].astype(int).astype(str).str.zfill(2)
            dfo = dfo.assign(_key=key_series)
            por_dia = []
            for k in sorted(dfo["_key"].unique().tolist()):
                sub = dfo[dfo["_key"] == k]
                entry = {"dia": k}
                for t in ALL_TIPOS:
                    entry[t] = round(float(sub[sub["tipo"] == t]["horas_dec"].sum()), 2)
                entry["oper_total"] = round(sum(entry[t] for t in TIPOS_OPER), 2)
                entry["manut_total"] = round(sum(entry[t] for t in TIPOS_MANUT), 2)
                por_dia.append(entry)

            os_por_tipo = {t: int(dfo[dfo["tipo"] == t]["os"].nunique())
                           for t in ALL_TIPOS}
            total_os = int(dfo["os"].nunique())
            dias_trab = int(dfo["data_dt"].dt.date.nunique())

            bucket[op] = {
                "horas_oper": h_oper,
                "horas_manut": h_manut,
                "horas_total": round(h_oper + h_manut, 2),
                "tipos": tipos_h,
                "por_dia": por_dia,
                "os_por_tipo": os_por_tipo,
                "total_os": total_os,
                "dias_trabalhados": dias_trab,
            }

        # _meta com calendário
        if ym == "ANUAL":
            uteis = corridos = 0
            for ymm in meses:
                a, m = map(int, ymm.split("-"))
                last = monthrange(a, m)[1]
                uteis += sum(1 for d in range(1, last + 1)
                             if datetime(a, m, d).weekday() < 5)
                corridos += last
        else:
            a, m = map(int, ym.split("-"))
            last = monthrange(a, m)[1]
            uteis = sum(1 for d in range(1, last + 1)
                        if datetime(a, m, d).weekday() < 5)
            corridos = last
        bucket["_meta"] = {"dias_uteis_calendario": uteis, "dias_corridos": corridos}

        out["dados"][ym] = bucket

    return out


def split_by_month(big: dict) -> dict:
    """Divide o agregado consolidado em arquivos por mês.
    Cada arquivo de mês é um JSON contendo apenas o `dados[ym]` daquele mês.
    O ANUAL fica embutido no manifesto para ser recalculado client-side."""
    per_month = {}
    for ym in big["meses"]:
        per_month[ym] = {
            "ym": ym,
            "operadores": big["operadores"],
            "tipos_oper": big["tipos_oper"],
            "tipos_manut": big["tipos_manut"],
            "dados": big["dados"][ym],
            "_generated_at": big["_generated_at"],
        }
    return per_month


def write_outputs(big: dict, per_month: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    # Arquivo por mês
    for ym, payload in per_month.items():
        with open(os.path.join(DATA_DIR, f"{ym}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    # Manifesto: lista os meses + dados ANUAL pré-calculados (assim o frontend
    # não precisa baixar tudo só pra montar a aba Anual).
    manifest = {
        "operadores": big["operadores"],
        "meses": big["meses"],
        "tipos_oper": big["tipos_oper"],
        "tipos_manut": big["tipos_manut"],
        "anual": big["dados"]["ANUAL"],
        "_generated_at": big["_generated_at"],
    }
    with open(os.path.join(DATA_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, separators=(",", ":"))


# ───────────────────────── Main ─────────────────────────
def main():
    xls_files = sorted(glob.glob(os.path.join(UPLOADS_DIR, "*.xls"))
                       + glob.glob(os.path.join(UPLOADS_DIR, "*.XLS"))
                       + glob.glob(os.path.join(UPLOADS_DIR, "*.xlsx"))
                       + glob.glob(os.path.join(UPLOADS_DIR, "*.html"))
                       + glob.glob(os.path.join(UPLOADS_DIR, "*.htm")))
    if not xls_files:
        print(f"⚠ Nenhum arquivo encontrado em {UPLOADS_DIR}/")
        # Mesmo sem dados, garante que data/ exista com um manifesto vazio
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, "index.json"), "w", encoding="utf-8") as f:
            json.dump({
                "operadores": [], "meses": [], "tipos_oper": TIPOS_OPER,
                "tipos_manut": TIPOS_MANUT, "anual": None,
                "_generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            }, f, ensure_ascii=False)
        return 0

    print(f"📂 Lendo {len(xls_files)} arquivo(s) de uploads/:")
    dfs = []
    for f in xls_files:
        try:
            df = read_xls_html(f)
            print(f"   • {os.path.basename(f)} → {len(df)} linhas")
            dfs.append(df)
        except Exception as e:
            print(f"   ✗ {os.path.basename(f)} falhou: {e}", file=sys.stderr)

    if not dfs:
        print("✗ Nenhum arquivo pôde ser lido.", file=sys.stderr)
        return 1

    big_df = pd.concat(dfs, ignore_index=True)
    print(f"\n🔗 Consolidado: {len(big_df)} linhas (antes da dedup)")

    aggregated = build_aggregates(big_df)
    print(f"📊 Após dedup e agregação: meses = {aggregated['meses']}, "
          f"operadores = {len(aggregated['operadores'])}")

    per_month = split_by_month(aggregated)
    write_outputs(aggregated, per_month)

    print(f"\n✓ Arquivos gerados em {DATA_DIR}/")
    print(f"   • index.json (manifesto)")
    for ym in aggregated["meses"]:
        b = aggregated["dados"][ym]["_ALL"]
        print(f"   • {ym}.json — {b['horas_oper']:.0f}h OPER + "
              f"{b['horas_manut']:.0f}h manut. · {b['total_os']} OS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
