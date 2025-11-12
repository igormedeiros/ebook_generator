<!-- instructions/INSTRUCTIONS-CHECKLISTS.md -->
# instructions/INSTRUCTIONS-CHECKLISTS.md
# ✅ CHECKLISTS.md
> Template de **checklists práticos de aprendizado** ao final de cada capítulo.  
> Cada checklist deve ser gerado com base na **pesquisa híbrida (Internet + RAG local em `livros_base.md`)**,  
> validando que o leitor internalizou os conceitos centrais do capítulo.

---

## 🎯 Objetivo
Guiar o leitor na **autoavaliação consciente** do progresso técnico,  
garantindo que o aprendizado teórico se converta em **competência prática**.

O checklist serve como:
- Ferramenta de **reflexão ativa**.  
- Indicador de domínio técnico.  
- Síntese dos pontos essenciais antes de avançar ao próximo capítulo.

---

## ⚙️ Estrutura Recomendada
Cada capítulo deve terminar com um checklist estruturado em quatro blocos:

| Bloco | Propósito | Ícones Sugeridos |
|--------|------------|----------------|
| **Conceitos-Chave** | Verificar se entendeu a teoria. | 🧠 |
| **Aplicação Prática** | Garantir que testou os exemplos e entendeu resultados. | 💻 |
| **Boas Práticas** | Confirmar compreensão de padrões e recomendações. | 🧩 |
| **Integração com RAG local** | Reforçar o vínculo entre teoria (livros) e prática (web). | 📚 |

---

## 🧱 Template Padrão por Capítulo

```markdown
# ✅ Checklist — Capítulo <NN>: <Título do Capítulo>

> Fontes: Internet + RAG local (`livros_base.md`)  
> Nível do capítulo: 🟦 / 🟨 / 🟥

---

### 🧠 Conceitos-Chave
- [ ] Consigo explicar o conceito principal do capítulo em minhas próprias palavras.  
- [ ] Entendi os termos técnicos apresentados.  
- [ ] Consegui relacionar o tema deste capítulo com o anterior.  
- [ ] Identifiquei possíveis dúvidas para revisar depois.

---

### 💻 Aplicação Prática
- [ ] Executei todos os exemplos de código e compreendi os resultados.  
- [ ] Modifiquei o código para testar variações.  
- [ ] Comparei os resultados com explicações de fontes oficiais.  
- [ ] Criei uma mini-experiência própria com base no exemplo.

---

### 🧩 Boas Práticas e Design
- [ ] Apliquei princípios de legibilidade (PEP 8, Clean Code).  
- [ ] Entendi o motivo por trás das boas práticas apresentadas.  
- [ ] Identifiquei quando **não** usar determinada técnica.  
- [ ] Aprendi uma nova convenção que melhorou meu código.

---

### 📚 Integração com RAG Local
- [ ] Consultei o `livros_base.md` para reforçar o tema.  
- [ ] Encontrei pelo menos **um trecho relevante** nos PDFs locais.  
- [ ] Comparei a explicação do livro com a versão da Internet.  
- [ ] Adicionei uma anotação personal para lembrar do insight.

---

### 💬 Reflexão Final
> Escreva em uma linha o que mais te marcou neste capítulo:  
> ✍️ _________________________________________________  
>
> “O aprendizado real acontece quando a teoria encontra a prática e o significado pessoal.”
````

---

## 📘 Diretrizes para Criação de Checklists

1. **Personalização por Capítulo**

   * Cada checklist deve refletir o conteúdo específico do capítulo.
   * Evite repetições mecânicas.
   * Use o vocabulário do tema abordado.

2. **Abordagem Didática**

   * Use verbos de ação (“expliquei”, “executei”, “comparei”, “identifiquei”).
   * Mantenha tom encorajador e reflexivo.

3. **Integração Híbrida (Internet + RAG)**

   * Crie ao menos **uma pergunta associada ao conteúdo de `livros_base.md`**.
   * Incentive o leitor a validar aprendizados em fontes oficiais.

4. **Indicadores de Nível**

   * 🟦 Capítulos introdutórios: foco em sintaxe e compreensão conceitual.
   * 🟨 Capítulos intermediários: prática, experimentação e raciocínio aplicado.
   * 🟥 Capítulos avançados: abstração, refatoração e visão sistêmica.

---

## 🧩 Exemplo Concreto

```markdown
# ✅ Checklist — Capítulo <NN>: <Título do Capítulo Exemplo>

> Fontes: Internet + RAG local (`livros_base.md`)  
> Nível: 🟨 Pleno

### 🧠 Conceitos-Chave
- [ ] Consigo explicar o conceito principal do capítulo em minhas próprias palavras.  
- [ ] Entendi os termos técnicos apresentados.  
- [ ] Consegui relacionar o tema deste capítulo com o anterior.  

### 💻 Aplicação Prática
- [ ] Executei todos os exemplos de código e compreendi os resultados.  
- [ ] Modifiquei o código para testar variações.  
- [ ] Criei uma mini-experiência própria com base no exemplo.  

### 🧩 Boas Práticas
- [ ] Apliquei princípios de legibilidade (PEP 8, Clean Code).  
- [ ] Entendi o motivo por trás das boas práticas apresentadas.  
- [ ] Aprendi uma nova convenção que melhorou meu código.  

### 📚 Integração com RAG Local
- [ ] Consultei o `livros_base.md` para reforçar o tema.  
- [ ] Encontrei pelo menos **um trecho relevante** nos PDFs locais.  
- [ ] Comparei a explicação do livro com a versão da Internet.  

💬 “Percebi que [INSIRA UM INSIGHT PESSOAL AQUI].”
```

---

## 🧠 Automação e Metadados (YAML)

> Útil para geração automatizada e rastreabilidade de aprendizado.

```yaml
- id: checklist-<capitulo>
  titulo: "<título do capítulo>"
  nivel: "junior|pleno|senior"
  fontes:
    - origem: "internet"
      link: "https://docs.python.org/3/tutorial/"
    - origem: "livros_base.md"
      livro: "Fluent Python"
      capitulo: "Function Decorators and Closures"
      paginas: [185, 210]
  secoes:
    - nome: "Conceitos-Chave"
      itens:
        - "Expliquei o conceito principal com minhas palavras."
        - "Relacionei o tema com o capítulo anterior."
    - nome: "Aplicação Prática"
      itens:
        - "Executei e modifiquei os exemplos do texto."
        - "Comparei resultados com fontes oficiais."
    - nome: "Integração com RAG Local"
      itens:
        - "Consultei um trecho dos livros-base."
```

---

## ✅ Checklist do Autor (para revisão)

* [ ] Cada checklist está contextualizado com o capítulo.
* [ ] Inclui pelo menos 1 referência ao RAG local.
* [ ] Linguagem simples, positiva e instrutiva.
* [ ] Estimula reflexão, não apenas verificação.
* [ ] Formato compatível com automação YAML/Markdown.
* [ ] Mantém coerência entre teoria, prática e propósito.

---

> 💬 *“Aprender não é acumular — é perceber o que já se tornou parte de você.”*
> — *Igor Medeiros*

```