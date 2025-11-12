<!-- instructions/INSTRUCTIONS-LIVROS_BASE.md -->
# instructions/INSTRUCTIONS-LIVROS_BASE.md
# 📚 LIVROS_BASE.md
> **Base Literária e Técnica do eBook**  
> Este documento orienta a pesquisa, curadoria e integração de fontes bibliográficas para embasar o conteúdo técnico e filosófico do eBook de Igor Medeiros.  
> Atua como camada de **RAG (Research Augmented Generation)**, combinando referências **clássicas, contemporâneas e aplicadas** à prática de IA e tecnologia na saúde.

---

## 🧭 FINALIDADE

O objetivo deste documento é garantir que cada capítulo do eBook seja fundamentado em **fontes sólidas e verificáveis**, combinando:
- **Pesquisa profunda na Internet** sobre os **5 livros mais importantes** do tema central.  
- **Consulta local** em materiais técnicos (PDFs, manuais e eBooks) armazenados no repositório do autor.  
- **Integração de resumos, críticas, trechos e citações** diretamente no contexto de escrita do eBook.  

> “A fonte é a raiz da credibilidade — e a busca é o adubo do pensamento.”  
> — *Igor Medeiros*

---

## ⚙️ FLUXO DE PESQUISA

### 1️⃣ Seleção dos 5 Livros-Chave
O agente pesquisador deve identificar **os 5 livros mais relevantes** sobre o tema principal do eBook (ex.: *IA na Saúde*, *LangChain na Prática*, *Agentes de IA*, *Deep Learning Médico*, etc.).  
Critérios:
- Alto volume de citações acadêmicas ou técnicas.  
- Reconhecimento em comunidades de desenvolvedores ou cientistas de dados.  
- Relevância prática para Python, IA, agentes e saúde.  

Os títulos e autores selecionados devem ser adicionados à seção `📘 LIVROS PRINCIPAIS`.

---

### 2️⃣ Pesquisa Ampliada na Internet
Para cada livro selecionado, realizar busca aprofundada contendo:
- **Resumos e sinopses oficiais.**  
- **Críticas e resenhas técnicas (Amazon, Goodreads, Papers with Code, ArXiv).**  
- **Artigos e entrevistas** com os autores.  
- **Discussões em comunidades (Reddit, Medium, Dev.to, Hacker News).**

Cada resultado deve ser sintetizado em formato resumido e adicionado ao contexto com:
```yaml
- titulo: <livro>
  resumo_sintetico: <síntese de 5 a 10 linhas>
  insights_chave: <principais ideias extraídas>
  opiniao_publica: <visão geral das críticas e impacto>
  aplicacao_no_ebook: <como o conteúdo influencia a escrita>
````

---

### 3️⃣ Integração Local — RAG

Em paralelo à pesquisa na Internet, o sistema deve:

* Buscar os livros ou materiais correspondentes em PDF na pasta local de eBooks.
* Indexar o conteúdo na **base vetorial (Supabase ou Chroma)**.
* Conectar trechos relevantes às seções do `CAPITULOS.md`.
* Marcar referências cruzadas com `@livro:<id>` para rastreabilidade.

> “Pesquisar é conversar com os gigantes — e aprender onde eles tropeçaram.”

---

### 4️⃣ Conexão com a Escrita

Durante a geração de cada capítulo:

* As fontes devem ser **citadas e sintetizadas**, não apenas referenciadas.
* O agente redator deve **incluir a essência das ideias dos autores** (por exemplo, Topol, Chollet, Russell, Bengio, Harrison Chase).
* A integração deve gerar **comentários contextuais e comparativos**, ligando as ideias dos livros à experiência pessoal de Igor Medeiros.

Exemplo:

> “Como destacou [AUTOR] em *[LIVRO]*, [CITAÇÃO RELEVANTE]. Essa visão se alinha à minha própria experiência ao desenvolver [TEMA DO EBOOK].”

---

### 1️⃣ Seleção dos 5 Livros-Chave
O agente pesquisador deve identificar **os 5 livros mais relevantes** sobre o tema principal do eBook (ex.: *IA na Saúde*, *LangChain na Prática*, *Agentes de IA*, *Deep Learning Médico*, etc.), **de acordo com o tema e título definidos em `@ebook/ESPECIFICACOES.md`**.
Critérios:
- Alto volume de citações acadêmicas ou técnicas.
- Reconhecimento em comunidades de desenvolvedores ou cientistas de dados.
- Relevância prática para Python, IA, agentes e saúde.

Os títulos e autores selecionados devem ser adicionados ao arquivo `@ebook/LIVROS_PESQUISADOS.md`, que começa zerado e é preenchido dinamicamente com esta lista.

---

### 2️⃣ Pesquisa Ampliada na Internet
Para cada livro selecionado, realizar busca aprofundada contendo:
- **Resumos e sinopses oficiais.**
- **Críticas e resenhas técnicas (Amazon, Goodreads, Papers with Code, ArXiv).**
- **Artigos e entrevistas** com os autores.
- **Discussões em comunidades (Reddit, Medium, Dev.to, Hacker News).**

Cada resultado deve ser sintetizado em formato resumido e adicionado ao contexto com:
```yaml
- titulo: <livro>
  resumo_sintetico: <síntese de 5 a 10 linhas>
  insights_chave: <principais ideias extraídas>
  opiniao_publica: <visão geral das críticas e impacto>
  aplicacao_no_ebook: <como o conteúdo influencia a escrita>
```


---

## 🧩 YAML DE CONTROLE EDITORIAL

```yaml
tipo_documento: "livros_base"
versao: 1.0
autor: "Igor Medeiros"
funcoes:
  - "definir fontes bibliográficas e técnicas"
  - "alimentar RAG local e pesquisas online"
  - "criar contexto de apoio para o Agente Redator"
ferramentas:
  - "web.search()"
  - "file_search.msearch()"
  - "RAG local (Supabase / Chroma)"
objetivo:
  - "combinar teoria, prática e filosofia autoral"
status: "em evolução contínua"
atualizacao_sugerida: "a cada novo eBook"
```

---

## ✅ CHECKLIST FINAL

* [ ] Os 5 livros principais foram identificados e resumidos.
* [ ] Pesquisas online e locais foram integradas.
* [ ] Cada livro contém resumo, crítica e aplicação prática.
* [ ] As citações estão conectadas aos capítulos correspondentes.
* [ ] O contexto foi atualizado no RAG local para uso futuro.

---

> 💬 *“Ler é viajar no tempo. Citar é voltar com bagagem.”*
> — *Igor Medeiros*

```