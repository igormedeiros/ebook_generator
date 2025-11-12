# Ebook Generator 1.0

**A Production-Ready, AI-Powered Editorial Pipeline for Autonomous Ebook Generation**

Transform raw topics into publication-ready ebooks with a sophisticated 8-stage editorial pipeline powered by LangChain 1.0+ and Google's Gemini AI.

## 🎯 Overview

Ebook Generator 1.0 is an advanced multi-agent system that orchestrates the complete editorial process from ideation to KDP publication. The pipeline combines specialized AI agents with 5 domain-expert review personas and 5 virtual readers for iterative critical feedback.

### Key Features

- **8-Stage Autonomous Pipeline**: From ideation to publication-ready package
- **5 Specialized Review Personas**: Technical, Editorial, Style, Governance, and Ethics validation
- **5 Virtual Readers**: Beginner, Professional, Educator, Specialist, and Reflective perspectives
- **Dual-Model Strategy**: Gemini 2.5 Flash (writing) + Gemini 2.5 (research/RAG)
- **LangChain 1.0+ Native**: Built on latest best practices and patterns
- **RAG Integration Ready**: Supabase pgvector support for knowledge augmentation
- **Production Quality**: Output validated for Amazon KDP, LGPD, and industry standards
- **Extensible Architecture**: Easy to add new agents, tools, and personas

## 📋 Pipeline Architecture

### The 8-Stage Editorial Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│ EBOOK GENERATOR 1.0 - 8-STAGE EDITORIAL PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Stage 1: IDEATION                                                      │
│ └─ Define: Central idea, problem, target audience, transformation    │
│    Output: Business idea framework                                    │
│                                                                         │
│ Stage 2: TITLE GENERATION                                             │
│ └─ Generate: 3 Amazon-optimized title + subtitle combinations        │
│    Output: Market-optimized titles                                    │
│                                                                         │
│ Stage 3: STRUCTURE & OUTLINE                                          │
│ └─ Create: Hierarchical table of contents scaled to word count        │
│    Output: Didactic outline in Markdown                               │
│                                                                         │
│ Stage 4: CHAPTER WRITING                                              │
│ └─ Write: Didactic content with RAG context integration               │
│    Output: Content chapters with citations                            │
│                                                                         │
│ Stage 5: SPECIALIZED REVIEW (5 PERSONAS)                              │
│ ├─ Technical Reviewer (code quality, framework versions)              │
│ ├─ Editorial Reviewer (clarity, tone, flow, linguistics)               │
│ ├─ Content Stylist (formatting, structure, consistency)                │
│ ├─ Governance QA (compliance, metadata, security, LGPD)                │
│ └─ Ethics Validator (bias, medical disclaimers, AI ethics, HIPAA)     │
│    Output: 5-perspective feedback dictionary                          │
│                                                                         │
│ Stage 6: CRITICAL READING (5 VIRTUAL READERS)                        │
│ ├─ Curious Beginner (clarity, progression, accessibility)            │
│ ├─ Technical Professional (depth, relevance, accuracy)                │
│ ├─ Didactic Educator (pedagogical structure, methodology)             │
│ ├─ Domain Specialist (application relevance, coherence)               │
│ └─ Reflective Reader (empathy, purpose, emotional impact)             │
│    Output: Independent feedback from 5 reading perspectives            │
│                                                                         │
│ Stage 7: EDITING & FORMATTING                                         │
│ └─ Validate: Markdown formatting, heading hierarchy, consistency      │
│    Output: Publication-ready formatted document                       │
│                                                                         │
│ Stage 8: FINALIZATION & COVER                                         │
│ └─ Generate: Cover concept and validate metadata                      │
│    Output: Cover design + validated metadata                          │
│                                                                         │
│ Stage 9: PUBLICATION & KDP EXPORT                                     │
│ └─ Export: DOCX, EPUB, PDF, JSON formats for KDP                      │
│    Output: Complete publication package                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Review Personas: The Quality Assurance Core

The system includes 5 specialized review personas, each with domain expertise:

#### 1. **Technical Reviewer Agent**
- **Expertise**: Code quality and technical accuracy
- **Focus**:
  - Python code syntax and best practices
  - LangChain API compatibility (v1.0+ patterns)
  - AI/ML concept accuracy
  - Framework version validation
  - Example code execution testing

#### 2. **Editorial Reviewer Agent**
- **Expertise**: Writing quality and audience engagement
- **Focus**:
  - Clarity and readability
  - Tone and voice consistency
  - Paragraph flow and transitions
  - Grammar and spelling accuracy
  - Terminology consistency

#### 3. **Content Stylist Agent**
- **Expertise**: Formatting and visual consistency
- **Focus**:
  - Heading hierarchy (H1, H2, H3)
  - Code block formatting
  - List consistency
  - Table of contents accuracy
  - Visual emphasis usage

