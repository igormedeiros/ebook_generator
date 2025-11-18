import builtins
import contextlib
import os
import tempfile
import types
import unittest
from unittest.mock import mock_open, patch

@contextlib.contextmanager
def fake_docx_module(document_cls):
    original_import = builtins.__import__

    def _fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "docx":
            return types.SimpleNamespace(Document=document_cls)
        return original_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=_fake_import):
        yield


@contextlib.contextmanager
def missing_docx_module():
    original_import = builtins.__import__

    def _fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "docx":
            raise ImportError("module not available")
        return original_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=_fake_import):
        yield

from src.tools import (
    _init_supabase_client,
    search_knowledge_base,
    retrieve_rag_context,
    count_words,
    validate_content_quality,
    validate_structure,
    format_markdown,
    generate_amazon_optimized_title,
    validate_title_seo,
    generate_outline,
    perform_deep_research,
    vectorize_research,
    store_in_rag_external,
    retrieve_author_stories,
    retrieve_author_positioning,
    retrieve_author_vision,
    review_tone_and_engagement,
    review_clarity_and_empathy,
    review_grammar_and_style,
    review_logical_flow,
    review_code_examples,
    generate_cover,
    export_to_docx,
    export_to_epub,
    export_to_pdf,
    export_to_json,
    generate_kdp_metadata,
    replace_text_in_docx,
    send_epub_to_kindle,
    get_ideation_tools,
    get_finalization_tools,
    get_all_tools,
)

