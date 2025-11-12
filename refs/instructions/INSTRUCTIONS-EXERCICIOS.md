<!-- instructions/INSTRUCTIONS-EXERCICIOS.md -->
# instructions/INSTRUCTIONS-EXERCICIOS.md
# 🧩 EXERCICIOS.md
> Template completo para **exercícios de múltipla escolha** e **desafio final prático (sem resposta)**.  
> Cada conjunto de exercícios é gerado com base na **pesquisa combinada (Internet + RAG local em `livros_base.md`)**,  
> validando os conceitos abordados no capítulo.

---

## 🎯 Objetivo
Consolidar o aprendizado técnico do leitor por meio de:
- Exercícios de múltipla escolha baseados no conteúdo do capítulo.  
- Correção comentada e referenciada.  
- Um **desafio prático final** para estimular pensamento crítico e aplicação real — **sem resposta pronta**.

---

## 🧱 Estrutura de Exercícios por Capítulo

| Tipo | Quantidade | Descrição |
|------|-------------|-----------|
| **Múltipla Escolha** | 5 | Questões de raciocínio e compreensão técnica, com quatro alternativas (a–d). |
| **Desafio Final** | 1 | Problema aberto e prático (sem resposta fornecida), integrando os aprendizados do capítulo. |

---

## ⚙️ Diretrizes Gerais

1. **Origem do Conteúdo:**  
   Cada questão deve combinar informações vindas da **Internet (documentações, artigos, tutoriais)** e do **RAG local (`livros_base.md`)**.

2. **Níveis de Dificuldade:**  
   - 🟦 *Júnior*: compreensão básica e execução direta.  
   - 🟨 *Pleno*: raciocínio aplicado e boas práticas.  
   - 🟥 *Sênior*: análise crítica, otimização e decisão arquitetural.

3. **Estilo de Escrita:**  
   - Didático, direto e amigável.  
   - Evite pegadinhas. Ensine enquanto avalia.  
   - Cada questão deve ter apenas **uma resposta correta** e **um comentário breve e educativo**.  

4. **Integração com Fontes:**  
   - Cada resposta deve mencionar pelo menos **uma fonte oficial (link ou livro-base)**.  
   - Quando a explicação for inspirada em livros, cite a página ou capítulo.

---

## 📘 Modelo de Exercícios (Capítulo Exemplo)

