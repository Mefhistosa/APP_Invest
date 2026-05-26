# Progress — App Investidor

## O Que Já Foi Feito

### Funcionalidades Entregues
- [x] API REST com 14 endpoints cobrindo recomendações, carteira, dividendos, macro, notícias
- [x] Frontend SPA com 4 abas funcionais (Minhas Ações, Gráficos, Dividendos, Recomendações)
- [x] 3 perfis de investimento com filtros fundamentalistas (iniciante/moderado/agressivo)
- [x] Carteira via 3 fontes: ODS, Google Sheets, JSON local (+ mock)
- [x] Análise de sentimento de notícias (DeepSeek + fallback keywords)
- [x] Dados macroeconômicos (SELIC/CDI)
- [x] Gráficos ECharts com períodos 7d/30d/90d/6m/1a
- [x] Upload de arquivo ODS via POST
- [x] Health check endpoint

### Infraestrutura
- [x] Ambiente virtual Python configurado
- [x] Script start.sh com detecção automática
- [x] .gitignore configurado
- [x] Documentação inicial em docs/ (9 arquivos)
- [x] Memory Bank criado (6 arquivos)

## O Que Falta

### Correções Pendentes
- [ ] Datas hardcoded nos mocks (ex: "2026-06-15", "2026-05-01") — tornar dinâmicas
- [ ] Duplicação de código: `parse_portfolio_from_csv()` e `parse_portfolio_from_worksheet()` são idênticas
- [ ] Imports de função dentro de `main.py` (linhas 82, 219, 256) — mover para topo
- [ ] `CVm_CODE_MAP` com códigos CVM duplicados (ITUB4/ITSA4/BBSE3 = 1023)

### Melhorias Planejadas
- [ ] Importar skill `documentador-python` na empresa Paperclip
- [ ] Configurar `instructionsPath` do agente Documentador Python
- [ ] CORS restrito para produção (atualmente `*`)
- [ ] Tratamento de erro consistente em todos os endpoints
- [ ] Remover dependências não utilizadas (`aiohttp`, `yfinance`)
- [ ] Remover diretório `doc/` (deprecado)

## Bugs Conhecidos

| Bug | Severidade | Arquivo | Status |
|-----|-----------|---------|--------|
| CVM code 1023 compartilhado por ITUB4, ITSA4 e BBSE3 | Média | `services/dados_mercado.py` | Aberto |
| Dados mock com datas fixas de 2026 | Baixa | `services/google_sheets.py` | Aberto |
| Gráfico gera random walk quando Brapi falha | Média | `main.py` (endpoint chart) | Aberto |
| Import dentro de função em 3 lugares | Baixa | `main.py` | Aberto |

## Correções Recentes na Carteira

### Soma de Quantidade (QTDE)
`ods_reader.py` agrupa corretamente por Ativo e soma as quantidades. O cálculo do preço médio usa `total_cost / quantity`.

### Remoção de VL VENDA
`VL VENDA` não é processado em nenhum serviço. Decisão confirmada: preço de venda não altera preço médio de posição.

### Subtração na Alteração
`custom_portfolio.py:sell_stock()` implementa subtração correta. Se quantidade <= 0 após venda, posição é removida.

## Próximos Marcos

1. **Configurar Documentador Python** — importar skill, configurar agente
2. **Corrigir bugs conhecidos** — CVM codes, datas mock, imports no topo
3. **Restringir CORS** — preparar para produção
4. **Cleanup dependencies** — remover pacotes não usados
