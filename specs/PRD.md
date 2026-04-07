# Product Requirements Document (PRD) - Amazon Ebook Generator (Technical Factory)

## 1. Visão Geral
Fábrica automatizada de e-books técnicos sob a ótica do **Autor-Empreendedor**. Unindo precisão técnica (Python/IA), voz autoral ("Código com Alma") e estratégia de mercado (KDP).

---

## 2. 🚀 Pipeline de Produção (Mandato de Checkpoint)
**Regra de Ouro:** Não confie na memória do agente. Cada interação, decisão ou geração deve ser salva imediatamente em um arquivo `.md` no diretório `workspace/process/`.

1.  **Input de Tema:** Salvamento do tema, nicho e contexto inicial (`00-THEME.md`).
2.  **Metadados:** Título, Subtítulo e Mensagem Central (`01-METADATA.md`).
3.  **Visão do Autor:** Seleção da base filosófica (`01B-VISION.md`).
4.  **Estilo do Autor:** Seleção do guia editorial (`01C-STYLE.md`).
5.  **Tipo de Livro:** Confirmação das regras de tipo, ex: TECH (`01D-TYPE.md`).
6.  **Avatares:** Perfis de leitores ideais e pesquisa de mercado (`02-AVATARS.md`).
7.  **Requirements:** Tecnologias, pacotes e "must-haves" técnicos (`03-REQUIREMENTS.md`).
8.  **Outline:** Estrutura de 10 capítulos validada (`04-OUTLINE.md`).
9.  **Deep Research:** Registro exaustivo de referências e achados (`05-RESEARCH_LOG.md`).
10. **Drafting (Capítulo por Capítulo):** Cada capítulo gerado é salvo individualmente em `workspace/content/`.
11. **Refinamento (Avatares):** Logs de feedback dos 3 ciclos de leitura crítica (`06-AVATAR_FEEDBACK.md`).
12. **Revisão Editorial (Personas):** Consolidação dos ajustes do conselho de 21 especialistas (`06B-EDITORIAL_REVIEW.md`).
13. **Validação Final:** Relatório de métricas (palavras, estrutura, links) (`07-FINAL_AUDIT.md`).
14. **Entrega:** Registro de conversão e log de envio para o Kindle (`08-DELIVERY_LOG.md`).

---

## 3. Requisitos Funcionais & Métricas
- **Extensão:** Alvo de 15.000 palavras.
- **Estrutura Fixa:** 10 capítulos + Intro + Conclusão.
- **Saída:** Diretório `output/` e envio para `igor.medeiros_bMKtAL@kindle.com`.
- **Didática:** Padrão "Conceito -> Código -> Explicação".

---

## 4. 🛠️ Tecnologias & Distribuição
- **Core:** Python 3.10+, Pandoc, Mermaid.js, Nano Banana 2.
- **Entrega:** Integração com serviço de e-mail (SMTP/API) para envio direto ao dispositivo Kindle.

---

## 5. 🤖 Instruções para o Agente
- Use as histórias de `STORIES.md` para humanizar a técnica.
- Mantenha o tom: "Não escrevo para máquinas. Escrevo para pessoas que cuidam de pessoas."
- Antes de converter, garanta que o volume está próximo das 15k palavras.