```markdown
# 🧩 Exercícios — Capítulo <NN>: <Título do Capítulo>

> Fontes: Internet + RAG local (`livros_base.md`)  
> Nível geral: 🟦 / 🟨 / 🟥  

---

### 🧠 Exercício 1 — (nível: 🟦 Júnior)
[PERGUNTA DO EXERCÍCIO 1]

```python
# [CÓDIGO DE EXEMPLO 1]
```

**a)** [ALTERNATIVA A]
**b)** [ALTERNATIVA B]
**c)** [ALTERNATIVA C]
**d)** [ALTERNATIVA D]

✅ **Resposta correta:** [LETRA DA RESPOSTA CORRETA]
🗒 **Comentário:** [COMENTÁRIO SOBRE A RESPOSTA]
📚 **Referência:** [REFERÊNCIA]

---

### 🧠 Exercício 2 — (nível: 🟨 Pleno)

[PERGUNTA DO EXERCÍCIO 2]

```python
# [CÓDIGO DE EXEMPLO 2]
```

**a)** [ALTERNATIVA A]
**b)** [ALTERNATIVA B]
**c)** [ALTERNATIVA C]
**d)** [ALTERNATIVA D]

✅ **Resposta correta:** [LETRA DA RESPOSTA CORRETA]
🗒 **Comentário:** [COMENTÁRIO SOBRE A RESPOSTA]
📚 **Fonte RAG local:** [REFERÊNCIA RAG LOCAL]

---

### 🧠 Exercício 3 — (nível: 🟨 Pleno)

[PERGUNTA DO EXERCÍCIO 3]

```python
# [CÓDIGO DE EXEMPLO 3]
```

**a)** [ALTERNATIVA A]
**b)** [ALTERNATIVA B]
**c)** [ALTERNATIVA C]
**d)** [ALTERNATIVA D]

✅ **Resposta correta:** [LETRA DA RESPOSTA CORRETA]
🗒 **Comentário:** [COMENTÁRIO SOBRE A RESPOSTA]
📚 **Referência:** [REFERÊNCIA]

---

### 🧠 Exercício 4 — (nível: 🟥 Sênior)

[PERGUNTA DO EXERCÍCIO 4]

**a)** [ALTERNATIVA A]
**b)** [ALTERNATIVA B]
**c)** [ALTERNATIVA C]
**d)** [ALTERNATIVA D]

✅ **Resposta correta:** [LETRA DA RESPOSTA CORRETA]
🗒 **Comentário:** [COMENTÁRIO SOBRE A RESPOSTA]
📚 **Fonte Web:** [REFERÊNCIA WEB]

---

### 🧠 Exercício 5 — (nível: 🟥 Sênior)

[PERGUNTA DO EXERCÍCIO 5]

**a)** [ALTERNATIVA A]
**b)** [ALTERNATIVA B]
**c)** [ALTERNATIVA C]
**d)** [ALTERNATIVA D]

✅ **Resposta correta:** [LETRA DA RESPOSTA CORRETA]
🗒 **Comentário:** [COMENTÁRIO SOBRE A RESPOSTA]
📚 **Referência:** [REFERÊNCIA]

---

### ⚙️ 💡 **Desafio Final (sem resposta)**

> [DESCREVA O ENUNCIADO COMPLETO DO DESAFIO FINAL]
>
> 💭 **Dica:** [DICA PARA O DESAFIO]
> 🧠 **Objetivo:** [OBJETIVO DO DESAFIO]
>
> ⚠️ Este desafio **não tem resposta fornecida** — incentive o leitor a experimentar, errar e comparar soluções.

````

---

## 🧠 Estrutura YAML (para automação / exportação)
> Modelo padrão para gerar automaticamente exercícios com explicações e desafios.

```yaml
- id: exercicio-<capitulo>-<numero>
  nivel: "junior|pleno|senior"
  tipo: "multipla_escolha"
  pergunta: "..."
  codigo_exemplo: "..."
  alternativas:
    a: "..."
    b: "..."
    c: "..."
    d: "..."
  resposta_correta: "..."
  comentario: "..."
  fontes:
    - origem: "internet"
      link: "https://docs.python.org/3/tutorial/"
    - origem: "livros_base.md"
      livro: "Fluent Python"
      capitulo: "Functions as Objects"
      paginas: [140, 145]

- id: desafio-<capitulo>
  tipo: "desafio_final"
  descricao: "Descreva o enunciado completo do desafio."
  nivel: "aberto"
  resposta_fornecida: false
  objetivo: "Estimular aplicação prática e pensamento criativo."
````

---

## 📈 Boas Práticas de Criação

* Mantenha **coerência entre código, pergunta e resposta**.
* Sempre explique *por que* a resposta é correta (não apenas *qual* é).
* Cite fontes sempre que possível (documentação oficial ou `livros_base.md`).
* Nos desafios, proponha **problemas abertos e realistas**, sem solução explícita.
* Evite trechos de código irrelevantes ou artificiais.
* Use a dificuldade como um **gradiente natural de aprendizado**: 🟦 → 🟨 → 🟥.

---

## ✅ Checklist de Qualidade

* [ ] 5 questões de múltipla escolha.
* [ ] 1 desafio prático **sem resposta**.
* [ ] Todas as questões revisadas por fontes web e RAG local.
* [ ] Cada explicação é didática, clara e fundamentada.
* [ ] O desafio final é inspirador e aberto à criatividade.
* [ ] Tom humano e motivador — o leitor sente que aprende com propósito.

---

> 💬 *“A prática não é o fim do aprendizado — é o momento em que ele ganha vida.”*
> — *Igor Medeiros*

```