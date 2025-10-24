# -*- coding: utf-8 -*-
"""
Integração (opcional) com GitHub para versionar artefatos gerados.
Depende de variável de ambiente/secret: GITHUB_TOKEN
Uso:
    from agents.github_bridge import GitHubBridge
    gh = GitHubBridge(owner="tjsp-org", repo="synapse-next")
    gh.commit_text("exports/relatorio/DFD_123.json", json.dumps(doc, ensure_ascii=False), "feat(dfd): adicionar rascunho")
"""
from __future__ import annotations
import os
from typing import Optional

class GitHubBridge:
    def __init__(self, owner: str, repo: str, branch: str = "main", token: Optional[str] = None):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN não configurado.")
        try:
            from github import Github  # PyGithub
        except Exception as e:
            raise RuntimeError("Pacote PyGithub não encontrado. Adicione `PyGithub>=2.2.0` ao requirements.txt.")
        self._gh = Github(self.token)
        self._repo = self._gh.get_repo(f"{owner}/{repo}")

    def commit_text(self, path: str, content: str, message: str):
        try:
            # Tentar obter arquivo existente
            file = self._repo.get_contents(path, ref=self.branch)
            self._repo.update_file(path, message, content, file.sha, branch=self.branch)
        except Exception:
            # Criar se não existir
            self._repo.create_file(path, message, content, branch=self.branch)
