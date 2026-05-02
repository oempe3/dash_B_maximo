# Especificação para Evolução da Dashboard de Manutenção e Operação

## Referência de implementações existentes

O repositório `maximo_B_26` contém uma dashboard em HTML/CSS/JS com dados incorporados em JSON. A página atual apresenta KPIs, gráfico de barras de **Horas por dia**, listagem de **Ordens de Serviço por tipo** e um **Detalhamento das horas de manutenção**. As principais seções e elementos visíveis são:

- **Cabeçalho (“appbar”)** com título e subtítulo (“Painel Operacional”, “Operação · Manutenção · Ordens de Serviço”). Também traz um botão *Atualizar*, que busca novos meses no repositório e atualiza a página, e um seletor para filtragem por operador.  
- **Seletor de período** (tabs) com meses e visão anual.  
- **KPIs**: horas operacionais, horas de manutenção, dias trabalhados, horas totais (× 8 h), horas úteis (× 7 h) e total de ordens de serviço.  
- **Gráfico de barras** com horas de operação versus horas de manutenção por dia, com tooltip para detalhes.  
- **Lista de OS por tipo** exibindo a quantidade de ordens de serviço no período.  
- **Breakdown de horas de manutenção** com horas totais para cada tipo de manutenção.  
- **Rodapé** simples informando que a dashboard é estática e mostrando a quantidade de meses e operadores.

Esses elementos podem ser verificados no conteúdo textual da página. Por exemplo, no cabeçalho e nos KPIs observa‑se o total de OS, as horas operacionais e de manutenção e o mês selecionado【87211117776069†L10-L16】, bem como os indicadores de horas de manutenção e dias trabalhados【87211117776069†L24-L34】.  Na seção “Horas por dia”, a página mostra a descrição “Operação vs. Manutenção · passe o mouse sobre as barras para detalhamento”【87211117776069†L50-L58】, e na lista de OS por tipo são exibidos os totais de cada classificação【87211117776069†L96-L119】.  O detalhamento de horas por tipo de manutenção é apresentado com valores como “26h Corretiva” ou “18h Preditiva”【87211117776069†L132-L150】.

## Objetivos de melhoria

1. **Atualização visual e integração de marcas** – O novo modelo (maximo_2026) possui uma estética mais atual, voltada para a “Turma B”. É preciso incorporar nessa base:  
   - **Título personalizável** conforme a unidade/turno.  
   - **Links com logotipos**: utilizar os arquivos `logo_MNT.png` e `logo_OPE.png` no cabeçalho como links clicáveis para as áreas de Manutenção e Operação ou outro destino definido. Deverão estar alinhados e dimensionados de forma proporcional ao cabeçalho; idealmente com `width` inferior a 40 px e `height` calculado preservando o aspecto, com `alt` descritivo.  
   - **Rodapé enriquecido**: inserir informações como e‑mail de contato, data/hora da última atualização, link para a origem dos dados e eventuais avisos de confidencialidade. O rodapé deve permanecer responsivo e com texto legível em tela pequena.  
   - Manter o efeito de desfoque do cabeçalho (“backdrop‑filter”) para dar contraste com o corpo da página.

2. **Melhorias nos quadros de horas** – Para tornar a análise mensal mais intuitiva, devem ser incluídos os seguintes elementos:

   - **Quadro “Horas no mês”**: exibir o total de horas lançadas no mês somando horas operacionais (OPER) e horas de manutenção (“Restante”), com destaque visual. Esse valor ficará sob os KPIs, junto da seleção de mês e operador, permitindo comparar rapidamente com as horas totais nominalmente previstas.
   - **Gráfico tipo velocímetro / rosca**:  
     - O objetivo é representar o cumprimento de horas mensais em relação à carga teórica de **8 h × dias trabalhados**.  
     - Implementar utilizando um componente de gauge ou donut chart (por exemplo, com D3.js, Chart.js ou outra biblioteca) com range de 0 a 100 % (0 % = 0 h, 100 % = 8 h × dias).  
     - Dividir o preenchimento em duas cores: **OPER** e **Restante** (soma de todos os tipos de manutenção). Assim, a área de OPER aparece em azul (seguindo a variável CSS `--op`) e a área de RESTANTE em amarelo (`--maint`).  
     - Adicionar uma **seta/ponteiro** indicando a posição das horas lançadas no mês (OPER + Restante).  
     - Inserir **marcador na escala** para as **horas úteis (7 h × dias)**, permitindo comparar com a meta nominal.  
     - Fornecer **tooltips** e rótulos ao passar o mouse: o tooltip deve indicar o valor numérico de horas em cada segmento (ex.: “OPER: 223 h – 60 %, Restante: 223 h – 60 %”, “Total: 446 h de 288 h previstas”).  
     - Este gráfico substitui ou complementa o KPI de horas totais, oferecendo visão percentual intuitiva.

