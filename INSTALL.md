# Guia de Instalação - Dashboard Turma B

## Instalação Rápida

### 1. GitHub Pages (Recomendado)

1. Crie um repositório no GitHub
   - Acesse https://github.com/new
   - Nome sugerido: `dashboard-turma-b`
   - Visibilidade: Private (recomendado para dados internos)

2. Faça upload dos arquivos
   ```bash
   # Clone o repositório vazio
   git clone https://github.com/SEU-USUARIO/dashboard-turma-b.git
   cd dashboard-turma-b
   
   # Copie todos os arquivos da dashboard
   # (index.html, logo_*.png, README.md, etc.)
   
   # Adicione e envie
   git add .
   git commit -m "Dashboard inicial"
   git push origin main
   ```

3. Ative o GitHub Pages
   - Vá em Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Salve

4. Acesse sua dashboard
   - URL: `https://SEU-USUARIO.github.io/dashboard-turma-b/`

### 2. Servidor Web Local

Se preferir hospedar em servidor interno:

```bash
# Com Python
python3 -m http.server 8000

# Com Node.js (http-server)
npx http-server -p 8000

# Com PHP
php -S localhost:8000
```

Acesse: `http://localhost:8000`

## Configuração de Dados

### Estrutura de Dados

Os dados são armazenados em JSON embutido no `index.html`.

Para atualizar:

1. Localize a tag `<script id="data-blob" type="application/json">`
2. Atualize o JSON conforme a estrutura existente
3. Salve e faça commit

### Integração com Google Drive (Opcional)

Para integração automática:

1. Configure as permissões no Google Drive
2. Atualize as URLs no código JavaScript
3. Implemente autenticação OAuth2

**Nota**: A integração com Google Drive requer configuração adicional no console do Google Cloud.

## Personalização

### Alterar Cores

Edite as variáveis CSS em `:root`:

```css
:root {
  --op: #22d3ee;        /* Cor principal operação */
  --maint: #f59e0b;     /* Cor principal manutenção */
  /* ... outras variáveis ... */
}
```

### Alterar Título

No `<head>`:
```html
<title>Seu Título Aqui</title>
```

No cabeçalho:
```html
<div class="t">Seu Título</div>
<div class="s">Subtítulo</div>
```

### Atualizar Links

Edite os atributos `href` dos logos no cabeçalho.

## Solução de Problemas

### Dashboard não carrega

- Verifique o console do navegador (F12)
- Confirme que todos os arquivos estão no mesmo diretório
- Verifique se o JSON está válido

### Imagens não aparecem

- Confirme que os arquivos de imagem estão no mesmo diretório
- Verifique os nomes dos arquivos (case-sensitive no Linux)

### Dados não atualizam

- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique a data de modificação do arquivo

## Suporte

Para questões ou sugestões:
- Email: operacao@empresa.com.br
- Ou abra uma issue no repositório do GitHub

## Segurança

**Importante**: 
- Não commite dados sensíveis no repositório público
- Use repositório privado para dados internos
- Configure .gitignore adequadamente
