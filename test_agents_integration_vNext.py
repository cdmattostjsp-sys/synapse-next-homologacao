"""
test_agents_integration_vNext.py – SynapseNext vNext
Teste integrado dos agentes internos homologados.
Verifica comunicação, geração de artefatos e logs.
Homologado: SAAB/TJSP – vNext 2025
"""

import os
import json
from agents.document_agent import DocumentAgent
from agents.stage_detector import StageDetector
from agents.guide_agent import GuideAgent
from agents.github_bridge import GitHubBridge

EXPORTS = "exports"
LOGS = os.path.join(EXPORTS, "logs")
os.makedirs(LOGS, exist_ok=True)

print("===================================================")
print("🧠 Teste Integrado – Núcleo de Agentes SynapseNext vNext")
print("===================================================\n")

# 1️⃣ Testa DocumentAgent
try:
    doc_agent = DocumentAgent()
    artefato = doc_agent.processar_documento(
        "insumos_processados/DFD_Ficticio_SynapseNext.txt"
    )
    print(f"✅ DocumentAgent gerou: {artefato}")
except Exception as e:
    print(f"❌ Erro no DocumentAgent: {e}")

# 2️⃣ Testa StageDetector
try:
    detector = StageDetector()
    resultado_stage = detector.detect_stage(verbose=True)
    print("\n📊 Estágio detectado:", resultado_stage["estagio_atual"])
except Exception as e:
    print(f"❌ Erro no StageDetector: {e}")

# 3️⃣ Testa GuideAgent
try:
    guide = GuideAgent()
    orientacao = guide.gerar_orientacao()
    log_path = guide.registrar_orientacao(orientacao)
    print("\n🧭 GuideAgent executado com sucesso.")
    print("📄 Log salvo em:", log_path)
except Exception as e:
    print(f"❌ Erro no GuideAgent: {e}")

# 4️⃣ Testa GitHubBridge
try:
    bridge = GitHubBridge()
    bridge.commit_and_log("Homologação automática – Teste Integrado vNext")
    print("🔗 GitHubBridge executado com sucesso.")
except Exception as e:
    print(f"❌ Erro no GitHubBridge: {e}")

print("\n===================================================")
print("✅ Teste integrado concluído.")
print(f"📂 Logs salvos em: {LOGS}")
print("===================================================\n")