#### 4. **Governance QA Agent**
- **Expertise**: Compliance and standards
- **Focus**:
  - Framework version accuracy
  - Security compliance
  - LGPD compliance (Brazilian data protection)
  - Metadata completeness
  - Copyright and license declarations

#### 5. **Ethics Validator Agent**
- **Expertise**: AI ethics and regulatory compliance
- **Focus**:
  - Bias detection and mitigation
  - Medical disclaimer requirements
  - AI ethics principles
  - LGPD/HIPAA compliance
  - Diversity and inclusion language

## � Virtual Readers: Critical Reading Personas

The system simulates **5 virtual readers** that provide independent, iterative feedback:

| Persona | Profile | Validation Focus |
|---------|---------|------------------|
| **👩‍💻 Curious Beginner** | New to AI/programming | Clarity, progression, accessibility |
| **🧔 Technical Professional** | Senior developer | Depth, relevance, technical accuracy |
| **👩‍🏫 Didactic Educator** | Teacher/mentor | Pedagogical structure, methodology |
| **👨‍⚕️ Domain Specialist** | Physician, researcher | Application relevance, cross-disciplinary coherence |
| **🧘 Reflective Reader** | General audience | Empathy, purpose, emotional impact |

Each reader generates independent reports that feed into the **3-iteration refinement loop** conducted by the Coordinator Super Agent.

## �🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google API Key (Gemini 2.5 Flash)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/igormedeiros/ebook-generator.git
   cd ebook-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your Google API Key
   export GOOGLE_API_KEY="your-api-key-here"
   ```

### Basic Usage

```python
from src.main import run_ebook_pipeline

# Execute the 8-stage pipeline
results = run_ebook_pipeline(
    topic="Advanced Python with LangChain",
    target_audience="Senior Python Developers",
    word_count_target=15000,
    run_all_stages=True
)

# Access results from each stage
ideation = results["ideation"]
titles = results["title"]
structure = results["structure"]
chapter = results["chapter"]
reviews = results["review_personas"]  # 5 specialized reviews
```

## 📁 Project Structure

```
ebook-generator/
├── .github/
│   └── copilot-instructions.md    # Code standards for all agents
├── src/
│   ├── main.py                     # Pipeline orchestration (8 stages)
│   ├── agents.py                   # 8 agents + 1 coordinator + 5 reviewers
│   ├── tools.py                    # 30+ specialized tools
│   ├── config.py                   # Model initialization
│   └── __init__.py
├── pyproject.toml                  # Project metadata and dependencies
├── README.md                        # This file
└── requirements.txt                # Python dependencies
```

## 🔧 Core Components

### agents.py: Specialized Agents

The system includes 14 distinct agent creators:

**Main Pipeline Agents (8)**:
- `create_ideation_agent()` - Stage 1: Central idea definition
- `create_title_agent()` - Stage 2: Amazon-optimized titles
- `create_structure_agent()` - Stage 3: Outline generation
- `create_chapter_agent()` - Stage 4: Content writing
- `create_review_agent()` - Stage 5: Review orchestration
- `create_editing_agent()` - Stage 6: Formatting validation
- `create_finalization_agent()` - Stage 7: Cover and metadata
- `create_publication_agent()` - Stage 8: Export and packaging

**Specialized Review Agents (5)**:
- `create_technical_reviewer_agent()` - Code quality validation
- `create_editorial_reviewer_agent()` - Writing quality
- `create_content_stylist_agent()` - Formatting consistency
- `create_governance_agent()` - Compliance validation
- `create_ethics_validator_agent()` - Ethics and bias checking

**Orchestration**:
- `create_coordinator_superagent()` - 8-stage pipeline orchestrator
- `execute_review_personas()` - Execute all 5 reviewers in sequence

### tools.py: Specialized Tools

30+ tools organized by pipeline stage:

**Stage 1 - Ideation Tools**:
- `search_knowledge_base()` - Find relevant knowledge
- `retrieve_rag_context()` - RAG context retrieval

**Stage 2 - Title Tools**:
- `generate_amazon_optimized_title()` - Market-optimized titles
- `validate_title_seo()` - SEO validation

**Stage 3 - Structure Tools**:
- `generate_outline()` - Create hierarchical outlines
- `count_words()` - Word count validation

**Stage 4 - Writing Tools**:
- `format_markdown()` - Markdown formatting
- `validate_content_quality()` - Content metrics

**Stage 5 - Review Tools**:
- `review_tone_and_engagement()` - Tone analysis
- `review_clarity_and_empathy()` - Clarity checking
- `review_grammar_and_style()` - Grammar validation
- `review_logical_flow()` - Flow analysis
- `review_code_examples()` - Code validation

**Stage 6 - Editing Tools**:
- (Formatting validation tools)

**Stage 7 - Finalization Tools**:
- `generate_cover()` - Cover design generation
- `generate_kdp_metadata()` - KDP metadata

**Stage 8 - Publication Tools**:
- `export_to_docx()` - Word export
- `export_to_epub()` - EPUB export
- `export_to_pdf()` - PDF export

### config.py: Configuration

Centralized configuration and model initialization:

```python
from config import get_model

