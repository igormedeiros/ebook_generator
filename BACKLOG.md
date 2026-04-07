# 📋 Backlog de Projeto: AI eBook Generator & Course Platform

**Header: Metadados**
* **Versão:** 1.4
* **Status:** Pronto para Sprint Planning
* **Autor:** Igor Medeiros
* **Data:** 07 de Abril de 2026
* **Reviewers:** Gemini AI, Community (GitHub)

---

## 1. Fluxo de Trabalho
1. **Captura:** Adicionar novos itens nesta lista.
2. **Priorização:** Avaliar o impacto e a urgência de cada item (P0, P1, P2).
3. **Planejamento:** Para itens priorizados, criar um plano de execução detalhado.
4. **Execução:** Mover para a lista de TODO no `GEMINI.md` após o planejamento.

---

## 2. Visão Geral
Sistema automatizado para conversão de manuscritos técnicos originais em produtos multimídia escaláveis. O pipeline processa um arquivo Markdown mestre e o deriva em dois caminhos: locução naturalista via **Qwen3-TTS** e material didático visual (PowerPoint) para a plataforma **Udemy**, mantendo a transparência da colaboração IA e o compromisso social de acesso gratuito ao texto base.

---

## 3. Requisitos Arquiteturais & Pendências Técnicas

### 3.1 Prioridade Alta (P0)
- [ ] **R-01: Notas de Autoria e Fraternidade** - Implementar geração automática de seções detalhando a autoria humana (100% ideias/histórias) e a declaração de acesso gratuito no GitHub.
- [ ] **R-02: Integração Qwen3-TTS** - Configurar motor para síntese de voz com Zero-Shot Voice Cloning (voz de Igor Medeiros).
- [ ] **Normalização Fonética** - Script para limpar sintaxe Markdown e inserir tags de prosódia para o motor TTS.
- [ ] **Sistema de Logs** - Implementar logging robusto na `ebook_factory.py`.

### 3.2 Prioridade Média (P1)
- [ ] **R-03: Derivação Automática MD** - Criar transformadores para converter MD Mestre em `MD-TTS` (locução) e `MD-Slides` (sumarizado).
- [ ] **R-04: Exportação PPTX** - Integração com `python-pptx` para injetar conteúdo em Template Mestre (.potx).
- [ ] **Estrutura Udemy** - Organização automática de módulos/lições baseada em headers H1/H2.
- [ ] **Conversão EPUB** - Script para conversão via Pandoc.

### 3.3 Prioridade Baixa (P2)
- [ ] **Interface CLI** - Desenvolver dashboard no terminal para gerenciar status da produção.
- [ ] **Sistema de Cache** - Cache para transcrições de vídeos do YouTube.
- [ ] **Validação de Links** - Verificação automática de links quebrados nos HTMLs gerados.
- [ ] **Sincronização Áudio/Slide** - Pesquisa de metadados de tempo para automatizar transições.

---

## 4. Decisões de Tecnologia (Source of Truth)
| Componente | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.x | Expertise do autor e ecossistema de automação. |
| **Motor TTS** | Qwen3-TTS | Controle por linguagem natural e baixa latência. |
| **Sumarização** | LangChain / Gemini | Eficiência em transformar parágrafos em bullet points. |
| **Manipulação PPTX** | `python-pptx` | Automação programática via templates `.potx`. |

---

## 5. Riscos e Mitigações
- **Qualidade da Clonagem:** Utilizar amostras de 30s de alta fidelidade.
- **Quebra de Layout:** Limitar número de bullets por slide via script de sumarização.
- **Licenciamento:** Definir entre MIT ou Creative Commons para o repositório GitHub.
