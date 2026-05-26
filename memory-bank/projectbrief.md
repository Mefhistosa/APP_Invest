# Project Brief — App Investidor

## Visão Geral

Sistema web de acompanhamento e recomendação de investimentos em ações brasileiras. Combina dados fundamentalistas, análise de sentimento de notícias e indicadores macroeconômicos para gerar recomendações personalizadas conforme o perfil do investidor.

## Objetivos

- Recomendar ativos da B3 conforme perfil de risco (iniciante/moderado/agressivo)
- Consolidar carteira do usuário em múltiplas fontes (planilha ODS, Google Sheets, JSON local)
- Exibir dividendos, histórico de preços e indicadores macro (SELIC/CDI)
- Analisar sentimento de notícias por ticker via IA (DeepSeek) + keywords

## Escopo

| Inclui | Não inclui |
|--------|------------|
| API REST (FastAPI) com 14 endpoints | Execução de ordens (compra/venda real) |
| Frontend SPA com ECharts | Autenticação de usuários |
| 3 perfis de investimento | Integração com corretoras |
| Carteira local (JSON/ODS/Sheets) | Dados em tempo real |
| Dados fundamentalistas de 48+ ativos | Suporte a outros mercados (EUA, cripto) |
| Análise de sentimento de notícias | Notificações push |

## Stack Principal

Python 3.12 + FastAPI + Uvicorn + Vanilla JS + ECharts

## Cronograma

Projeto em estágio inicial operacional. Próximas iterações focam em correções de tratamento de dados da carteira e melhoria de fallbacks.
