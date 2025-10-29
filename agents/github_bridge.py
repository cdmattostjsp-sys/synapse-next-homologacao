"""
github_bridge.py – SynapseNext vNext
Agente responsável pela integração segura entre o ambiente local (Codespaces)
e o repositório GitHub oficial do projeto.
Permite sincronização, commit automatizado e registro de auditoria.
Homologado: SAAB/TJSP – vNext 2025
"""

import os
import subprocess
from datetime import datetime

LOG_DIR = "exports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

class GitHubBridge:
    """
    Agente de integração e auditoria GitHub.
    Suporta execução com ou sem token de autenticação.
    """

    def __init__(self):
        self.repo_url = self._get_repo_url()
        self.has_git = self._check_git_available()

    def _check_git_available(self) -> bool:
        """Verifica se o Git está instalado e acessível."""
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            return True
        except Exception:
            return False

    def _get_repo_url(self) -> str:
        """Obtém a URL do repositório remoto configurado."""
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True, text=True
            )
            return result.stdout.strip() or "desconhecido"
        except Exception:
            return "desconhecido"

    def commit_and_log(self, message: str = "Atualização automática – SynapseNext vNext") -> None:
        """
        Cria commit local e registra log de auditoria.
        Se o push falhar (por falta de token), mantém log local seguro.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = os.path.join(LOG_DIR, f"github_bridge_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")

        with open(log_path, "w", encoding="utf-8") as log:
            log.write("============================================================\n")
            log.write("🔗 GitHub Bridge – SynapseNext vNext\n")
            log.write(f"🕒 Execução: {timestamp}\n")
            log.write(f"📁 Repositório: {self.repo_url}\n")
            log.write("============================================================\n\n")

            if not self.has_git:
                log.write("❌ Git não detectado neste ambiente.\n")
                print("⚠️ Git não encontrado — commit remoto desabilitado.")
                return

            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", message], check=True)
                log.write("✅ Commit local criado com sucesso.\n")

                # Tenta enviar (push) — caso falhe, mantém log local
                push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
                if push_result.returncode == 0:
                    log.write("🚀 Push remoto realizado com sucesso.\n")
                else:
                    log.write("⚠️ Falha no push remoto (sem token ou permissões).\n")
                    log.write(f"Detalhes: {push_result.stderr}\n")

            except subprocess.CalledProcessError as e:
                log.write(f"❌ Erro ao executar operação Git: {e}\n")

        print(f"📄 Log salvo em: {log_path}")

    def create_snapshot(self, branch_name: str = None) -> None:
        """
        Cria um snapshot da versão atual (novo branch local opcional).
        Exemplo: snapshot_20251029_1530
        """
        if not self.has_git:
            print("⚠️ Git não disponível neste ambiente.")
            return

        branch = branch_name or f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M')}"
        try:
            subprocess.run(["git", "checkout", "-b", branch], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Snapshot automático {branch}"], check=True)
            print(f"📦 Snapshot criado: {branch}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Falha ao criar snapshot: {e}")


if __name__ == "__main__":
    print("🔗 Teste rápido do GitHubBridge – SynapseNext vNext")
    bridge = GitHubBridge()
    bridge.commit_and_log("Teste de auditoria e commit automático.")
