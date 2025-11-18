"""Semeia dados nas tabelas RAG do Supabase para o Ebook Generator 1.0.

O script alimenta as tabelas rag_author_* e rag_external com referências
derivadas de specs/book.yaml, garantindo que os agentes tenham contexto.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import yaml
from supabase import Client, create_client

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOK_SPEC_PATH = PROJECT_ROOT / "specs" / "book.yaml"
ENV_PATH = PROJECT_ROOT / ".env"
KB_PATH = PROJECT_ROOT / "kb"


def _load_env_file() -> None:
    """Carrega variáveis do arquivo .env quando presente."""

    if not ENV_PATH.exists():
        return
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _load_book_metadata() -> dict:
    """Carrega metadados do arquivo specs/book.yaml."""

    with BOOK_SPEC_PATH.open("r", encoding="utf-8") as handler:
        content: dict[str, Any] = yaml.safe_load(handler) or {}
    return content.get("metadata", {})


def _build_markdown_payloads() -> list[dict[str, Any]]:
    """Monta payloads a partir de todos os arquivos markdown dentro de kb/."""

    payloads = []

    if not KB_PATH.exists():
        return payloads

    for md_file in sorted(KB_PATH.rglob("*.md")):
        payloads.append({
            "source": str(md_file.relative_to(PROJECT_ROOT)),
            "content": md_file.read_text(encoding="utf-8"),
            "type": "markdown",
        })

    return payloads


def _build_author_payloads(author_name: str) -> tuple[list[dict[str, Any]], ...]:
    """Monta payloads para histórias, posicionamento e visão do autor."""

    stories = [
        {
            "author_name": author_name,
            "story": (
                "Quando o pai enfrentou demência precoce, Igor percebeu que o maior desafio "
                "não era a tecnologia em si, mas a falta de ferramentas para apoiar a relação "
                "humana entre equipes clínicas e famílias."
            ),
            "category": "familia",
            "tags": ["demencia", "familia", "empatia"],
        },
        {
            "author_name": author_name,
            "story": (
                "Durante um projeto hospitalar em Fortaleza, Igor conduziu squads de Python "
                "focados em LangChain para padronizar anotações clínicas e reduzir retrabalho "
                "dos médicos residentes."
            ),
            "category": "projeto_clinico",
            "tags": ["langchain", "python", "hospital"],
        },
        {
            "author_name": author_name,
            "story": (
                "Ao acompanhar Melissa, paciente de UTI, Igor viu como insights narrativos "
                "podem humanizar dashboards e decidiu dedicar a carreira a IA com propósito."
            ),
            "category": "historia_pessoal",
            "tags": ["humanizacao", "ia_com_proposito"],
        },
    ]

    positioning = [
        {
            "author_name": author_name,
            "positioning_statement": (
                "Especialista em agentes LangChain 1.0 aplicados à saúde, integrando sensores, "
                "EHRs e compliance ético em pipelines RAG."),
            "aspect": "autoridade_tecnica",
        },
        {
            "author_name": author_name,
            "positioning_statement": (
                "Defensor de IA responsável que coloca o paciente no centro e entrega "
                "ferramentas que amplificam, não substituem, o cuidado humano."),
            "aspect": "eticacompliance",
        },
        {
            "author_name": author_name,
            "positioning_statement": (
                "Mentor de times de engenharia que traduzem pesquisas médicas em produtos "
                "digitais com explicabilidade e governança."),
            "aspect": "lideranca",
        },
    ]

    vision = [
        {
            "author_name": author_name,
            "vision_or_opinion": (
                "Automação clínica precisa nascer com revisão humana obrigatória e trilhas de "
                "auditoria para cada decisão algorítmica."),
            "category": "eticaclinica",
            "principle": "responsabilidade_compartilhada",
        },
        {
            "author_name": author_name,
            "vision_or_opinion": (
                "Ferramentas de IA só escalam em hospitais quando reduzem carga cognitiva e "
                "libertam o profissional para interagir com o paciente."),
            "category": "experiencia_profissional",
            "principle": "humanizacao",
        },
        {
            "author_name": author_name,
            "vision_or_opinion": (
                "Ebooks técnicos precisam equilibrar rigor e acolhimento para que novos "
                "profissionais se sintam confiantes em ambientes críticos."),
            "category": "educacao",
            "principle": "didatica_empatica",
        },
    ]

    return stories, positioning, vision


def main() -> None:
    """Ponto de entrada principal para o script de semeadura."""

    _load_env_file()
    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

    if not url or not key:
        print("As variáveis de ambiente do Supabase não foram definidas.")
        return

    try:
        supabase: Client = create_client(url, key)
        print("Conexão com Supabase estabelecida.")

        metadata = _load_book_metadata()
        author_name = metadata.get("author", "Igor Medeiros")

        stories, positioning, vision = _build_author_payloads(author_name)
        markdown_payloads = _build_markdown_payloads()

        print(f"Semeando {len(stories)} histórias do autor...")
        supabase.table("rag_author_stories").upsert(stories).execute()

        print(f"Semeando {len(positioning)} declarações de posicionamento...")
        supabase.table("rag_author_positioning").upsert(positioning).execute()

        print(f"Semeando {len(vision)} declarações de visão...")
        supabase.table("rag_author_vision").upsert(vision).execute()

        if markdown_payloads:
            print(f"Semeando {len(markdown_payloads)} documentos markdown...")
            supabase.table("rag_external").upsert(markdown_payloads).execute()

        print("\\nSemeação concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante a semeação: {e}")


if __name__ == "__main__":
    main()
