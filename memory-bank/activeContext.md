# Active Context

## Estado Atual (2026-05-25)
Sistema funcional com todas as rotas operacionais. Frontend SPA com abas de carteira, gráficos, dividendos e recomendações.

## Últimas Alterações
- Limpeza de arquivos não versionados (pycache, .env, binários)
- Initial commit do projeto no GitHub
- Criação do Memory Bank (projectbrief, productContext, systemPatterns, techContext, activeContext, progress)

## Problemas Conhecidos / Bugs
1. **Soma de QTDE na consolidação de carteira** — Ao mesclar ODS + custom_stocks, o campo `quantity` do ODS usa `old_qty + q` que pode duplicar se o mesmo ticker já foi carregado do custom. Precisa normalizar: usar apenas ODS como base, depois somar custom como adicional.
2. **VL VENDA na venda de ativos** — A rota `/api/v1/portfolio/sell` não registra o valor da venda. Apenas subtrai quantidade sem criar histórico de venda com preço realizado.
3. **Subtração na alteração de quantidade** — Quando um ativo é vendido parcialmente, a quantidade é subtraída mas o preço médio não é recalculado corretamente para refletir a venda (deveria manter o preço médio original pois a venda não altera o custo médio remanescente).

## Próximas Ações Prioritárias
1. Corrigir soma de QTDE na consolidação ODS + custom — usar ODS como base e custom como adicional
2. Remover VL VENDA da lógica de sell — não deve ser necessário para venda
3. Garantir que subtração na alteração mantenha preço médio correto

## Decisões Técnicas Pendentes
- Implementar histórico de transações (compras e vendas)
- Adicionar testes automatizados
- CI/CD via GitHub Actions
