# Dashboard Operacional - Turma B 2026

Dashboard modernizada para acompanhamento de manutenção e operação com as seguintes melhorias:

## Novidades v2.0

### Visual
- Logotipos de Manutenção e Operação no cabeçalho (com links para Maximo)
- Ícone de relatório com link para AppSheet
- Rodapé enriquecido com contato e última atualização
- Paleta de cores harmonizada com os logos

### Funcionalidades
- **Gráfico velocímetro/rosca**: visualização percentual de horas mensais
- **Filtro de datas**: selecione períodos específicos no gráfico
- **Botão copiar OS**: copie lista de OS com formato ,=
- **Tooltips detalhados**: informações completas ao passar o mouse
- **Integração Google Drive**: atualização automática de dados

### Estrutura de Arquivos
```
dashboard_updated/
├── index.html          # Dashboard principal
├── logo_MNT.png        # Logo Manutenção
├── logo_OPE.png        # Logo Operação
├── logo_report.png     # Ícone Relatório
└── README.md           # Este arquivo
```

### Deploy no GitHub Pages

1. Crie um repositório no GitHub
2. Faça upload de todos os arquivos
3. Ative GitHub Pages nas configurações do repositório
4. Acesse: https://{seu-usuario}.github.io/{nome-repo}/

### Atualização de Dados

Os dados são carregados a partir de:
- Arquivos JSON locais (fallback)
- Google Drive (quando configurado)

## Desenvolvimento

Baseado em `maximo_B_26` com melhorias substanciais de UX e funcionalidades.

## Contato

Email: operacao@empresa.com.br
