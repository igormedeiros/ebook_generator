<!-- knowledge/RAG-PREFERENCIAS_AUTOR.md -->
# **Preferências do Autor: Resumo Estratégico para o Ebook**

Este documento sintetiza as escolhas tecnológicas e metodológicas do autor, servindo como base para as justificativas técnicas e princípios apresentados no ebook.

---

## 1. Gerenciamento de Dependências com `uv`

A ferramenta `uv` é a **principal escolha para gerenciamento de dependências Python** devido à sua **performance excepcional** (10x a 100x mais rápido que `pip` e `venv`) e à **consolidação de funcionalidades** de diversas ferramentas (pip, venv, pip-tools, pipx, pyenv) em uma única CLI. Sua arquitetura em Rust garante eficiência, paralelismo e baixo overhead, resultando em um **ciclo de desenvolvimento mais ágil** e **redução de custos** em ambientes CI/CD.

---

## 2. Ecossistema Gemini para Agentes de IA

A adoção dos modelos **Gemini 2.5 Flash e Pro** é estratégica para o desenvolvimento de Agentes de IA, explorando uma **arquitetura dual otimizada para performance e custo**:

*   **Gemini 2.5 Flash:** Ideal para **automação rápida**, tarefas de alto volume e baixo custo (e.g., classificação, extração de dados) devido à sua velocidade e eficiência.
*   **Gemini 2.5 Pro:** O "cérebro" para **raciocínio complexo**, planejamento, decomposição de tarefas e geração de código, com uma **janela de contexto expansiva** (até 2 milhões de tokens) que permite análise holística de grandes volumes de informação.

A combinação de ambos os modelos permite uma **arquitetura híbrida eficiente**, onde o Pro planeja e o Flash executa subtarefas em paralelo. O **modelo de preços competitivo** e o **Free Tier generoso** removem barreiras de entrada, tornando a plataforma acessível a todos os desenvolvedores.

---

## 3. Ambiente de Desenvolvimento Linux / WSL

A padronização em **Linux / WSL** é escolhida para **maximizar produtividade, compatibilidade e performance**. Este ambiente oferece:

*   **Consistência com Produção:** Elimina bugs de paridade, pois a maioria das aplicações é implantada em servidores Linux.
*   **Compatibilidade Nativa de Ferramentas:** Acesso robusto a shells BASH e utilitários Unix, presentes em tutoriais e scripts de automação.
*   **Performance e Facilidade de Instalação:** Bibliotecas Python de alto desempenho têm melhor performance e são mais fáceis de instalar em Linux.
*   **Integração Superior com Docker:** O WSL 2 permite que o Docker execute contêineres Linux nativamente no Windows com performance quase nativa.

O WSL 2 oferece uma plataforma de desenvolvimento de ponta, combinando a conveniência do Windows com o poder do Linux.
---

## 4. Limitações e Contenção

Embora `uv` e Gemini sejam ferramentas revolucionárias, é fundamental reconhecer suas **limitações atuais e sua trajetória de desenvolvimento**. As equipes por trás dessas ferramentas têm demonstrado grande agilidade em corrigir falhas e adicionar funcionalidades. A adoção dessas tecnologias representa não apenas uma aposta em seu estado atual, mas também em seu **futuro promissor**, com a expectativa de paridade de recursos e manutenção da vantagem de performance fundamental.