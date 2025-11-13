# PRD – Automated eBook Generator

**Ebook Generator 1.0 - AI-Powered Editorial Automation Platform**

**Status:** Active Development  
**Last Updated:** November 13, 2025  
**Version:** 1.0

---

## 1. Objective

Build an automated ebook generation system integrating Python, LangChain 1.0, Google Gemini 2.5 Flash (fast editorial writing) and Gemini 2.5 Pro (deep research/RAG), capable of creating customized digital books, reviewed through a multi-agent approach, with ingestion and use of the author's personal stories and opinions.

### Business Objectives

- **Reduce editorial production time** by ≥80% compared to traditional workflows
- **Achieve ≥95% factual accuracy** via RAG integration and validation
- **Ensure 100% Amazon KDP compatibility** for direct publication
- **Maintain ≥90% user satisfaction** through quality review and iteration

---

## 2. Main Functionalities

### Flexible Input with Validation
- User provides book specification in `input/book_input.yaml` with mandatory fields:
  - `topic` (string): Main topic
  - `target_audience` (string): Target audience description
  - `word_count_target` (integer): Desired word count
- The system validates the input and prompts the user for missing information.

### 9-Stage Editorial Pipeline
1.  **Ideation**: Defines the central idea, problem, and audience.
2.  **Title Generation**: Creates 3 Amazon-optimized title options.
3.  **Structure**: Generates a hierarchical table of contents.
4.  **Deep Research & Chapter Writing**:
    -   **4A. Deep Research**: Gathers and vectorizes external knowledge.
    -   **4B. Chapter Writing**: Writes chapters using the research.
5.  **Specialized Review**: 10 specialized personas review the content.
6.  **Critical Reading & Iteration**: 5 virtual readers provide feedback in 3 cycles.
7.  **Editing**: Finalizes formatting and validation.
8.  **Finalization**: Generates a cover concept and metadata.
9.  **Publication**: Exports the ebook to DOCX, EPUB, PDF, and JSON.

### Dual-Model Architecture
- **Gemini 2.5 Flash**: For creative writing, reviews, and summaries.
- **Gemini 2.5 Pro**: For research, analysis, and factual validation.

### RAG Integration
- **Author Knowledge**: Pre-loaded author stories, positioning, and vision.
- **External Research**: Deep research results vectorized during the pipeline.

### Multi-Persona Review and Iteration
- **10 Review Personas**: Provide specialized feedback on the content.
- **5 Virtual Readers**: Simulate different reader profiles for iterative improvement.

### Export and Publication
- Automatic conversion to DOCX, EPUB, PDF, and JSON.
- Assistance in generating inputs for KDP publication.

---

## 3. Technical Specifications

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Python | 3.11+ |
| **AI Orchestration** | LangChain | 1.0+ |
| **Writing Model** | Gemini 2.5 Flash | Latest |
| **Research Model** | Gemini 2.5 Pro | Latest |
| **Vector Storage** | Supabase + pgvector | Latest |
| **Export** | Pandoc | 3.0+ |

### Model Configuration

**Gemini 2.5 Flash (Fast Writing)**
- Temperature: 0.7
- top_p: 0.95
- top_k: 40

**Gemini 2.5 Pro (Deep Research)**
- Temperature: 0.3
- top_p: 0.95
- top_k: 40

---

## 4. Success Metrics

### Speed
- **Execution Time**: 2-5 minutes for a complete pipeline.
- **Relative Reduction**: ≥80% vs. manual flow.

### Quality
- **Factual Accuracy**: ≥95% via RAG + validation.
- **KDP Compatibility**: 100% (zero rejections).
- **User Satisfaction**: ≥90%.

### Technical
- **API Availability**: ≥99.5% uptime.
- **Error Rate**: <1% failed executions.

---

## 5. User Stories

### User Story 1: Complete Pipeline Execution
**As a** publisher,
**I want to** execute a full 9-stage pipeline from topic to publication,
**So that** I can produce a complete ebook in minimal time.

### User Story 2: Quality Assurance Through Review Personas
**As a** quality manager,
**I want to** receive feedback from 10 specialized review perspectives,
**So that** I can ensure multi-dimensional quality.

### User Story 3: Iterative Improvement Through Virtual Readers
**As a** content team lead,
**I want to** receive feedback from 5 diverse reader perspectives across 3 iterations,
**So that** I can continuously improve content quality.

---

## 6. Non-Functional Requirements

- **Performance**: The full pipeline should execute in under 5 minutes.
- **Scalability**: The system should support batch processing for multiple ebooks.
- **Reliability**: The system should have robust error handling and retry logic.
- **Security**: API keys should be managed via environment variables.
- **Compliance**: The system should be compliant with LGPD, HIPAA, and KDP standards.