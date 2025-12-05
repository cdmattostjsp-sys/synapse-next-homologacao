# -*- coding: utf-8 -*-
"""
utils/knowledge_loader.py – Carregador simples da knowledge_base


Objetivo: Ler textos .txt de pastas selecionadas e fornecer um bloco de contexto
para enriquecer o prompt do agente (sem dependência de embeddings neste patch).
"""
from __future__ import annotations
import os
from typing import List


KB_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")




def read_txt_files(subfolders: List[str], max_chars: int = 20000) -> str:
"""Concatena conteúdo .txt de subpastas sob knowledge_base, respeitando um limite de caracteres."""
chunks: List[str] = []
total = 0
for sub in subfolders:
base = os.path.join(KB_ROOT, sub)
if not os.path.isdir(base):
continue
for root, _, files in os.walk(base):
for fn in files:
if not fn.lower().endswith(".txt"):
continue
path = os.path.join(root, fn)
try:
with open(path, "r", encoding="utf-8", errors="ignore") as f:
text = f.read()
if not text.strip():
continue
# Respeita orçamento simples de caracteres
if total + len(text) > max_chars:
remaining = max(0, max_chars - total)
text = text[:remaining]
chunks.append(f"\n\n=== {fn} ===\n" + text)
total += len(text)
if total >= max_chars:
return "\n".join(chunks)
except Exception:
continue
return "\n".join(chunks)
