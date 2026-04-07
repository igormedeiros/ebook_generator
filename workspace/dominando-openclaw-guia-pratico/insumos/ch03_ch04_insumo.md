# Insumo Capítulo 3: Dando Vida ao Bot (@BotFather e Token)
**Fonte:** Pesquisa Consolidada (v2026.3.31)
**Data:** 2026-04-01

## Detalhes @BotFather para Não-Devs
- **Criação:** Enviar `/newbot`, escolher nome de exibição e username (obrigatoriamente terminando em `bot`).
- **Segurança:** Desativar "Join Groups" e "Inline Mode" se o uso for estritamente pessoal (evita intrusões).
- **Bot Settings:** Configurar o Menu Button para os comandos principais para facilitar a usabilidade móvel.

## Vinculação de Token na v2026.3.31
- **Protocolo Seguro:** Abandono de tokens em arquivos `.yaml` ou `.env` simples para evitar vazamentos em logs.
- **Uso de `openclaw secrets`:** Novo comando para injetar credenciais de forma criptografada.
- **Procedimento:** `openclaw configure` -> selecionar provedor Telegram -> colar token (o sistema agora mascara o input automaticamente).

## Comandos Iniciais Recomendados
- `/start`: Aciona o `heartbeat` inicial e valida as permissões do seu ID único (Chat ID).
- `/status`: Verifica a saúde das "garras" (plugins) e a latência (velocidade) da sua IA.
- `/help`: Lista as habilidades (skills) ativas e o manual de comandos rápidos do seu robô.

---

# Insumo Capítulo 4: Moldando a Alma (soul.md e Tamagotchi)
**Fonte:** Pesquisa Consolidada (v2026.3.31)
**Data:** 2026-04-01

## Conceito Tamagotchi
- **Alimentação de Dados:** O agente "morre" (torna-se um chat genérico e chato) se não receber inputs constantes de contexto sobre sua vida e negócios.
- **Áudios e Notas:** Uso de transcrições de áudios rápidos ("Áudios de Uber") e notas diárias para atualizar a memória de curto prazo e reforçar a identidade única do agente.

## Estrutura Obrigatória `soul.md`
- **Personalidade:** Adjetivos e arquétipo (ex: "Socrático", "Direto", "Cético", "Otimista").
- **Valores:** O que o agente prioriza (ex: "Privacidade acima de conveniência", "Segurança em primeiro lugar").
- **Tom de Voz:** Estilo linguístico (ex: "Uso de termos técnicos", "Sem emojis", "Conciso e objetivo").

## Cicatrizes de Produção
- **Identidade Genérica:** Agentes que tentam agradar a todos acabam sendo medíocres e não resolvem problemas reais.
- **Identidade Especialista:** O sucesso reside em definir "opiniões fortes" no arquivo `soul.md`. Um agente que tem opinião toma decisões melhores e mais rápidas.
- **Vazamento de Identidade:** Cuidado ao copiar o `soul.md` de outra pessoa; o agente passará a agir como ela, não como você.