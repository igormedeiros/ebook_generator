# Insumo Capítulo 2: Hospedagem (Nuvem vs Local/Linux)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Opções de Hospedagem:**
  - **Nuvem (Hostinger, AWS, Locaweb):** Ideal para bots que precisam de 100% de uptime no Telegram.
  - **Local (PC com Linux/Docker):** Recomendado para "Infrerência Local" e privacidade máxima.
- **Isolamento:** Uso de Docker para garantir que o ambiente do agente não interfira no sistema host.
- **Node Pairing:** Comandos em nós remotos agora exigem aprovação explícita (v2026.3.31).

## Novidades (Últimos 60 dias)
- **OpenClaw Doctor:** Novo comando `openclaw doctor` para validar o setup de rede e permissões após atualizações.
- **Gateway Restrições:** O gateway agora rejeita tokens compartilhados mistos; exige autenticação direta para segurança local.

## Cicatrizes de Produção
- Rodar em Windows nativo costuma causar erros de path e permissões; o uso de WSL2 ou Linux puro é a "regra de ouro".
- **Erro comum:** Não configurar limites de memória no Docker, o que pode causar travamento do host durante inferências pesadas.
