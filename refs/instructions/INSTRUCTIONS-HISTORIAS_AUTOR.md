<!-- instructions/INSTRUCTIONS-HISTORIAS_AUTOR.md -->
# instructions/INSTRUCTIONS-HISTORIAS_AUTOR.md
# 📖 INSTRUCTIONS-HISTORIAS_AUTOR.md
> **Catálogo de Histórias Pessoais do Autor**  
> Documento de referência para as personas *Contador de Histórias*, *Poeta*, *Filósofo* e *Motivador*.  
> Usado para enriquecer os capítulos com narrativas pessoais, metáforas, analogias e inspirações reais.  

---

## 🧭 Finalidade
Este arquivo funciona como um **repositório local de histórias** do autor, estruturadas por **categoria temática**.  
Cada história deve conter:
- Contexto histórico e emocional.  
- Desfecho (resultado e aprendizado).  
- Moral (lição central).  
- Tags para classificação semântica (usadas por agentes e RAG local).

As histórias podem ser:
- Citadas integralmente (em capítulos reflexivos ou motivacionais).  
- Parafraseadas como analogias (em capítulos técnicos).  
- Referenciadas como estudos de caso pessoais.  

---

## 🧱 Estrutura do Documento

Cada história deve seguir este padrão:

```yaml
- categoria: <tema macro>
  titulo: <título narrativo>
  ano: <ano ou período aproximado>
  historia: <descrição textual e envolvente>
  desfecho: <resultado emocional e prático>
  moral: <lição aprendida>
  tags: [#palavra1, #palavra2, ...]
```

---

## 🗂️ Catálogo de Histórias

> 🔸 **Nota:** Adicione aqui as histórias que serão usadas no ebook. Elas podem ser adaptadas para contexto técnico, filosófico ou motivacional conforme a necessidade.

[ADICIONE AQUI AS HISTÓRIAS DO AUTOR, SEGUINDO O FORMATO YAML ACIMA]

---

## 🔍 YAML de Controle para RAG Local

```yaml
indexacao:
  tipo: "historias_autor"
  embeddings: "local"
  formato: "md"
  colecao: "histórias"
  campos_chave:
    - titulo
    - categoria
    - moral
    - tags
```

---

## 🧩 Recomendações de Uso

* As histórias podem ser **usadas como analogias narrativas** em capítulos técnicos.
* O *Historiador* pode referenciar o contexto histórico.
* O *Poeta* pode extrair metáforas.
* O *Motivador* pode usá-las como **inspirações diretas** nos encerramentos de capítulos.

---

## ✅ Checklist de Integridade

* [ ] Todas as histórias categorizadas.
* [ ] Tags uniformes e legíveis.
* [ ] Narrativas completas com desfecho e moral.
* [ ] Prontas para consulta semântica via RAG local.

---