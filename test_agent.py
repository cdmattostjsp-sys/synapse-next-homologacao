# ==========================================================
# 🧠 SynapseNext – Teste Institucional de Agentes Cognitivos
# Secretaria de Administração e Abastecimento (SAAB/TJSP)
# ==========================================================
# Este script valida o funcionamento dos módulos de IA:
#   - agents/document_agent.py
#   - utils/ai_client.py
#   - prompts/ (por módulo)
# ==========================================================

from agents.document_agent import DocumentAgent
import json
import os

# ----------------------------------------------------------
# ⚙️ Configuração do ambiente
# ----------------------------------------------------------
print("\n🔧 Iniciando teste institucional de agentes – SynapseNext vNext\n")

# Verifica se a chave OpenAI está disponível
if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERRO: variável de ambiente OPENAI_API_KEY não configurada.")
    print("💡 Use: export OPENAI_API_KEY='sua_chave_aqui'\n")
    exit(1)

# ----------------------------------------------------------
# 📘 Módulos a testar
# ----------------------------------------------------------
modulos_teste = {
    "DFD": {
        "unidade": "SAAB/TJSP",
        "descricao": "Aquisição de notebooks para expansão das unidades judiciais",
        "prazo": "30 dias",
        "responsavel": "Carlos Mattos",
    },
    "ETP": {
        "objeto": "Aquisição de notebooks",
        "justificativa_tecnica": "Necessidade de renovação do parque computacional",
        "estimativa_custos": "R$ 250.000,00",
    },
    "TR": {
        "objeto": "Aquisição de notebooks corporativos",
        "criterios_aceitacao": "Processadores i7, 16GB RAM, SSD 512GB",
        "prazo_execucao": "45 dias",
    },
}

# ----------------------------------------------------------
# 🚀 Execução dos testes
# ----------------------------------------------------------
resultados = {}

for modulo, metadata in modulos_teste.items():
    print(f"\n=== 🧩 Testando agente {modulo} ===")
    try:
        agent = DocumentAgent(modulo)
        resultado = agent.generate(metadata)
        resultados[modulo] = resultado

        # Exibir resumo visual
        print(f"✅ {modulo} gerado com sucesso ({len(resultado.get('secoes', {}))} seções).")
        print(f"🕒 Gerado em: {resultado.get('_gerado_em', 'N/D')}")
        print("🧾 Seções:", ", ".join(resultado.get("secoes", {}).keys()))
        if resultado.get("lacunas"):
            print("⚠️ Lacunas detectadas:", resultado["lacunas"])
        print("-" * 60)

    except Exception as e:
        print(f"❌ Falha ao gerar {modulo}: {e}")
        print("-" * 60)

# ----------------------------------------------------------
# 💾 Exportar resultado consolidado (corrigido)
# ----------------------------------------------------------
os.makedirs("exports/tests", exist_ok=True)
out_path = "exports/tests/test_agent_resultados.json"

# Converte objetos não-serializáveis (como _usage) para string
def safe_json(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)

# Sanitiza o dicionário antes de salvar
resultados_serializaveis = {
    k: {kk: safe_json(vv) for kk, vv in v.items()}
    for k, v in resultados.items()
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(resultados_serializaveis, f, ensure_ascii=False, indent=2)

print(f"\n📂 Resultados salvos em: {out_path}")
print("\n✅ Teste institucional concluído com sucesso.\n")
