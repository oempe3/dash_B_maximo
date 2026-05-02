# Painel Operacional — Dashboard de Manutenção & Operação

Dashboard estática com atualização automática para GitHub Pages.

## Estrutura do repositório

```
├── index.html                    ← Dashboard (abra no navegador)
├── convert.py                    ← Script de conversão XLS → JSON
├── data/                         ← JSONs gerados (NÃO editar manualmente)
│   ├── index.json                ← Manifesto (lista de meses + dados anuais)
│   ├── 2026-01.json
│   ├── 2026-02.json
│   ├── 2026-03.json
│   └── 2026-04.json
├── uploads/                      ← COLOQUE SEUS ARQUIVOS .xls AQUI
│   ├── 76890600.xls
│   ├── 79687038.xls
│   ├── 79714178.xls
│   └── 79740615.xls
└── .github/workflows/
    └── convert.yml               ← GitHub Action (conversão automática)
```

## Como publicar

1. Crie um repositório no GitHub (pode ser público ou privado com Pages).
2. Faça upload de **toda esta pasta** para a raiz do repositório.
3. Vá em **Settings → Pages → Source**: selecione branch `main`, pasta `/ (root)`.
4. Pronto! A dashboard ficará em `https://<usuario>.github.io/<repo>/`.

## Como adicionar meses novos

1. Exporte o `.xls` do mês novo do sistema.
2. Coloque o arquivo na pasta `uploads/` do repositório.
3. Faça `commit` e `push`.
4. A **GitHub Action** roda automaticamente: lê todos os `.xls`, gera os JSONs em `data/` e faz commit.
5. Na dashboard, clique no botão **"Atualizar"** para buscar os novos meses (ou recarregue a página).

> **Nota**: O nome do arquivo `.xls` não importa — o script lê todos os `.xls` da pasta `uploads/` e deduplica automaticamente.

## Funcionalidades

- Botões por mês + visão **Anual** consolidada
- Filtro por operador
- 6 KPIs: horas OPER, horas manutenção, dias trabalhados, horas totais (×8h), horas úteis (×7h), total de OS
- Gráfico de barras dia a dia (Operação vs Manutenção)
- Tooltip com detalhamento dos 6 tipos de manutenção (cores diferenciadas)
- Lista de OS executadas por tipo
- Botão **Atualizar** que busca novos meses no repositório sem recarregar a página
- Dados embutidos no HTML como fallback offline
