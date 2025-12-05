# ==========================================================
# 🧭 SynapseNext – Utilitário de Carregamento do Checklist de Edital
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================
# Este módulo permite carregar, de forma dinâmica e segura,
# o checklist de Edital (YAML) conforme o tipo de contratação.
# Inclui logs institucionais e compatibilidade com Streamlit.
# ==========================================================

from pathlib import Path
import yaml
import datetime

# ==========================================================
# 🧩 Função principal
# ==========================================================
def carregar_checklist(tipo: str = "servicos") -> list:
    """
    Carrega o checklist de Edital a partir do arquivo YAML principal
    localizado em 'knowledge/edital_checklist.yml'.

    Retorna a combinação dos itens:
        base + bloco específico (ex: servicos, obras, materiais, etc.)

    Args:
        tipo (str): tipo de contratação. Valores possíveis:
            'servicos', 'materiais', 'obras', 'ti', 'consultoria'

    Returns:
        list: lista consolidada de itens do checklist.
    """

    base_path = Path(__file__).resolve().parents[1] / "knowledge" / "edital_checklist.yml"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ======================================================
    # 🔍 Verificação do arquivo
    # ======================================================
    if not base_path.exists():
        log_mensagem(f"❌ [ERRO] Arquivo não encontrado: {base_path}")
        return []

    try:
        with open(base_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        log_mensagem(f"⚠️ [ERRO] Falha ao carregar YAML: {e}")
        return []

    # ======================================================
    # 🔎 Carregamento dos blocos
    # ======================================================
    base_itens = data.get("checklist", {}).get("base", {}).get("items", [])
    tipo_itens = data.get("checklist", {}).get(tipo, {}).get("items", [])

    if not tipo_itens:
        log_mensagem(f"⚠️ [AVISO] Tipo '{tipo}' não encontrado ou sem itens específicos no checklist.")
    else:
        log_mensagem(f"✅ Checklist carregado com sucesso ({tipo}) – {len(base_itens) + len(tipo_itens)} itens totais.")

    return base_itens + tipo_itens


# ==========================================================
# 🧾 Função de log institucional (com fallback)
# ==========================================================
def log_mensagem(msg: str):
    """
    Exibe a mensagem no Streamlit, se disponível.
    Caso contrário, imprime no terminal (modo CLI).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        import streamlit as st
        st.sidebar.info(f"[{timestamp}] {msg}")
    except ModuleNotFoundError:
        print(f"[{timestamp}] {msg}")


# ==========================================================
# 🧪 Teste rápido (opcional)
# ==========================================================
if __name__ == "__main__":
    # Teste de carregamento direto via terminal
    for t in ["servicos", "obras", "materiais", "ti", "consultoria"]:
        itens = carregar_checklist(t)
        print(f"\n🧩 Tipo: {t} → {len(itens)} itens")
