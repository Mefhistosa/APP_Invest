# Product Context — App Investidor

## Problema que Resolve

Investidores brasileiros individuais enfrentam dificuldade em:
1. Selecionar ativos compatíveis com seu perfil de risco sem ferramentas profissionais
2. Consolidar visão da carteira entre múltiplas planilhas e fontes
3. Acompanhar indicadores fundamentalistas e macroeconômicos de forma integrada
4. Avaliar sentimento de mercado sobre ativos específicos

## Personas

### Investidor Iniciante
- Pouca experiência com análise fundamentalista
- Prefere recomendações guiadas
- Busca ativos com DY consistente e baixa volatilidade
- Usa planilha ODS ou Google Sheets para controlar posições

### Investidor Moderado
- Conhecimento intermediário do mercado
- Aceita risco moderado por retornos melhores
- Quer dados fundamentalistas para decisões próprias
- Acompanha dividendos e proventos regularmente

### Investidor Agressivo
- Experiente e tolerante a risco
- Busca crescimento e oportunidades subvalorizadas
- Precisa de dados macro para contexto de mercado
- Quer análise de sentimento de notícias como input adicional

## Fluxo do Usuário

1. Abre o dashboard SPA (`/`)
2. Visualiza recomendações de ativos por perfil (aba Recomendações)
3. Cadastra posições via upload ODS, Google Sheets, ou manualmente
4. Acompanha carteira consolidada com preço médio e quantidade (aba Minhas Ações)
5. Visualiza gráficos de preço histórico com períodos selecionáveis (aba Gráficos)
6. Consulta dividendos provisionados e recebidos (aba Dividendos)
7. Analisa sentimento de notícias por ticker individual

## Casos de Uso

- **Recomendação:** Selecionar perfil → receber top 10 ativos com scores
- **Carteira:** Upload ODS → carteira consolidada com preço médio
- **Análise:** Buscar ticker → ver gráfico + dividendos + sentimento de notícias
- **Macro:** Consultar SELIC/CDI atuais para contexto de mercado
