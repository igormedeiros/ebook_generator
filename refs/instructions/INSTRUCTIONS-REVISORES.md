<!-- instructions/INSTRUCTIONS-REVISORES.md -->
# 🧩 REVISORES.md
> **Sistema de Revisão Multiperspectiva — 20 Personas de Revisão**  
> Documento que define as personas responsáveis por revisar, validar e aprimorar o conteúdo do eBook em diferentes camadas: técnica, ética, filosófica, emocional e estética.  
> Cada persona representa uma lente de revisão no pipeline do `@GEMINI.md`.

---

## 🧭 FINALIDADE
Garantir que o eBook final seja:
- **Tecnicamente correto**  
- **Humanamente sensível**  
- **Cientificamente embasado**  
- **Didaticamente claro**  
- **Narrativamente fluido**  

> “Revisar não é apenas corrigir — é lapidar sentido.”  
> — *Igor Medeiros*

---

## 🧠 VISÃO GERAL DO PROCESSO
Durante a revisão, cada persona lê e comenta o manuscrito com uma função específica.  
Os agentes de revisão trabalham em **camadas sequenciais**, unindo técnica, emoção e propósito.

---

## 🧩 PERSONAS DE REVISÃO (20)

As 20 personas de revisão estão detalhadas em arquivos individuais para maior clareza e modularidade. Cada persona herda da persona base de escrita (`@knowledge/RAG-PERSONA.md`) e a especializa com um foco de revisão único.

| # | Persona | Foco Principal | Arquivo de Instrução |
|---|---|---|---|
| 1 | O Programador 💻 | Qualidade e correção do código | `@instructions/personas/INSTRUCTIONS-REVISOR-PROGRAMADOR.md` |
| 2 | O Testador de Código ⚙️ | Execução e validação funcional dos exemplos | `@instructions/personas/INSTRUCTIONS-REVISOR-TESTADOR_DE_CODIGO.md` |
| 3 | O Professor 🎓 | Clareza e didática do conteúdo | `@instructions/personas/INSTRUCTIONS-REVISOR-PROFESSOR.md` |
| 4 | O Filósofo 🧘 | Profundidade ética e humana | `@instructions/personas/INSTRUCTIONS-REVISOR-FILOSOFO.md` |
| 5 | O Escritor ✍️ | Fluidez, ritmo e voz do autor | `@instructions/personas/INSTRUCTIONS-REVISOR-ESCRITOR.md` |
| 6 | O Poeta 🌙 | Leveza e conexão emocional | `@instructions/personas/INSTRUCTIONS-REVISOR-POETA.md` |
| 7 | O Historiador 📜 | Contextualização histórica da tecnologia | `@instructions/personas/INSTRUCTIONS-REVISOR-HISTORIADOR.md` |
| 8 | O Cientista 🧪 | Rigor científico e embasamento em fatos | `@instructions/personas/INSTRUCTIONS-REVISOR-CIENTISTA.md` |
| 9 | O Estatístico 📈 | Precisão de dados e métricas | `@instructions/personas/INSTRUCTIONS-REVISOR-ESTATISTICO.md` |
| 10 | O Cauteloso ⚠️ | Identificação de riscos e boas práticas | `@instructions/personas/INSTRUCTIONS-REVISOR-CAUTELOSO.md` |
| 11 | O Motivador 🔥 | Engajamento e apoio emocional ao leitor | `@instructions/personas/INSTRUCTIONS-REVISOR-MOTIVADOR.md` |
| 12 | O Irmão Mais Velho 🤝 | Conselhos práticos e mentoria | `@instructions/personas/INSTRUCTIONS-REVISOR-IRMAO_MAIS_VELHO.md` |
| 13 | O Palhaço 🤡 | Humor inteligente e alívio cômico | `@instructions/personas/INSTRUCTIONS-REVISOR-PALHACO.md` |
| 14 | O Ilustrador 🎨 | Visualização de conceitos em texto | `@instructions/personas/INSTRUCTIONS-REVISOR-ILUSTRADOR.md` |
| 15 | O Editor Markdown 📝 | Qualidade e consistência da formatação | `@instructions/personas/INSTRUCTIONS-REVISOR-EDITOR_MARKDOWN.md` |
| 16 | O Orador 🎤 | Clareza e fluidez para formatos de áudio | `@instructions/personas/INSTRUCTIONS-REVISOR-ORADOR.md` |
| 17 | O Contador de Casos 🧩 | Contextualização com estudos de caso | `@instructions/personas/INSTRUCTIONS-REVISOR-CONTADOR_DE_CASOS.md` |
| 18 | O Contador de Histórias 📚 | Humanização através de narrativas | `@instructions/personas/INSTRUCTIONS-REVISOR-CONTADOR_DE_HISTORIAS.md` |
| 19 | O Validador ✅ | Consistência técnica e padrões de mercado | `@instructions/personas/INSTRUCTIONS-REVISOR-VALIDADOR.md` |
| 20 | O Opinador 💬 | Coerência filosófica com a visão do autor | `@instructions/personas/INSTRUCTIONS-REVISOR-OPINADOR.md` |


