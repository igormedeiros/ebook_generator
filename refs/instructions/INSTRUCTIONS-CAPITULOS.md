<!-- instructions/INSTRUCTIONS-CAPITULOS.md -->
# instructions/INSTRUCTIONS-CAPITULOS.md
# 📘 CAPITULOS.md
> **Guia Mestre de Geração de Capítulos**
> Pipeline para pesquisar, gerar, revisar e publicar os capítulos do eBook técnico.

Todo capítulo deve ser construído com base em **pesquisa híbrida**, revisões multiperspectiva e validação contínua, usando:

| Ferramenta / MCP | Função |
|------------------|--------|
| `@context7` | Consultar documentação técnica atualizada (APIs, libs, comandos, specs) |
| `@GoogleSearch` | Buscar informações atuais da web |
| `@Memory` | Persistir aprendizados e contexto |
| `@sequentialThinking` | Raciocínio estendido, etapas, análises profundas |
| `mcp-markdownfy` | Revisão final e formatação Markdown |
| `mcp-docx-pdf` | Geração final do livro (DOCX + PDF) |

> 🧠 A IA não deve confiar apenas no conhecimento interno — deve pesquisar, validar e lembrar.

---

## 🛠️ Stack Tecnológico e Justificativas do Autor
Este e-book adota um conjunto de ferramentas modernas e de alta performance, escolhidas deliberadamente para otimizar o fluxo de trabalho do desenvolvedor [LINGUAGEM PRINCIPAL]. Todas as decisões técnicas são detalhadas e justificadas no arquivo `@INSTRUCTIONS-PREFERENCIAS_AUTOR.md`.

As principais escolhas são:

-   **[FERRAMENTA 1]**: [JUSTIFICATIVA PARA A FERRAMENTA 1].
-   **[FERRAMENTA 2]**: [JUSTIFICATIVA PARA A FERRAMENTA 2].
-   **[FERRAMENTA 3]**: [JUSTIFICATIVA PARA A FERRAMENTA 3].

A leitura do `@INSTRUCTIONS-PREFERENCIAS_AUTOR.md` é recomendada para uma compreensão aprofundada do "porquê" por trás das ferramentas utilizadas em todos os capítulos.

---

## 🎯 Objetivos deste Arquivo

1. Mapear e extrair **8 pilares** + **2 fundamentos** do tema do eBook.
2. Guiar a geração de **10 capítulos altamente técnicos** com profundidade crescente.
3. Fornecer **estrutura padrão** para todo capítulo.
4. Integrar:
   - 🌐 Pesquisa na web (`@GoogleSearch`)
   - 📦 RAG local (`@INSTRUCTIONS-LIVROS_BASE.md`)
   - 🧠 Memória contínua (`@Memory`)
   - 🧾 Referência técnica (`@context7`)

---

## 🌐 + 📚 Fontes e Modelo de Pesquisa

| Tipo | Ferramenta |
|------|------------|
| Documentação oficial | `@context7` |
| Pesquisa na internet | `@GoogleSearch` |
| Reflexão profunda | `@sequentialThinking` |
| Base literária local | `@INSTRUCTIONS-LIVROS_BASE.md` |
| Manutenção de contexto | `@Memory` |

---

## 🔄 Pipeline Obrigatório por Capítulo

1. **Pesquisar**  
   - `@GoogleSearch`: últimas referências, papers, APIs  
   - `@context7`: documentação técnica atualizada

2. **Consultar base local**  
   - `@INSTRUCTIONS-LIVROS_BASE.md`

3. **Raciocinar e estruturar**  
   - `@sequentialThinking`

4. **Registrar contexto e resultado**  
   - `@Memory`

5. **Revisar com personas**  
   conforme `@INSTRUCTIONS-REVISORES.md`

6. **Formatação final**  
   - `mcp-markdownfy`

7. **Exportar final**  
   - `mcp-docx-pdf` (gerar PDF + DOCX)

---

## 📂 Estrutura-Modelo de Capítulo

```markdown
# Capítulo <NN> — <Título>
> Nível: 🟦 Júnior | 🟨 Pleno | 🟥 Sênior  
> Fontes: Web + RAG + Docs Técnicas  
> Tempo médio: 60–90min  

## 🎯 Objetivos de Aprendizado
- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

## 🌱 Introdução e Contexto
(Conectar tema com saúde e prática real. O tom, estilo e a voz do autor devem seguir as diretrizes de @INSTRUCTIONS-ESPECIFICACOES.md, @INSTRUCTIONS-POSICIONAMENTO.md e @INSTRUCTIONS-OPINIOES_VISAO_AUTOR.md)

## 🌐 Pesquisa Web
(links pesquisados via `@GoogleSearch`)

## 📘 Documentação Oficial
(citações via `@context7`)

## 📚 RAG Local — `@INSTRUCTIONS-LIVROS_BASE.md`
- Livro / página  
- Insight extraído  
- Confiança

## 🧠 Conceitos-Chave
- Termos
- Fórmulas
- Pitfalls

## 💻 Exemplo de código
```python
# capitulo_<NN>/exemplo.py
...
````

## ⚙️ Estudo de caso aplicado

(usar `@INSTRUCTIONS-ESTUDOS_DE_CASO.md`)

## 🧪 Exercícios

(ver `@INSTRUCTIONS-EXERCICIOS.md`)

## ✅ Checklist de domínio

* Executei?
* Entendi?
* Expliquei em voz alta?

## 🔗 Referências finais

* Web
* Livros
* Docs

```

---

## 💡 Sequência dos 10 Capítulos

### Lógica base:
1. Fundamentos do tema
2. Conceitos essenciais
3. Hands-on progressivo
4. Integração avançada
5. Projeto / produto / deploy
6. Ética + saúde + impacto

---

## ✅ Checklist Global

| Item | OK |
|------|----|
Usar `@context7` para docs | ✔️
Pesquisar web via `@GoogleSearch` | ✔️
Consultar `@INSTRUCTIONS-LIVROS_BASE.md` | ✔️
Pensar com `@sequentialThinking` | ✔️
Salvar contexto com `@Memory` | ✔️
Revisar com `@INSTRUCTIONS-REVISORES.md` | ✔️
Formatar com `mcp-markdownfy` | ✔️
Exportar com `mcp-docx-pdf` | ✔️

---

> ✨ “Cada capítulo é uma ponte entre conhecimento humano, pesquisa viva e propósito em saúde.”

```