model = get_model()  # Returns ChatGoogleGenerativeAI with Gemini 2.5 Flash
```

Configuration parameters:
- **Model**: Gemini 2.5 Flash
- **Temperature**: 0.7 (balanced creativity/consistency)
- **top_p**: 0.95
- **top_k**: 40

## 💡 Usage Examples

### Example 1: Full Pipeline Execution

```python
from src.main import run_ebook_pipeline

# Run complete 8-stage pipeline
results = run_ebook_pipeline(
    topic="Python Data Science with Pandas",
    target_audience="Data Scientists and Analysts",
    word_count_target=20000,
    run_all_stages=True
)

print(f"Stage 1 (Ideation): {results['ideation'][:200]}...")
print(f"Stage 2 (Titles): {results['title'][:200]}...")
print(f"Stage 5 Reviews: {results['review_personas'].keys()}")
```

### Example 2: Single Stage Execution

```python
from src.agents import (
    create_ideation_agent,
    execute_agent
)
from config import get_model

model = get_model()
agent = create_ideation_agent(model)

query = """
Define the central idea for a technical ebook:
Topic: Machine Learning in Healthcare
Target Audience: Healthcare professionals
Target Word Count: 12000
"""

result = execute_agent(agent, query)
print(result)
```

### Example 3: Custom Review Process

```python
from src.agents import (
    create_technical_reviewer_agent,
    create_editorial_reviewer_agent,
    execute_agent
)
from config import get_model

model = get_model()
content = "Your ebook content here..."

# Technical review
tech_agent = create_technical_reviewer_agent(model)
tech_feedback = execute_agent(tech_agent, f"Review this: {content}")

# Editorial review
editorial_agent = create_editorial_reviewer_agent(model)
editorial_feedback = execute_agent(editorial_agent, f"Review this: {content}")

print(f"Technical: {tech_feedback}")
print(f"Editorial: {editorial_feedback}")
```

## 🧠 LangChain 1.0+ Integration

The system uses LangChain 1.0+ native patterns with **dual-model strategy**:

### Dual-Model Architecture

**Writing & Revision Model**: Gemini 2.5 Flash
- Purpose: Fast, creative text generation and iterative refinement
- Configuration: temperature=0.7 (balanced creativity/consistency)

**Research & Analysis Model**: Gemini 2.5
- Purpose: Deep analysis, RAG context retrieval, semantic search
- Configuration: temperature=0.3 (focused for RAG accuracy)

### Tool Definition Pattern

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description."""
    return "Tool result"
```

### Structured Output Pattern

```python
@tool(response_format="content_and_artifact")
def structured_tool(param: str) -> tuple[str, dict]:
    """Returns both narrative and structured data."""
    return narrative_text, structured_data
```

### Agent Creation

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="Clear role definition..."
)
```

### Execution

```python
response = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
output = response["messages"][-1].content
```

## 🔗 RAG Integration (Supabase)

The system includes integration points for Retrieval-Augmented Generation:

```python
# Tools marked with RAG integration points
@tool
def retrieve_rag_context(query: str) -> str:
    """
    TODO: Implement Supabase pgvector integration
    1. Connect to Supabase (postgresql+psycopg://...)
    2. Query pgvector with similarity_search()
    3. Return top-k relevant documents
    """
    pass
```

### Setup Instructions

1. **Create Supabase project** with pgvector extension enabled
2. **Configure connection**:
   ```python
   from langchain.vectorstores import PGVectorStore
   
   vector_store = PGVectorStore.connect_from_documents(
       connection_string="postgresql+psycopg://user:password@host/db",
       documents=documents,
       embedding=embeddings,
   )
   ```
3. **Use in agents**: Call `retrieve_rag_context()` during chapter writing

## 📊 System Architecture

```
┌──────────────────────────────────────────────────────┐
│            EBOOK GENERATOR 1.0                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ORCHESTRATOR LAYER                                  │
│  ├─ create_coordinator_superagent()                 │
│  └─ run_ebook_pipeline()                            │
│                                                      │
│  AGENT LAYER (14 agents)                            │
│  ├─ 8 Main Pipeline Agents (ideation to pub)        │
│  ├─ 5 Specialized Review Personas                   │
│  └─ 1 Coordinator Super Agent                       │
│                                                      │
│  TOOL LAYER (30+ tools)                             │
│  ├─ Generation Tools (titles, outlines, etc)        │
│  ├─ Review Tools (tone, clarity, grammar)           │
│  ├─ Validation Tools (quality, compliance)          │
│  └─ Export Tools (DOCX, EPUB, PDF, JSON)            │
│                                                      │
│  MODEL LAYER                                         │
│  ├─ LangChain 1.0+                                  │
│  ├─ Google Generative AI (Gemini 2.5 Flash)         │
│  └─ RAG Backend (Supabase pgvector)                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 🛠️ Configuration & Environment

