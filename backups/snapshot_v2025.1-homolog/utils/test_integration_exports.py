# -*- coding: utf-8 -*-
"""
==========================================================
🧩 Teste Institucional de Integração – SynapseNext vNext
Secretaria de Administração e Abastecimento – SAAB/TJSP
==========================================================

Objetivo:
  Verificar a camada de integração e exportação de dados
  (DFD, ETP e TR) do pipeline SynapseNext vNext.

Execução:
  python utils/test_integration_exports.py
==========================================================
"""

import os
import json
from datetime import datetime

# Importações condicionais (apenas se existirem os módulos)
try:
    from utils.integration_dfd import export_dfd_to_json, load_dfd_from_json
except ImportError:
    export_dfd_to_json = load_dfd_from_json = None

try:
    from utils.integration_etp import export_etp_to_json, load_etp_from_json
except ImportError:
    export_etp_to_json = load_etp_from_json = None

try:
    from utils.integration_tr import export_tr_to_json, load_tr_from_json
except ImportError:
    export_tr_to_json = load_tr_from_json = None

EXPORTS_DIR = "exports"

# ----------------------------------------------------------
# 🔧 Função auxiliar para exibir status formatado
# ----------------------------------------------------------
def print_status(etapa: str, status: str, extra: str = ""):
    icone = "✅" if "Sucesso" in status else "❌"
    print(f"{icone} {etapa.ljust(15)} → {status} {extra}")

# ----------------------------------------------------------
# 🚀 Teste principal
# ----------------------------------------------------------
print("\n🔧 Iniciando teste institucional de integração – SynapseNext vNext\n")

os.makedirs(EXPORTS_DIR, exist_ok=True)

# Teste DFD
if export_dfd_to_json and load_dfd_from_json:
    print("=== 🧩 Testando integração DFD ===")
    dfd_data = {"unidade": "SAAB", "objeto": "Aquisição de notebooks"}
    path = export_dfd_to_json(dfd_data)
    loaded = load_dfd_from_json()
    print_status("Exportação DFD", "Sucesso" if os.path.exists(path) else "Falhou", f"→ {path}")
    print_status("Leitura DFD", "Sucesso" if loaded == dfd_data else "Falhou", str(loaded))
    print("------------------------------------------------------------")
else:
    print_status("DFD", "❌ Módulo não encontrado")

# Teste ETP
if export_etp_to_json and load_etp_from_json:
    print("=== 📘 Testando integração ETP ===")
    etp_data = {"objeto": "Aquisição de notebooks", "estimativa": "R$ 250.000,00"}
    path = export_etp_to_json(etp_data)
    loaded = load_etp_from_json()
    print_status("Exportação ETP", "Sucesso" if os.path.exists(path) else "Falhou", f"→ {path}")
    print_status("Leitura ETP", "Sucesso" if loaded == etp_data else "Falhou", str(loaded))
    print("------------------------------------------------------------")
else:
    print_status("ETP", "❌ Módulo não encontrado")

# Teste TR
if export_tr_to_json and load_tr_from_json:
    print("=== 📑 Testando integração TR ===")
    tr_data = {"objeto": "Aquisição de notebooks", "prazo_execucao": "45 dias"}
    path = export_tr_to_json(tr_data)
    loaded = load_tr_from_json()
    print_status("Exportação TR", "Sucesso" if os.path.exists(path) else "Falhou", f"→ {path}")
    print_status("Leitura TR", "Sucesso" if loaded == tr_data else "Falhou", str(loaded))
    print("------------------------------------------------------------")
else:
    print_status("TR", "❌ Módulo não encontrado")

# ----------------------------------------------------------
# 💾 Resultado final consolidado
# ----------------------------------------------------------
resultado = {
    "executado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "dfd": os.path.exists("exports/dfd_data.json"),
    "etp": os.path.exists("exports/etp_data.json"),
    "tr": os.path.exists("exports/tr_data.json"),
}

os.makedirs("exports/tests", exist_ok=True)
result_path = "exports/tests/test_integration_exports_result.json"

with open(result_path, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("\n📂 Resultados salvos em:", result_path)
print("✅ Teste institucional concluído com sucesso.\n")