class TestTools(unittest.TestCase):

    def test_count_words(self):
        """Test the word count tool."""
        self.assertEqual(count_words("Hello world"), 2)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("One"), 1)

    def test_format_markdown(self):
        """Test the markdown formatting tool."""
        title = "My Title"
        content = "This is the content."
        expected_output = f"# {title}\n\n{content}\n\n---"
        self.assertEqual(format_markdown(title, content), expected_output)

    def test_validate_content_quality(self):
        """Test the content quality validation tool."""
        short_content = "This is short."
        long_content = "This is a much longer content that should pass the validation with a good score. " * 5
        result_short = validate_content_quality(short_content)
        result_long = validate_content_quality(long_content)

        self.assertEqual(result_short['status'], 'too_short')
        self.assertEqual(result_long['status'], 'valid')
        self.assertGreater(result_long['word_count'], 100)

    def test_validate_structure(self):
        """Test the outline structure validation tool."""
        valid_outline = {
            "chapters": [
                {"title": "Introduction", "estimated_words": 100},
                {"title": "Main Content", "estimated_words": 500},
                {"title": "Conclusion", "estimated_words": 100},
            ]
        }
        invalid_outline = {"chapters": [{"title": "Only one chapter"}]}
        
        result_valid = validate_structure(valid_outline)
        result_invalid = validate_structure(invalid_outline)

        self.assertTrue(result_valid['structure_valid'])
        self.assertFalse(result_invalid['structure_valid'])
        self.assertIn('No introduction chapter found', result_invalid['issues'])

    def test_generate_amazon_optimized_title(self):
        """Test the Amazon KDP title generation tool."""
        topic = "Python Programming"
        audience = "Beginners"
        title = generate_amazon_optimized_title(topic, audience)
        self.assertIn(topic, title)
        self.assertIn(audience, title)

    def test_validate_title_seo(self):
        """Test the title SEO validation tool."""
        short_title = "Short"
        long_title = "This is a very long title that will definitely exceed the maximum length allowed for an SEO optimized title and should fail the validation."
        good_title = "A Complete Guide to Python for Beginners"

        self.assertFalse(validate_title_seo(short_title)['min_length_ok'])
        self.assertFalse(validate_title_seo(long_title)['max_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['min_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['max_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['keyword_present'])

    def test_generate_outline(self):
        """Test the outline generation tool."""
        topic = "Test Topic"
        word_count = 10000
        text_outline, dict_outline = generate_outline(topic, word_count)

        self.assertIn(topic, text_outline)
        self.assertEqual(dict_outline['topic'], topic)
        self.assertEqual(len(dict_outline['chapters']), 5)
        self.assertEqual(dict_outline['target_words'], word_count)

    def test_get_ideation_tools(self):
        """Test that the ideation tools are returned correctly."""
        tools = get_ideation_tools()
        self.assertEqual(len(tools), 2)
        self.assertIn(search_knowledge_base, tools)
        self.assertIn(retrieve_rag_context, tools)

    def test_get_all_tools(self):
        """Test that all tools are returned."""
        tools = get_all_tools()
        self.assertGreater(len(tools), 20) # Check for a reasonable number of tools

    def test_get_finalization_tools_includes_email_sender(self):
        tools = get_finalization_tools()
        self.assertIn(send_epub_to_kindle, tools)

    @patch('src.tools.supabase_client', None)
    def test_search_knowledge_base_no_supabase(self):
        """Test RAG search when Supabase is not configured."""
        result = search_knowledge_base("test query")
        self.assertIn("Supabase not configured", result)

    @patch('src.tools.GoogleGenerativeAIEmbeddings')
    @patch('src.tools.supabase_client')
    def test_search_knowledge_base_with_supabase(self, mock_supabase_client, mock_embeddings):
        """Test RAG search with a mocked Supabase client."""
        mock_supabase_client.rpc.return_value.execute.return_value.data = [{'content': 'mock result'}]
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 768
        
        result = search_knowledge_base("test query")
        self.assertIn("Found 1 relevant documents", result)
        mock_supabase_client.rpc.assert_called_once()

    @patch('src.tools.search_knowledge_base')
    def test_retrieve_rag_context(self, mock_search):
        """Test the RAG context retrieval tool."""
        mock_search.return_value = "Mocked search result"
        context = retrieve_rag_context("test query", max_results=1)
        self.assertIn("Mocked search result", context)
        mock_search.assert_called_once_with("test query", max_results=1)

    @patch.dict("os.environ", {"SUPABASE_URL": "https://example", "SUPABASE_ANON_KEY": "key"}, clear=True)
    @patch("src.tools.create_client", return_value="client")
    def test_init_supabase_client_success(self, mock_create):
        client = _init_supabase_client()
        self.assertEqual(client, "client")
        mock_create.assert_called_once_with("https://example", "key")

    @patch.dict("os.environ", {"SUPABASE_URL": "https://example", "SUPABASE_ANON_KEY": "key"}, clear=True)
    @patch("src.tools.create_client", side_effect=RuntimeError("boom"))
    def test_init_supabase_client_handles_errors(self, mock_create):
        self.assertIsNone(_init_supabase_client())
        mock_create.assert_called_once()

    def test_search_knowledge_base_empty_query(self):
        self.assertEqual(search_knowledge_base(""), "Empty query provided")

    @patch("src.tools.GoogleGenerativeAIEmbeddings", None)
    @patch("src.tools.supabase_client")
    def test_search_knowledge_base_missing_embeddings(self, mock_client):
        mock_client.rpc.return_value.execute.return_value.data = []
        result = search_knowledge_base("topic")
        self.assertIn("Supabase search error", result)

def test_research_helpers_cover_branches():
    findings = perform_deep_research("IA", research_depth="avançado")
    assert findings["topic"] == "IA"
    assert findings["depth"] == "avançado"
    vectorized = vectorize_research(findings)
    assert vectorized["vectorized"] is True
    assert vectorized["findings_count"] == len(findings["findings"])
    stored = store_in_rag_external(vectorized, "IA")
    assert "Dados armazenados" in stored


def test_author_helpers_return_formatted_strings():
    stories = retrieve_author_stories("Ana", max_results=2)
    positioning = retrieve_author_positioning("Ana", max_results=1)
    vision = retrieve_author_vision("Ana", max_results=5)
    assert "Histórias" in stories and "Posicionamento" in positioning and "Visão" in vision


def test_review_helpers_return_expected_schema():
    content = "Parágrafo com insights"
    assert review_tone_and_engagement(content)["tone"] == "Apropriado"
    assert review_clarity_and_empathy(content)["clarity"] == "Claro"
    assert review_grammar_and_style(content)["style_score"] == 90
    assert review_logical_flow(content)["coherence_score"] == 88
    assert review_code_examples(content)["coverage"] == "Alta"


def test_generate_cover_and_simple_exports():
    assert "Capa gerada" in generate_cover("Titulo", "Sub", "Autor")
    assert export_to_epub("conteudo", "Titulo") == "Exportado para EPUB: Titulo.epub"
    assert export_to_pdf("conteudo", "Titulo") == "Exportado para PDF: Titulo.pdf"

    mocked_open = mock_open()
    with patch("builtins.open", mocked_open):
        message = export_to_json("conteudo", "Titulo", metadata={"lang": "pt"})
    assert "export_Titulo.json" in message
    mocked_open.assert_called_once_with("export_Titulo.json", "w", encoding="utf-8")


def test_generate_kdp_metadata_contains_language():
    metadata = generate_kdp_metadata("Titulo", "Autor")
    assert metadata == {"title": "Titulo", "author": "Autor", "language": "pt-BR"}


def test_export_to_docx_handles_missing_dependency():
    with missing_docx_module():
        message = export_to_docx("conteudo", "Titulo")
    assert message == "python-docx not installed"


def test_export_to_docx_writes_heading_and_paragraph():
    class RecordingDocument:
        instances = []

        def __init__(self):
            self.heading_calls = []
            self.paragraph_calls = []
            self.saved_file = None
            RecordingDocument.instances.append(self)

        def add_heading(self, title, level):
            self.heading_calls.append((title, level))

        def add_paragraph(self, content):
            self.paragraph_calls.append(content)

        def save(self, filename):
            self.saved_file = filename

    with fake_docx_module(RecordingDocument):
        message = export_to_docx("texto", "Titulo")

    assert "export_Titulo.docx" in message
    doc = RecordingDocument.instances[-1]
    assert doc.heading_calls == [("Titulo", 0)]
    assert doc.paragraph_calls == ["texto"]
    assert doc.saved_file == "export_Titulo.docx"


def test_replace_text_in_docx_successfully_updates_text():
    class ReplaceDocument:
        instances = []

        def __init__(self, _path):
            paragraph = types.SimpleNamespace(text="Olá [NOME]")
            cell = types.SimpleNamespace(text="[NOME] na tabela")
            row = types.SimpleNamespace(cells=[cell])
            table = types.SimpleNamespace(rows=[row])
            self.paragraphs = [paragraph]
            self.tables = [table]
            self.saved = None
            ReplaceDocument.instances.append(self)

        def save(self, filename):
            self.saved = filename

    with fake_docx_module(ReplaceDocument):
        message = replace_text_in_docx(
            "entrada.docx", "saida.docx", {"[NOME]": "Alice"}
        )

    assert "saida.docx" in message
    doc = ReplaceDocument.instances[-1]
    assert doc.paragraphs[0].text == "Olá Alice"
    assert doc.tables[0].rows[0].cells[0].text == "Alice na tabela"
    assert doc.saved == "saida.docx"


def test_replace_text_in_docx_import_error():
    with missing_docx_module():
        message = replace_text_in_docx("entrada.docx", "saida.docx", {"a": "b"})
    assert message == "python-docx not installed"


def test_replace_text_in_docx_handles_processing_error():
    class ExplodingDocument:
        def __init__(self, *_args, **_kwargs):
            pass

        def save(self, filename):
            raise RuntimeError("boom")

    with fake_docx_module(ExplodingDocument):
        message = replace_text_in_docx("entrada.docx", "saida.docx", {"a": "b"})

    assert "Erro ao processar" in message


class TestSendEpubToKindle(unittest.TestCase):

    def _create_epub_file(self):
        handle = tempfile.NamedTemporaryFile(suffix=".epub", delete=False)
        handle.write(b"conteudo de teste")
        handle.flush()
        handle.close()
        self.addCleanup(lambda: os.path.exists(handle.name) and os.remove(handle.name))
        return handle.name

    def test_missing_file_returns_message(self):
        message = send_epub_to_kindle("/tmp/inexistente.epub", "user@kindle.com")
        self.assertIn("não encontrado", message)

    def test_missing_kindle_email(self):
        epub_path = self._create_epub_file()
        message = send_epub_to_kindle(epub_path, kindle_email="")
        self.assertEqual(message, "E-mail do Kindle não configurado")

    @patch("src.tools.smtplib.SMTP")
    @patch.dict(
        "os.environ",
        {
            "KINDLE_SMTP_USER": "sender@gmail.com",
            "KINDLE_SMTP_PASSWORD": "secret",
        },
        clear=True,
    )
    def test_successful_send_uses_smtp(self, mock_smtp):
        epub_path = self._create_epub_file()
        smtp_conn = mock_smtp.return_value.__enter__.return_value
        message = send_epub_to_kindle(epub_path, kindle_email="reader@kindle.com")
        self.assertIn("EPUB enviado", message)
        smtp_conn.starttls.assert_called_once()
        smtp_conn.login.assert_called_once_with("sender@gmail.com", "secret")
        smtp_conn.send_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()