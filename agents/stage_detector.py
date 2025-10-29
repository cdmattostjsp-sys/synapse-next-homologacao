"""
stage_detector.py – SynapseNext vNext
Agente de detecção automática de estágio da jornada de contratação.
Homologado: SAAB/TJSP – vNext 2025
"""

import os
import json
from datetime import datetime

EXPORTS_DIR = "exports"
LOG_DIR = os.path.join(EXPORTS_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

STAGES = [
    ("DFD", "dfd_data.json"),
    ("ETP", "etp_data.json"),
    ("TR", "tr_data.json"),
    ("EDITAL", "edital_data.json"),
    ("CONTRATO", "contrato_data.json")
]


class StageDetector:
    """
    Analisa os artefatos existentes e determina o estágio atual do processo.
    """

    def __init__(self, exports_dir=EXPORTS_DIR):
        self.exports_dir = exports_dir

    def detect_stage(self, verbose=False) -> dict:
        """
        Detecta o estágio atual da jornada de contratação com base
        nos artefatos presentes e válidos.
        """
        status = {}
        logs = []
        current_stage = "INDEFINIDO"

        for stage, filename in STAGES:
            path = os.path.join(self.exports_dir, filename)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    valid = bool(data)
                    logs.append(f"✅ {stage} detectado ({filename}) – válido: {valid}")
                    status[stage] = {"existe": True, "valido": valid}
                    current_stage = stage
                except Exception as e:
                    logs.append(f"⚠️ Erro ao ler {filename}: {e}")
                    status[stage] = {"existe": True, "valido": False}
            else:
                logs.append(f"❌ {stage} ausente ({filename})")
                status[stage] = {"existe": False, "valido": False}

        logs.append("\n📊 Estágio atual identificado: " + current_stage)
        result = {
            "estagio_atual": current_stage,
            "detalhes": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if verbose:
            print("\n".join(logs))

        self._registrar_log(result, logs)
        return result

    def _registrar_log(self, resultado: dict, logs: list):
        """
        Registra o resultado da detecção em um arquivo de log institucional.
        """
        path = os.path.join(LOG_DIR, f"stage_detector_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("============================================================\n")
            f.write("🔍 SynapseNext – Detecção de Estágio da Jornada\n")
            f.write(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("============================================================\n\n")
            f.write("\n".join(logs))
            f.write("\n\nResumo:\n")
            f.write(json.dumps(resultado, ensure_ascii=False, indent=2))
        print(f"📄 Log salvo em: {path}")

    def detect_stage_verbose(self):
        """Executa a detecção detalhada (modo verbose)."""
        return self.detect_stage(verbose=True)


if __name__ == "__main__":
    print("🔍 Teste rápido do StageDetector – SynapseNext vNext\n")
    detector = StageDetector()
    resultado = detector.detect_stage_verbose()
    print("\n📊 Resultado consolidado:\n", json.dumps(resultado, ensure_ascii=False, indent=2))
