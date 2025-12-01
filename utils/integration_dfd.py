# ======================================================================
# utils/integration_dfd.py — Versão 2025-D2.4 (Fluxo A – 100% Moderno)
# Compatível com DocumentAgent(D2) + AIClient vNext
# Fluxo oficial: INSUMOS → DFD Moderno (texto_narrativo + 11 seções + lacunas)
# ======================================================================

from __future__ import annotations
import os
import json
import glob
from datetime import datetime
import streamlit as st


# ======================================================================
# 🔧 Utilitários básicos
# ======================================================================

SECOES_DFD_PADRAO = [
    "Contexto Institucional",
    "Diagnóstico da Situação Atual",
    "Fundamentação da Necessidade",
    "Objetivos da Contratação",
    "Escopo Inicial da Demanda",
    "Resultados Esperados",
    "Benefícios Institucionais",
    "Justificativa Legal",
    "Riscos da Não Contratação",
    "Requisitos Mínimos",
    "Critérios de Sucesso",
]


def _limpar_markdown(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    return (
        texto.replace("```json", "")
        .replace("```", "")
        .replace("“", '"')
        .replace("”", '"')
        .strip()
    )


def _to_str(valor) -> str:
    if valor is None:
        return ""
    if isinstance(valor, (dict, list)):
        try:
            return json.dumps(valor, ensure_ascii=False, indent=2)
        except Exception:
            return str(valor)
    return str(valor).strip()


# ======================================================================
# 🧩 Normalização para o MODELO MODERNO
# ======================================================================
def _normalizar_para_moderno(dados_brutos: dict) -> dict:
    """
    Recebe QUALQUER formato parcialmente estruturado e devolve SEMPRE
    um DFD MODERNO completo, com as chaves:

    - unidade_demandante
    - responsavel
    - prazo_estimado
    - valor_estimado
    - descricao_necessidade
    - motivacao
    - texto_narrativo
    - secoes (11 seções Moderno-Governança)
    - lacunas (lista)
    """

    if not isinstance(dados_brutos, dict):
        dados_brutos = {}

    # Compatibilidade: IA pode devolver {"DFD": {...}}
    if "DFD" in dados_brutos and isinstance(dados_brutos["DFD"], dict):
        dados_brutos = dados_brutos["DFD"]

    # ---------------------------
    # Campos administrativos
    # ---------------------------
    unidade = _to_str(
        dados_brutos.get("unidade_demandante")
        or dados_brutos.get("unidade")
    )
    responsavel = _to_str(dados_brutos.get("responsavel"))
    prazo = _to_str(
        dados_brutos.get("prazo_estimado")
        or dados_brutos.get("prazo")
    )

    valor_raw = (
        dados_brutos.get("valor_estimado")
        or dados_brutos.get("estimativa_valor")
        or "0,00"
    )
    valor = _to_str(valor_raw) or "0,00"

    # ---------------------------
    # Síntese tradicional
    # ---------------------------
    descricao = _to_str(
        dados_brutos.get("descricao_necessidade")
        or dados_brutos.get("descricao")
        or dados_brutos.get("conteudo")
    )

    motivacao = _to_str(dados_brutos.get("motivacao"))

    # ---------------------------
    # Seções Moderno-Governança
    # ---------------------------
    secoes_orig = dados_brutos.get("secoes")
    secoes = {}
    if isinstance(secoes_orig, dict):
        for k, v in secoes_orig.items():
            secoes[k] = _limpar_markdown(_to_str(v))

    # Se não houver seções, criar estrutura mínima a partir da descrição/motivação
    if not secoes:
        for nome in SECOES_DFD_PADRAO:
            secoes[nome] = "Conteúdo não identificado explicitamente no insumo."

        if descricao:
            secoes["Fundamentação da Necessidade"] = descricao

        if motivacao:
            secoes["Resultados Esperados"] = motivacao

    # Garantir todas as 11 seções
    for nome in SECOES_DFD_PADRAO:
        if nome not in secoes or not isinstance(secoes[nome], str) or not secoes[nome].strip():
            secoes[nome] = "Conteúdo não identificado explicitamente no insumo."

    # ---------------------------
    # Texto narrativo consolidado
    # ---------------------------
    texto_narrativo = _limpar_markdown(_to_str(dados_brutos.get("texto_narrativo")))

    if not texto_narrativo:
        # Monta a partir das seções (versão numerada)
        partes = []
        idx = 1
        for nome in SECOES_DFD_PADRAO:
            t = secoes.get(nome, "").strip()
            if t:
                partes.append(f"{idx}. {t}")
                idx += 1

        if partes:
            texto_narrativo = "\n\n".join(partes)
        else:
            # Fallback: descrição + motivação
            partes = []
            if descricao:
                partes.append(f"1. {descricao}")
            if motivacao:
                partes.append(f"2. {motivacao}")
            texto_narrativo = "\n\n".join(partes)

    # ---------------------------
    # Lacunas
    # ---------------------------
    lacunas_raw = dados_brutos.get("lacunas", [])
    lacunas = []
    if isinstance(lacunas_raw, list):
        for item in lacunas_raw:
            t = _to_str(item)
            if t:
                lacunas.append(t)

    # ---------------------------
    # Resultado MODERNO
    # ---------------------------
    dfd_moderno = {
        "unidade_demandante": unidade,
        "responsavel": responsavel,
        "prazo_estimado": prazo,
        "valor_estimado": valor,
        "descricao_necessidade": descricao,
        "motivacao": motivacao,
        "texto_narrativo": texto_narrativo,
        "secoes": secoes,
        "lacunas": lacunas,
    }

    return dfd_moderno


# ======================================================================
# 📥 Leitura de arquivos DFD
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {caminho}: {e}")
        return {}

    # Caso 1 — DFD consolidado (formulário moderno)
    if isinstance(dados.get("campos_ai"), dict):
        return _normalizar_para_moderno(dados["campos_ai"])

    # Caso 2 — resultado IA moderna gravado diretamente
    if isinstance(dados.get("resultado_ia"), dict):
        return _normalizar_para_moderno(dados["resultado_ia"])

    if "DFD" in dados:
        return _normalizar_para_moderno(dados)

    # Caso 3 — insumo puro (apenas texto bruto do PDF/TXT)
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 20:
        return _normalizar_para_moderno(
            {"descricao_necessidade": texto.strip()}
        )

    return {}


# ======================================================================
# 🔄 Obter DFD carregado (sessão → último arquivo → histórico)
# ======================================================================
def obter_dfd_da_sessao() -> dict:
    """
    Fonte de verdade para a página DFD.

    1. Se existir na sessão: dfd_moderno
    2. Se existir dfd_campos_ai (legado), normaliza e migra
    3. Se existir DFD_ultimo.json → carrega e normaliza
    4. Se existir histórico DFD_*.json → pega o mais recente
    """

    # Sessão – novo padrão
    if "dfd_moderno" in st.session_state and st.session_state["dfd_moderno"]:
        return st.session_state["dfd_moderno"]

    # Sessão – legado recente
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        dfd_norm = _normalizar_para_moderno(st.session_state["dfd_campos_ai"])
        st.session_state["dfd_moderno"] = dfd_norm
        return dfd_norm

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # Último arquivo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_moderno"] = dados
            return dados

    # Histórico
    arquivos = sorted(
        glob.glob(os.path.join(base, "DFD_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )

    for arq in arquivos:
        if arq.endswith("DFD_ultimo.json"):
            continue
        dados = _carregar_dfd_de_arquivo(arq)
        if dados:
            st.session_state["dfd_moderno"] = dados
            return dados

    return {}


# ======================================================================
# 💾 Salvar DFD consolidado (formulário → JSON)
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "formulario_dfd_moderno_streamlit") -> str:
    """
    Recebe um dicionário (vindo do formulário) e garante que será salvo
    no formato MODERNO, em:

      exports/insumos/json/DFD_ultimo.json
      exports/insumos/json/DFD_<timestamp>.json
    """
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    dfd_moderno = _normalizar_para_moderno(campos)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": dfd_moderno,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arq1 = os.path.join(base, "DFD_ultimo.json")
    arq2 = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq1, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq2, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.session_state["dfd_moderno"] = dfd_moderno
        return arq1

    except Exception as e:
        st.error(f"❌ Falha ao salvar DFD: {e}")
        return ""


# ======================================================================
# 🧾 Status exibido na página DFD
# ======================================================================
def status_dfd() -> str:
    if "dfd_moderno" in st.session_state and st.session_state["dfd_moderno"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível a partir dos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo INSUMOS."


# ======================================================================
# 🧠 IA → Gerar rascunho do DFD MODERNO (Versão final compatível)
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:
    """
    Lê o insumo DFD_ultimo.json (conteudo_textual),
    envia o texto bruto para o DocumentAgent(D2),
    e normaliza SEMPRE para o modelo MODERNO completo.
    """

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("⚠️ Nenhum insumo encontrado para DFD (DFD_ultimo.json inexistente).")
        return {}

    # 1) Leitura do insumo bruto
    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        texto = (dados.get("conteudo_textual") or "").strip()

    except Exception as e:
        st.error(f"❌ Falha ao ler insumo DFD_ultimo.json: {e}")
        return {}

    if len(texto) < 20:
        st.error("⚠️ Texto insuficiente para processamento pela IA.")
        return {}

    # 2) Chamada da IA (DocumentAgent)
    try:
        from agents.document_agent import processar_dfd_com_ia

        bruto = processar_dfd_com_ia(texto)

        # unwrap padrão {"resultado_ia": {...}}
        if isinstance(bruto, dict) and "resultado_ia" in bruto:
            bruto = bruto["resultado_ia"]

        dfd_moderno = _normalizar_para_moderno(bruto)

        # 3) Persistência em arquivo (substitui DFD_ultimo.json por versão moderna)
        os.makedirs(base, exist_ok=True)

        payload = {
            "artefato": "DFD",
            "origem": "ia_dfd_moderno",
            "campos_ai": dfd_moderno,
            "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fonte_insumo": {
                "arquivo": dados.get("arquivo"),
                "tipo": dados.get("tipo"),
            },
        }

        with open(ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        historico = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(historico, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # 4) Persistência na sessão
        st.session_state["dfd_moderno"] = dfd_moderno
        return dfd_moderno

    except Exception as e:
        st.error(f"❌ Erro ao processar DFD com IA: {e}")
        return {}