3. **Aprimoramento de “Ordens de serviço por tipo” e “Detalhamento das horas de manutenção”**:

   - **Botão Copiar**: incluir ao lado de cada linha (tipo de manutenção ou total) um ícone de copiar. Ao clicar, deve copiar para a área de transferência a lista de números de ordens de serviço relativas àquele filtro. Os números devem estar separados pela sequência `",="` para atender ao formato requisitado (ex.: `321321,=324321`). Após copiar, apresentar uma tooltip ou toast “Informação copiada” confirmando a ação.  
   - **Tooltip de detalhes**: nos painéis de OS por tipo e no painel geral, implementar um tooltip de sobreposição ao passar o mouse que contenha: número da OS, descrição, local e status (data de atualização). Esses dados deverão ser obtidos do dataset (xls/JSON) e agrupados conforme o tipo selecionado.  
   - **Separação visual clara** entre cada linha e ícone de copiar, com foco acessível para teclado.

4. **Integração com dados externos (Google Drive)**:

   - A dashboard atual utiliza dados incorporados em JSON e pode ser atualizada via GitHub. Para atender às novas necessidades, implementar rotina de busca automática em pastas do Google Drive:  
     - **Horas lançadas** – pasta: `https://drive.google.com/drive/folders/1ckqvL24ShJQxY8ZK1Aiw3BDkiKPrrXNE`.  
     - **Status de OS** – pasta: `https://drive.google.com/drive/u/1/folders/1H_oZ5PybIUoEZmj3rsAsjY_I5MYXYr7M`.  
   - Utilizar a API do Google Drive (ou serviço Sheets/CSV público) para listar os arquivos mais recentes, baixar os `.xls` ou planilhas, converter para JSON (podendo reaproveitar o script `convert.py` para converter planilhas em HTML para a estrutura esperada) e atualizar os dados locais.  
   - Inserir mecanismo de autenticação/segreção seguro (OAuth2) com permissões somente de leitura.  
   - Exibir feedback de carregamento e erros via toast (ex.: “Não foi possível acessar o Drive – usando dados locais”).  
   - Registrar no rodapé a data/hora da última sincronização com o Google Drive.

5. **Outras considerações de usabilidade**

   - **Responsividade**: as novas cartas e gráficos devem adaptar‑se a telas menores. Considere empilhar os elementos verticalmente em `max-width 980px` como já implementado no modelo atual.  
   - **Acessibilidade**: adicionar rótulos `aria‑label` nos botões de copiar e nos elementos interativos; garantir contraste mínimo de texto e ícones; permitir navegação por teclado.  
   - **Internacionalização**: manter textos em português e permitir parametrização para outras unidades/meses.  
   - **Documentação**: manter comentários claros no código e atualizar o `README.md` explicando o novo processo de atualização via Google Drive.

## Requisitos adicionais

Além das melhorias gerais descritas acima, as seguintes funcionalidades adicionais devem ser implementadas:

### Filtro de datas e ajustes no gráfico de horas por dia

1. **Filtro de período** – adicionar campos de **data inicial** e **data final** no card “Horas por dia”. A interação deve ser realizada através de um calendário (“date picker”) com interface amigável que permita selecionar as datas sem digitar, compatível com dispositivos móveis e desktop. Ao aplicar o filtro, o gráfico e os KPIs devem ser recalculados exibindo apenas os lançamentos compreendidos no intervalo.

2. **Limite máximo de 31 dias** – o gráfico de barras deve exibir no máximo 31 colunas. Para períodos maiores, considerar compactar os dados (por exemplo, agregando por semana) ou dividir a visualização em páginas.

3. **Tooltip aprimorada** – no gráfico de barras, o tooltip deve mostrar a data completa em **DD/MM/AAAA**. Quando a filtragem de operadores estiver em “Todos os operadores”, incluir na tooltip a **média diária** calculada dividindo as horas totais do dia pelo número de operadores ativos (atualmente quatro), indicando algo como “Total: 8 h (média 2 h por operador)”.

### Personalização de cores e ícones

1. **Paleta de cores** – ajustar as cores da interface para harmonizar com as cores dos logotipos de Operação e Manutenção (`logo_OPE.png` e `logo_MNT.png`). Extrair as cores predominantes (azul para operação e amarelo/laranja para manutenção) e redefinir as variáveis CSS, mantendo contraste com o fundo escuro.

