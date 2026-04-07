# Insumo Capítulo 7: Proatividade (Heartbeats/Crons)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Heartbeats:** Ciclos de "consciência" periódicos (ex: a cada 30m) guiados pelo arquivo `HEARTBEAT.md`.
- **Crons:** Agendamentos de precisão para tarefas específicas (relatórios matinais, backups).
- **WakeMode:** O agente pode ser configurado para "acordar" em horários específicos ou em resposta a eventos externos.

## Novidades (Últimos 60 dias)
- **lightContext:** Opção para rodar heartbeats com contexto reduzido, economizando tokens ao ignorar o histórico completo do chat.
- **CLI Cron:** Comandos aprimorados: `openclaw cron add --every "day at 09:00" --session isolated`.

## Cicatrizes de Produção
- Heartbeats muito frequentes (ex: a cada 1 min) destroem o orçamento de API e podem causar rate-limits se o agente tentar processar muitas ferramentas.
- **Cicatriz:** Relatórios matinais que falham por queda de internet ou VPS; o novo ledger de flows ajuda a retomar tarefas perdidas.
