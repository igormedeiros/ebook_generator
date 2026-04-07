# Insumos de Pesquisa Profunda - Capítulos 7 e 8
**Data da Coleta:** 2026-03-31
**Fontes:** 
- NotebookLM (ID: dc5583ba-3e82-46e7-bdb8-42bfae4f08c0)
- Google Web Search (Google Search API)

---

## Capítulo 7: Proatividade (Heartbeats e Cron Jobs)

### 1. Heartbeat (Batimento Cardíaco)
- **O que é:** Sistema de monitoramento baseado em condições. O agente "acorda" em intervalos (15-30 min) para verificar eventos sem consumir créditos de API continuamente.
- **Funcionamento:**
  1. Carrega o contexto (`working.md` e notas diárias).
  2. Verifica itens urgentes (e-mails, menções, tarefas atribuídas).
  3. Executa ação ou reporta "heartbeat ok" e volta a dormir.
- **Configuração Conversacional (Telegram):**
  - Ex: "monitorar o meu e-mail de 30 em 30 minutos e me informar se tem algum e-mail importante".
  - Comando explícito se falhar: "modifique o arquivo heartbeat".
- **Arquivo `heartbeat`:** Contém as instruções do que checar (memória, `working.md`, painel de controle).

### 2. Cron Jobs (Automação por Horário)
- **O que é:** Automação fixa baseada em horários predefinidos.
- **Configuração Conversacional:**
  - Ex: "todo dia às 9 horas da manhã me enviar um reporte".
  - Ex: "entrar no meu calendário e enviar um resumo de como será o dia seguinte sempre às 18 horas".
- **Casos de Uso Avançados:**
  - Relatório Matinal (6h): Coleta dados do Stripe, Supabase e suporte para enviar painel completo.
  - Daily Stand-up (00:00): Resume atividades de sub-agentes do dia anterior.

### 3. Comandos de Terminal
- **`open claw security audit`**: Auditoria de segurança.
- **`open claw doctor fix`**: Correção automática de plugins/skills.
- *Nota: O comando `openclaw flows` não existe na documentação pesquisada.*

---

## Capítulo 8: Conexões (Zapier MCP e Segurança)

### 1. Zapier MCP
- **Conceito:** Ponte segura ("mãos") para conectar o agente a aplicativos externos sem programação de APIs.
- **Vantagem:** Evita permissões globais inseguras que poderiam permitir deletar dados acidentalmente.

### 2. Passo a Passo de Conexão (Visual)
1. Criar servidor em `mcp.zapier.com`.
2. Adicionar ferramentas (Gmail, Google Agenda, Notion).
3. Login e autorização via interface Zapier.
4. Instalar skill **MCP** no OpenClaw (Menu Agentes > Habilidades).
5. Gerar Token no Zapier e colar no chat do OpenClaw (ou via gerenciador de segredos).

### 3. Segurança e Permissões Granulares
- **Gmail:** Autorizar "encontrar labels" e "criar rascunhos". **Desmarcar** "deletar", "arquivar" e "enviar".
- **Agenda:** Autorizar leitura, **proibir** deletar ou atualizar.
- **Notion:** Autorizar leitura/escrita, **proibir** deletar páginas/bancos de dados.
- **Alerta de Token:** Colar tokens diretamente no chat gera um aviso de segurança. Recomenda-se o uso de cofres como 1Password para chaves de API.

---

## Pesquisa Externa (Alertas de Última Hora - Fev/Mar 2026)

### 1. Crise de Segurança OpenClaw
- **Vulnerabilidades Críticas:**
  - **RCE (CVE-2026-25253):** Execução remota de código via WebSocket malicioso.
  - **Sandbox Escape (GHSA-v8wv-jg3q-qwpq):** Leitura de arquivos do sistema hospedeiro.
  - **Privilege Escalation (GHSA-hc5h-pmr3-3497):** Controle administrativo total do gateway.
- **Malware no ClawHub:** Identificadas 1.100+ skills maliciosas exfiltrando tokens e chaves de API.
- **Ação Obrigatória:** Atualizar para a versão **v2026.3.31+** que bloqueia skills inseguras por padrão.

### 2. Recomendações Técnicas
- **Bind de IP:** Configurar para `127.0.0.1` (evitar exposição pública 0.0.0.0).
- **Node.js:** Versão mínima 22.12.0+.
- **Skills:** Usar apenas skills com selo "benigno" (verificado).
