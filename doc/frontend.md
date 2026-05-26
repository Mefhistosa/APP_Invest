# Frontend — SPA com JavaScript Vanilla (deprecated)

> **A documentacao foi movida para [`docs/frontend.md`](/home/dsa/Documentos/app_investidor/docs/frontend.md).**

Arquivo: `index.html`

SPA construida com JavaScript vanilla e ECharts para graficos.

---

## Tecnologias

- HTML5 + CSS3 (Flexbox, Grid, variaveis CSS)
- JavaScript ES6+ (async/await, arrow functions, template literals)
- ECharts 5.4.3 (CDN) para graficos de linha interativos

---

## Abas

| Aba | Conteudo |
|-----|----------|
| Minhas Acoes | Carteira com totais, variacao, resultado |
| Graficos | Historico de cotacoes com ECharts |
| Dividendos | Proventos recebidos com filtro por tipo |
| Recomendacoes | Sugestoes por perfil de investidor |

---

## Componentes

### Carteira
- Tabela responsiva com scroll horizontal
- Summary bar: Total Investido, Valor Atual, Resultado, Rentabilidade
- Destaque verde/vermelho para valores positivos/negativos
- Atualizacao automatica ao trocar para aba

### Grafico
- Integracao com ECharts
- Periodos: 7d, 30d, 90d, 6m, 1a
- Linha com gradiente verde/vermelho conforme variacao
- Linha tracejada azul da media do periodo
- Info cards: Ultimo, Abertura, Maxima, Minima, Variacao
- Responsivo (resize listener)

### Dividendos
- Filtro por tipo (JCP/DIVIDENDO/Todos)
- Badges: azul (JCP), cinza (DIVIDENDO)
- Ordenacao por data de pagamento

### Recomendacoes
- Cards de perfil com emoji e descricao
- Clique no perfil dispara busca automatica
- Noticias em paralelo (`Promise.all`)
- Top 5 com noticias positivas
- Badges: verde (boa), vermelho (ruim), azul (recomendado)

---

## Chamadas de API

Todas usam `fetch()` com handler unificado via `apiCall()`. Base URL configuracel via constante `BASE`.

```javascript
async function apiCall(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  return resp.json();
}
```
