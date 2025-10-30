# -*- coding: utf-8 -*-
"""
debug_alertas.py – Diagnóstico de integridade do módulo de alertas
=====================================================================
Verifica se o módulo utils.alertas_pipeline está acessível,
se o dicionário DEFAULTS contém todas as chaves esperadas e
se as funções export_alerts_json e evaluate_alerts estão operacionais.
=====================================================================
"""

import importlib
import sys
import os
import json
from datetime import datetime

# ======================================================
# 🧭 Ajuste de path (garante que utils/ seja encontrado)
# ======================================================
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

print("\n🔧 Iniciando diagnóstico do módulo de alertas...\n")

try:
    # Reimporta módulo forçando reload
    import utils.alertas_pipeline as alertas
    importlib.reload(alertas)

    print(f"✅ Módulo localizado: {alertas.__file__}")

    # Verifica DEFAULTS
    print("\n📦 DEFAULTS detectado:")
    print(json.dumps(alertas.DEFAULTS, indent=2, ensure_ascii=False))

    # Valida chaves obrigatórias
    obrigatorias = [
        "min_coerencia_global",
        "min_pairwise",
        "min_similaridade_tematica",
        "alerta_critico",
        "peso_risco"
    ]
    faltantes = [k for k in obrigatorias if k not in alertas.DEFAULTS]
    if faltantes:
        print(f"❌ ERRO: chaves faltando em DEFAULTS: {faltantes}")
    else:
        print("✅ Todas as chaves padrão estão presentes.")

    # Testa função evaluate_alerts
    print("\n🧪 Executando avaliação simulada...")
    resultados = alertas.evaluate_alerts(coerencia_global=78, pairwise_min=68)
    print("✅ Função evaluate_alerts executada com sucesso.")
    print(json.dumps(resultados, indent=2, ensure_ascii=False))

    # Testa exportação
    print("\n�� Testando exportação JSON...")
    caminho = alertas.export_alerts_json(resultados)
    print(f"✅ Arquivo salvo em: {caminho}")

    print("\n🎯 Diagnóstico concluído com sucesso. Módulo funcional.\n")

except ModuleNotFoundError as e:
    print(f"❌ ERRO: módulo não encontrado: {e}")

except AttributeError as e:
    print(f"❌ ERRO: função ou constante ausente: {e}")

except Exception as e:
    print(f"⚠️ ERRO inesperado: {e}")