2. **Links nas logos** – transformar os logotipos no cabeçalho em links para `http://10.56.22.57:9080/maximo/ui/login?welcome=true`. Estes links devem abrir em nova guia e conter atributos `alt`, `title` e `aria‑label` descrevendo a ação (“Acessar Maximo – Operação” e “Acessar Maximo – Manutenção”).

3. **Ícone de relatório** – adicionar um ícone adicional utilizando o arquivo `logo_report.png`. Este ícone deve ficar próximo aos logotipos principais e apontar para `https://www.appsheet.com/start/8b5e3af0-da8c-475e-bf2f-3464aec1c5d5?platform=desktop#appName=Report_OS_31-982081519&vss=H4sIAAAAAAAAA62POw7CMBBErxJN7RO4RRQIAUUQDaYw8UayCHZkO4HI8nk4CBfD4SMKOqDcN5qn2Yhe06kMsjqAb-P7mtMAjiiwHloS4AITa4KzjQATWMrjA66cIuMLRUVJrtfXixVISDv2MgXy4PFbEf_XIgadcdC1JjdaR0e2PQ05HvsZfLaRGI5dkPuG7u_kdkqZ1bbqPKlNnvfTLD8z03MrjVpYleW1bDylG9_IZX-XAQAA&view=Ordens%20de%20Servi%C3%A7o`, com tooltip e descrição “Acessar relatório de Ordens de Serviço”.

4. **Pacote de recursos** – reunir todos os recursos (o arquivo `maximo_B_26-main.zip`, os três logotipos e este documento) em um único arquivo ZIP para facilitar o compartilhamento e uso em ambientes de IA. Nome sugerido: `dashboard_resources.zip`.

## Solicitações corporativas e ideias de implementação

As imagens de e‑mails corporativos anexadas indicam que a companhia exigirá novos KPI’s e análises mais rigorosas para 2026. As mensagens enfatizam várias métricas: número de ordens de serviço programadas versus concluídas, comparação de horas apontadas com horas programadas e disponíveis, além de aderência à manutenção programada. A seguir estão sugestões para incorporar esses indicadores à dashboard.

1. **Aderência ao plano de ordens de serviço** – implementar um painel comparando o **número de OS programadas** com o **número de OS concluídas** no mesmo mês. Exibir tanto os valores absolutos quanto a porcentagem de aderência (OS concluídas ÷ OS programadas × 100 %). Utilizar gráfico de barras ou linhas para permitir comparações mensais e por operador ou classe de equipamento. Fornecer um resumo no rodapé ou em tooltip indicando desvios.

2. **Homem‑Hora (HH) programado vs apontado** – criar indicador que mostre, para cada período, as horas programadas de trabalho e as horas efetivamente apontadas. O velocímetro/rosca descrito anteriormente pode ser reutilizado, com segmentos representando HH programado e HH apontado, incluindo setas e marcadores para metas. Incluir alertas visuais quando a diferença entre programado e apontado exceder determinado limiar.

3. **HH apontado vs HH disponível** – adicionar indicador de utilização de capacidade. Calcular a capacidade disponível como (8 h × número de operadores × dias úteis) e comparar com as horas apontadas. Representar em gráfico de barras ou donut, destacando a taxa de utilização percentual. Permitir filtrar por operador ou classe para identificar gargalos ou folgas de capacidade.

4. **Aderência à manutenção programada por classe (A–E)** – conforme o gráfico apresentado no e‑mail corporativo, criar uma visualização que mostre, para cada classe de equipamento, a aderência mensal à manutenção programada. Usar barras agrupadas (meses no eixo X, classes no eixo de séries) com legenda. Permitir drill‑down para ver detalhes de ordens em cada classe e mês, usando o mecanismo de tooltip detalhado. Mostrar no topo a média de aderência da unidade.

Esses novos painéis permitirão atender às exigências corporativas de 2026, fornecendo uma visão holística do desempenho em manutenção e operação e permitindo que gestores atuem proativamente na correção de desvios.

## Resumo

O trabalho consiste em modernizar a dashboard existente para torná‑la mais alinhada ao modelo `maximo_2026` e atender às novas demandas cobradas por e‑mail. As principais mudanças incluem adicionar logotipos e melhorar título e rodapé; criar um gráfico do tipo velocímetro ou rosca que compare as horas lançadas com as horas teóricas do mês, com marcações para horas úteis e segmentação OPER/Restante; adicionar botões de copiar para listas de ordens de serviço e tooltips com detalhes; e integrar a busca de dados em pastas do Google Drive, mantendo feedback para o usuário.  Essa especificação deve servir como guia para implementação das melhorias no frontend e nos scripts de atualização de dados, preservando a qualidade visual e a clareza técnica do painel【87211117776069†L10-L16】【87211117776069†L50-L58】.