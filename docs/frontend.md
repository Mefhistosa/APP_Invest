# Frontend — SPA com JavaScript Vanilla

Arquivo: `index.html`

SPA (Single Page Application) construída com JavaScript vanilla e ECharts para gráficos.

## Tecnologias

- **HTML5** + **CSS3** (Flexbox, Grid, variáveis CSS)
- **JavaScript ES6+** (async/await, arrow functions, template literals)
- **ECharts 5.4.3** (CDN) para gráficos de linha interativos

## Abas

| Aba | ID | Descrição |
|-----|-----|-----------|
| Minhas Ações | `portfolio` | Carteira com totais, variação, resultado |
| Gráficos | `charts` | Histórico de cotações com ECharts |
| Dividendos | `dividends` | Proventos recebidos com filtro por tipo |
| Recomendações | `recommendations` | Sugestões por perfil de investidor |

## Funcionalidades

### Carteira (`loadPortfolio`)
- Tabela responsiva com scroll horizontal
- Summary bar com Total Investido, Valor Atual, Resultado (R$), Rentabilidade (%)
- Destaque visual verde/vermelho para valores positivos/negativos
- Atualização automática ao trocar para aba

### Gráfico (`loadChartData`, `renderChart`)
- Integração com ECharts
- Períodos selecionáveis: 7d, 30d, 90d, 6m, 1a
- Linha de preço com gradiente verde/vermelho conforme variação
- Linha tracejada azul da média do período
- Info cards: Último, Abertura, Máxima, Mínima, Variação do Período
- Responsivo (resize listener)

### Dividendos (`loadDividends`, `filterDividends`)
- Filtro por tipo de dividendo (JCP/DIVIDENDO/Todos)
- Badges coloridos: azul para JCP, cinza para DIVIDENDO
- Ordenação por data de pagamento

### Recomendações (`loadRecommendations`)
- Cards de seleção de perfil com emoji e descrição
- Clique no perfil já dispara a busca
- Busca notícias em paralelo (`Promise.all`) para cada ação
- Filtra top 5 com notícias positivas
- Badges: verde (boa), vermelho (ruim), azul (recomendado)

## Estilos

- Paleta escura: `#1a1a2e`, `#16213e`, `#0f3460`
- Cards com sombra suave e bordas arredondadas (12px)
- Botões com hover states e transições suaves
- Gradiente no header e na summary bar
- Loading spinner animado
- Totalmente responsivo (breakpoint 900px)

## API Calls

Todas as chamadas usam `fetch()` com handler de erro unificado via `apiCall()`.
Base URL configurável via constante `BASE` (vazia para mesmo origin).
