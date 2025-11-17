-- Schema setup for Ebook Generator Supabase project
-- Run this script inside Supabase SQL Editor (project: ebook_generator)
-- It creates the RAG tables consumed by the pipeline agents.

create table if not exists public.rag_author_stories (
    id bigserial primary key,
    author_name text not null,
    story text not null,
    category text,
    tags text[],
    created_at timestamptz default timezone('utc', now())
);

create table if not exists public.rag_author_positioning (
    id bigserial primary key,
    author_name text not null,
    positioning_statement text not null,
    aspect text,
    created_at timestamptz default timezone('utc', now())
);

create table if not exists public.rag_author_vision (
    id bigserial primary key,
    author_name text not null,
    vision_or_opinion text not null,
    category text,
    principle text,
    created_at timestamptz default timezone('utc', now())
);

create table if not exists public.rag_external (
    id bigserial primary key,
    topic text not null,
    category text,
    content text not null,
    source text,
    metadata jsonb default '{}'::jsonb,
    created_at timestamptz default timezone('utc', now())
);