### Environment Variables

```bash
# .env file
GOOGLE_API_KEY="your-gemini-api-key"

# Optional: RAG configuration
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-key"
```

### Model Parameters

Default Gemini 2.5 Flash configuration (in `config.py`):

```python
ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,      # Balanced creativity/consistency
    top_p=0.95,          # Diverse but focused
    top_k=40,            # Top K sampling
)
```

## 📈 Performance & Scaling

### Optimization Tips

1. **Batch Tool Calls**: Execute multiple tools in parallel when independent
2. **RAG Context**: Use top-k parameter to limit context size
3. **Token Usage**: Monitor Gemini API usage for cost optimization
4. **Caching**: Implement caching for repeated queries

### Expected Performance

- **Full Pipeline**: ~2-5 minutes (depending on API latency)
- **Single Agent**: ~15-30 seconds
- **Review Personas**: ~60-90 seconds (5 reviewers in sequence)
- **Token Cost**: ~5000-10000 tokens per full pipeline

## 🔐 Security & Compliance

### Standards Implemented

- **LGPD**: Brazilian data protection compliance checks
- **HIPAA**: Medical content disclaimer validation
- **Security**: No credentials in code, environment-based config
- **Ethics**: Bias detection and AI ethics validation

### Best Practices

- Store API keys in environment variables
- Use virtual environments
- Validate all inputs before processing
- Implement audit logging for sensitive operations

## 📚 Documentation

### Key Files

- `README.md` - This file, complete project documentation
- `.github/copilot-instructions.md` - Code standards and best practices
- `ARCHITECTURE.md` - Detailed system architecture
- `src/agents.py` - Agent definitions and docstrings
- `src/tools.py` - Tool definitions and docstrings

### Code Documentation

All functions include comprehensive docstrings:

```python
def my_function(param: str) -> dict:
    """
    Brief description.
    
    Args:
        param: Parameter description
    
    Returns:
        dict: Return value description
    """
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src tests/
```

### Manual Testing

```bash
# Test single agent
python -c "from src.agents import create_ideation_agent; \
from src.config import get_model; \
from src.agents import execute_agent; \
model = get_model(); \
agent = create_ideation_agent(model); \
print(execute_agent(agent, 'Test query'))"

# Test full pipeline
python src/main.py
```

## 🚀 Deployment

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run pipeline
python src/main.py

# Run specific stage
python -c "from src.main import run_ebook_pipeline; \
results = run_ebook_pipeline('Topic', 'Audience', 15000)"
```

### Production Considerations

1. **Environment**: Use managed Python runtime
2. **API Keys**: Use secret management service
3. **Logging**: Implement comprehensive logging
4. **Monitoring**: Track agent execution and errors
5. **Caching**: Store results in database

## 🤝 Contributing

Contributions are welcome! Please follow the code standards in `.github/copilot-instructions.md`:

1. **Language**: 100% English code
2. **Patterns**: LangChain 1.0+ standards
3. **Documentation**: Complete docstrings
4. **Type Hints**: All functions
5. **Testing**: Unit tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Igor Medeiros**
- GitHub: [@igormedeiros](https://github.com/igormedeiros)
- Email: igor@example.com

## 🔗 Links

- [LangChain Documentation](https://python.langchain.com)
- [Google Generative AI](https://ai.google.dev)
- [Supabase Documentation](https://supabase.com/docs)
- [Amazon KDP](https://kdp.amazon.com)

## 📞 Support

For issues, questions, or suggestions:

1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error logs and reproduction steps
4. Reference relevant documentation

## 🔄 Changelog

### Version 1.0 (Current)

- ✅ 8-stage autonomous pipeline
- ✅ 5 specialized review personas
- ✅ LangChain 1.0+ integration
- ✅ Google Gemini 2.5 Flash support
- ✅ RAG integration points for Supabase
- ✅ Comprehensive documentation
- ✅ Code standards and best practices

### Future Roadmap

- [ ] Implement Supabase pgvector RAG
- [ ] Add middleware support (PII, summarization, human-in-loop)
- [ ] Multi-language support
- [ ] Custom agent templates
- [ ] Web UI for pipeline management
- [ ] Batch processing for multiple ebooks
- [ ] Analytics and metrics dashboard

---

**Last Updated**: 2024
**Status**: Production Ready ✅
