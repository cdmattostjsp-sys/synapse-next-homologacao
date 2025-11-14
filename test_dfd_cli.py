#!/usr/bin/env python3
# ==========================================================
# test_dfd_cli.py
# Teste do pipeline DFD diretamente via terminal (CLI)
# ==========================================================

import json
import re
from pathlib import Path

from utils.integration_dfd import (
    obter_dfd_da_sessao,
    gerar_rascunho_dfd_com_ia,
    salvar_dfd_manual,
)

# ----------------------------------------------------------
# Utilitário: limpar blocos ```json ... ```
# ----------------------------------------------------------
def limpar_markdown_json(texto):
    if not isinstance(texto, str):
        return texto

    cleaned = texto.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()


# ----------------------------------------------------------
# Utilitário: mapeamento igual ao usado na interface
# ----------------------------------------------------------
def mapear_campos_para_form(c):

    processo = c.get("processo", {}) or {}
    objeto = c.get("objeto", {}) or {}
    necessidade = c.get("necessidade_contratacao", {}) or {}

    unidade = c.get("unidade_demandante", "") or c.get("unidade", "")
    responsavel = c.get("responsavel", "")

    prazo = ""
    vigencia = necessidade.get("vigencia_atual_contrato") or {}
    if isinstance(vigencia, dict):
        prazo = vigencia.get("data_fim", "")

    descricao = (
        necessidade.get("descricao")
        or objeto.get("descricao")
        or ""
    )

    motivacao = ""
    if "justificativa" in necessidade:
        if isinstance(necessidade["justificativa"], list):
            motivacao = "\n".join(necessidade["justificativa"])
        else:
            motivacao = necessidade["justificativa"]

    valor_estimado = objeto.get("valor_estimado", "0,00")

    return {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "valor_estimado": valor_estimado,
    }


# ----------------------------------------------------------
# Execução principal
# ----------------------------------------------------------
print("\n====================================================")
print("🔍 TESTE DO PIPELINE DFD (modo terminal)")
print("====================================================\n")

# 1️⃣ Carrega o último JSON de insumo
dfd = obter_dfd_da_sessao()

if not dfd:
    print("❌ Nenhum DFD_ultimo.json encontrado.")
    exit(1)

print("📁 Arquivo carregado com sucesso:")
print(json.dumps(dfd, indent=2, ensure_ascii=False))

# 2️⃣ Obtém rascunho vindo da IA ou gera se necessário
rascunho_raw = dfd.get("resultado_ia", {}).get("resposta_texto")

if not rascunho_raw:
    print("\n🔄 Nenhum rascunho da IA encontrado. Gerando agora...")
    rascunho_raw = gerar_rascunho_dfd_com_ia()

if not rascunho_raw:
    print("❌ Falha ao obter ou gerar rascunho da IA.")
    exit(2)

print("\n📄 Rascunho bruto recebido da IA:")
print(rascunho_raw[:800], "...\n")  # printa só o começo para clareza

# 3️⃣ Sanitizar JSON
texto_limpo = limpar_markdown_json(rascunho_raw)

try:
    parsed = json.loads(texto_limpo)
    print("✅ JSON parseado com sucesso!\n")
except Exception as e:
    print("❌ ERRO PARSEANDO JSON DA IA!")
    print(str(e))
    print("\nConteúdo recebido:")
    print(texto_limpo)
    exit(3)

# Normaliza se necessário
if "DFD" in parsed:
    campos = parsed["DFD"]
else:
    campos = parsed

# 4️⃣ Mapeia os campos para formato da página
mapeado = mapear_campos_para_form(campos)

print("📌 Campos mapeados:")
for k, v in mapeado.items():
    print(f"  - {k}: {v}")

# 5️⃣ Pergunta ao usuário se quer salvar
print("\nDeseja salvar o DFD consolidado? (s/n): ", end="")
resp = input().strip().lower()

if resp == "s":
    dfd_final = {
        "DFD": mapeado
    }
    salvar_dfd_manual(dfd_final)
    print("💾 DFD salvo com sucesso!")
else:
    print("✔ Nenhum arquivo salvo.")
