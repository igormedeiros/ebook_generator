# Insumo Capítulo 3: Dando Vida ao Bot (@BotFather e Token)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Configuração @BotFather:** O processo padrão de criação de bots no Telegram, gerando o API Token.
- **Segurança do Token:** Tokens nunca devem ser colocados em arquivos de texto simples; o OpenClaw v2026.3.31 introduziu gestão de segredos externa via `audit -> configure -> apply`.
- **VPS "Um Clique":** Scripts de instalação automatizada para vincular o bot à instância Linux.

## Novidades (Últimos 60 dias)
- **External Secret Management:** Possibilidade de usar gestores de segredos (como 1Password ou variáveis de ambiente seguras) fora do `config.yaml`.
- **ClawHub Prioritization:** O sistema agora prioriza o ClawHub para evitar ataques de confusão de dependência em plugins de chat.

## Cicatrizes de Produção
- Vazamento de Token em repositórios públicos do GitHub é o erro #1; bots são sequestrados em minutos.
- **Dica:** Sempre desativar o "Join Groups" no @BotFather se o bot for para uso pessoal, para evitar spam.