---

## 🔄 SEQUÊNCIA RECOMENDADA DE REVISÃO

1. O Programador
2. O Testador de Código
3. O Validador
4. O Cientista
5. O Estatístico
6. O Cauteloso
7. O Professor
8. O Escritor
9. O Ilustrador
10. O Editor Markdown
11. O Filósofo
12. O Poeta
13. O Historiador
14. O Contador de Casos
15. O Contador de Histórias
16. O Motivador
17. O Irmão Mais Velho
18. O Palhaço
19. O Orador
20. O Opinador

> “Cada persona é uma camada de humanidade aplicada à técnica.”  
> — *Igor Medeiros*

---

## 🧩 INTEGRAÇÃO COM OUTROS MÓDULOS

| Fonte | Função |
|--------|---------|
| `@INSTRUCTIONS-CAPITULOS.md` | Define conteúdo base para revisão. |
| `@INSTRUCTIONS-HISTORIAS_AUTOR.md` | Fornece histórias e experiências pessoais para humanizar o texto. |
| `@INSTRUCTIONS-OPINIOES_VISAO_AUTOR.md` | Garante coerência filosófica e ética. |
| `@INSTRUCTIONS-LIVROS_BASE.md` | Alimenta as revisões do Cientista e do Estatístico com fontes científicas. |
| `@INSTRUCTIONS-FORMULAS.md` | Mantém a coerência estrutural de títulos e seções. |
| `@INSTRUCTIONS-POSICIONAMENTO.md` | Reforça consistência com a marca autoral e o propósito central (saúde e ética). |

---

## 🧪 YAML DE CONTROLE EDITORIAL

```yaml
tipo_documento: "revisao_multiperspectiva"
versao: 2.0
autor: "Igor Medeiros"
total_personas: 20
personas:
  - Programador
  - Testador de Código
  - Professor
  - Filósofo
  - Escritor
  - Poeta
  - Historiador
  - Cientista
  - Estatístico
  - Cauteloso
  - Motivador
  - Irmão Mais Velho
  - Palhaço
  - Ilustrador
  - Editor Markdown
  - Orador
  - Contador de Casos
  - Contador de Histórias
  - Validador
  - Opinador
dependencias:
  - @CAPITULOS.md
  - @HISTORIAS_AUTOR.md
  - @OPINIOES_VISAO_AUTOR.md
  - @LIVROS_BASE.md
  - @POSICIONAMENTO.md
status: "ativo"
atualizacao_sugerida: "trimestral"
````

---

## ✅ CHECKLIST FINAL

* [ ] As 20 personas estão descritas e atribuídas.
* [ ] O Cientista e o Estatístico garantem base científica e factual.
* [ ] Revisão cobre técnica, emoção, ética e estética.
* [ ] Integração com os demais módulos confirmada.
* [ ] Fluxo de revisão documentado e sequenciado.

---

> 💬 *“Um livro técnico sem revisão é código sem teste.
> E aqui, cada persona é um teste de humanidade.”*
> — *Igor Medeiros*