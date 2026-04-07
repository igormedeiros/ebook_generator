# O Stack do Livro (03-REQUIREMENTS.md)

Para dar vida ao seu Agente 24h, você precisará escolher onde ele irá "morar". Ele precisa de um lugar que nunca durma e que tenha energia constante.

## 1. Onde seu Robô vai morar? (Hospedagem)

### Opção A: O "Hotel de Luxo" (VPS na Nuvem)
Ideal para quem quer facilidade total e não quer se preocupar com queda de luz ou internet em casa. 
- **Hostinger:** A mais recomendada para não-devs pela interface intuitiva e instalador "um clique" do OpenClaw.
- **Locaweb:** Uma das opções mais tradicionais e com excelente reputação no Brasil, com suporte em português.
- **AWS (Amazon) ou Google Cloud:** As "Big Techs". São extremamente robustas e possuem servidores em São Paulo, garantindo que sua IA responda sem atrasos (latência baixa).

### Opção B: A "Garagem Tecnológica" (Instalação Local)
Você pode rodar o OpenClaw em um computador na sua própria casa, desde que ele fique **ligado 24h por dia**.
- **A Regra de Ouro:** Nunca instale diretamente no seu computador pessoal de trabalho ou lazer. Se algo travar, seu robô para.
- **Isolamento é Segurança:** Recomendamos usar o **Docker** (pense nele como uma "bolha de proteção" dentro do seu PC) ou uma máquina dedicada apenas para isso.
- **O Setup do Autor:** Como exemplo de alta performance, eu (Igor) utilizo um **PC dedicado com Linux**, equipado com GPUs potentes para rodar "LLMs Locais" (modelos de linguagem que não dependem da internet para pensar). É uma verdadeira central de inferência privada.

## 2. A "Chave do Motor" (Tokens e APIs)
Você precisará de créditos para que sua IA possa raciocinar. 

### ⚠️ AVISO CRÍTICO: Bloqueio de Contas de Consumidor
Desde fevereiro de 2026, a **Anthropic** e o **Google** estão bloqueando permanentemente contas de consumidores (Claude Pro e Gemini Ultra) que utilizam o OpenClaw através de login direto (OAuth). Tentar usar sua conta pessoal de "chat" como motor do robô pode causar a perda total dos seus e-mails e arquivos.

### O Caminho Seguro:
- **Chaves de API Oficiais (BYOK):** Em vez de usar seu login de usuário, você deve criar uma conta de desenvolvedor (na Anthropic Console ou Google AI Studio) e gerar uma **API Key**. É mais seguro e você paga apenas pelo que o robô consome.
- **Alibaba Cloud (Model Studio):** Uma das melhores alternativas atuais, oferecendo APIs para modelos poderosos como o **Qwen 3.5** e outros, com alta performance e custos competitivos.
- **OpenRouter ou DeepSeek:** São excelentes alternativas para iniciantes, pois oferecem acesso a vários modelos com baixo risco de bloqueio.
- **LLMs Locais com Ollama:** Muitos usuários preferem rodar seus próprios modelos usando o **Ollama**. É a forma definitiva de privacidade e economia zero.

### Estratégia Híbrida (Dica de Ouro)
A estratégia mais inteligente usada por profissionais hoje é o "Mix de Inteligência":
1. **O Cérebro (Agente Principal):** Use modelos de elite via API (como Claude 3.5 Sonnet ou GPT-4o) para o agente orquestrador. Ele precisa de alta capacidade de raciocínio para entender ordens complexas e delegar.
2. **Os Braços (Agentes de Execução):** Para tarefas repetitivas e simples (como resumir um texto, formatar um dado ou traduzir), direcione esses agentes para rodarem localmente via **Ollama**. Isso reduz drasticamente seus custos mensais sem perder a eficiência da equipe.

## 3. A "Ponte de Comando" (Interface)
- **Telegram (Grátis):** Será o seu "controle remoto". Você instalará o aplicativo no celular para dar ordens e receber relatórios da sua IA através de um Bot privado.

## 4. O "Cérebro de Apoio" (Conexões)
- **Zapier (Versão Grátis atende o início):** Para conectar sua IA ao Gmail, Notion e Google Agenda de forma visual, sem precisar digitar códigos.

---

### Dica do Especialista (Cicatriz de Produção)
"Vi muitos amigos perderem contas de 10 anos do Google por tentarem economizar usando o Gemini Ultra no robô. Não arrisque sua vida digital. Use chaves de API oficiais ou, se quiser total soberania, parta para os modelos locais. No meu PC Linux, o robô é 100% meu e ninguém pode desligá-lo." — Igor Medeiros