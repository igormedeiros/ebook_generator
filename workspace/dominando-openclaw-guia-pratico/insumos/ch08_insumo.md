# Insumo Capítulo 8: Conexões (Zapier MCP/Notion)
**Fonte:** Pesquisa Web / NotebookLM ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0
**Data:** 2026-04-01

## Resumo Técnico
- **Zapier MCP:** Gateway que conecta o OpenClaw a +6.000 apps (Gmail, Notion, Slack).
- **Notion:** Uso para bancos de dados de tarefas e documentação visual.
- **Gmail:** Recomendação de uso apenas para rascunhos (`Create Draft`) por segurança, evitando envios automáticos acidentais.

## Novidades (Últimos 60 dias)
- **Unified Tool Mapping:** O Zapier MCP agora permite mapear ferramentas específicas diretamente no OpenClaw via URL do servidor MCP única.
- **Restrição de Gateway:** Rejeição de configurações inseguras de tokens em integrações de terceiros.

## Cicatrizes de Produção
- Dar permissão de "Delete" ao agente em bancos de dados do Notion é perigoso; o agente pode interpretar um pedido de limpeza como uma deleção em massa.
- **Regra de Ouro:** Sempre comece com permissões de "Read/Write" mas nunca "Admin/Delete".
