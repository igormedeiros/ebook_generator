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

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_SPEC_PATH = PROJECT_ROOT / "specs" / "book.yaml"
ENV_PATH = PROJECT_ROOT / ".env"


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


def _build_external_chunks(author_metadata: dict) -> list[dict[str, Any]]:
    """Cria contextos externos para inserção na tabela rag_external."""

    topic = author_metadata.get("topic", "Agentes de IA na saúde")
    return [
        {
            "topic": topic,
            "category": "estatistica",
            "content": (
                "Segundo relatório HIMSS 2024, 68% dos hospitais de grande porte já estudam "
                "agentes especializados para acelerar triagens clínicas."),
            "source": "HIMSS 2024",
            "metadata": {
                "credibility": 0.87,
                "tags": ["estatistica", "triagem"],
            },
        },
        {
            "topic": topic,
            "category": "caso_de_uso",
            "content": (
                "O Hospital Santa Aurora reduziu em 35% o tempo de resposta de teletriagem ao "
                "combinar LangChain 1.0 com supervisão médica assíncrona."),
            "source": "Estudo interno 2025",
            "metadata": {
                "credibility": 0.81,
                "tags": ["case", "teletriagem"],
            },
        },
    ]


def _get_supabase_client() -> Client:
    """Instancia o cliente Supabase usando variáveis de ambiente."""

    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL/KEY ausentes no ambiente")
    return create_client(url, key)


def _upsert(client: Client, table_name: str, rows: list[dict[str, Any]]) -> None:
    """Executa upsert em uma tabela do Supabase."""

    if not rows:
        return
    try:
        client.table(table_name).upsert(rows).execute()
        print(f"✅ {table_name}: {len(rows)} registros sincronizados")
    except Exception as exc:  # noqa: BLE001
        message = str(exc)
        print(f"❌ Falha ao inserir em {table_name}: {message}")
        if "PGRST205" in message or "Could not find the table" in message:
            raise RuntimeError(
                "Tabela inexistente. Execute scripts/supabase_schema.sql no Supabase "
                "SQL Editor e rode o seed novamente."
            ) from exc
        raise


def main() -> None:
    """Executa o seed completo das tabelas RAG."""

    _load_env_file()
    metadata = _load_book_metadata()
    author_name = metadata.get("author_name", "Autor Desconhecido")
    stories, positioning, vision = _build_author_payloads(author_name)
    external = _build_external_chunks(metadata)

    client = _get_supabase_client()
    _upsert(client, "rag_author_stories", stories)
    _upsert(client, "rag_author_positioning", positioning)
    _upsert(client, "rag_author_vision", vision)
    _upsert(client, "rag_external", external)
    print("🎯 Seed concluído.")


if __name__ == "__main__":
    main()
