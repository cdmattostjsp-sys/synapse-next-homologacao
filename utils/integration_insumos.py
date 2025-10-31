# ==========================================================
# 📜 integration_edital.py – Minuta do Edital (versão final)
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Responsável por:
# 1) Extrair texto de PDF/DOCX/TXT do insumo de EDITAL.
# 2) Integrar o contexto cumulativo (DFD + ETP + TR).
# 3) Invocar IA institucional (OpenAI) + modelos da Knowledge Base.
# 4) Normalizar campos e devolver JSON para pré-preenchimento da página.
# 5) Gerar DOCX oficial em /exports.
# ==========================================================

import os
import re
import json
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

import fitz          # PyMuPDF
import docx2txt
from docx import Document
from openai import OpenAI

# -----------------------------
# ⚙️ OpenAI Client
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# 📂 Paths
# -----------------------------
BASE_PATH = Path(__file__).resolve().parents[1]
KNOWLEDGE_EDITAL = BASE_PATH / "knowledge" / "edital_models"
EXPORTS_DIR = BASE_PATH / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 📚 Leitura dos modelos (Knowledge Base)
# ==========================================================
def ler_modelos_edital() -> str:
    textos = []
    if KNOWLEDGE_EDITAL.exists():
        for arq in KNOWLEDGE_EDITAL.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)


# ==========================================================
# 🔗 Integração de contexto (DFD, ETP, TR)
# ==========================================================
def integrar_com_contexto(session_state: dict) -> dict:
    """
    Constrói um contexto integrado com o que existir na sessão:
    DFD + ETP + TR. É tolerante à ausência de qualquer um deles.
    """
    contexto = {}
    for chave in ["dfd_campos_ai", "etp_campos_ai", "tr_campos_ai"]:
        bloco = session_state.get(chave)
        if isinstance(bloco, dict) and bloco:
            contexto[chave] = bloco
    return contexto


# ==========================================================
# 🧾 Extração e limpeza de texto
# ==========================================================
def _extrair_texto_arquivo(arquivo) -> str:
    nome = getattr(arquivo, "name", "").lower()
    try:
        if nome.endswith(".pdf"):
            dados = arquivo.read()
            arquivo.seek(0)
            texto = ""
            with fitz.open(stream=dados, filetype="pdf") as pdf:
                for p in pdf:
                    texto += p.get_text("text") + "\n"
            return _limpar(texto)

        if nome.endswith(".docx"):
            dados = arquivo.read()
            arquivo.seek(0)
            return _limpar(docx2txt.process(BytesIO(dados)))

        if nome.endswith(".txt"):
            dados = arquivo.read()
            arquivo.seek(0)
            return _limpar(dados.decode("utf-8", errors="ignore"))
    except Exception:
        pass
    return ""


def _limpar(txt: str) -> str:
    txt = re.sub(r"\s+", " ", txt or "")
    txt = re.sub(r"[^\w\s.,;:!?()/%\-–—ºª°]", "", txt)
    return txt.strip()


# ==========================================================
# 🧠 Invocação IA + Normalização de Campos
# ==========================================================
def _chamar_ia_edital(texto_insumo: str, modelos: str, contexto: dict) -> Dict[str, Any]:
    """
    Chama a IA institucional para projetar os campos do edital.
    Retorna um dicionário com os campos (ou fallback mínimo).
    """
    contexto_json = json.dumps(contexto or {}, ensure_ascii=False, indent=2)

    system_prompt = (
        "Você é um agente institucional do Tribunal de Justiça do Estado de São Paulo (SAAB/TJSP), "
        "especializado em minutas de EDITAL conforme a Lei 14.133/2021. "
        "Extraia e proponha os campos do edital com linguagem padrão SAAB/TJSP."
    )

    user_prompt = f"""
Texto do insumo (base):
\"\"\"{texto_insumo[:10000]}\"\"\"

Contexto cumulativo disponível (DFD, ETP, TR):
\"\"\"{contexto_json}\"\"\"

Modelos institucionais (Knowledge Base):
\"\"\"{modelos[:10000]}\"\"\"

Retorne APENAS um JSON com os campos:
{{
  "objeto": "",
  "tipo_licitacao": "",
  "criterio_julgamento": "",
  "condicoes_participacao": "",
  "exigencias_habilitacao": "",
  "obrigacoes_contratada": "",
  "prazo_execucao": "",
  "fontes_recursos": "",
  "gestor_fiscal": "",
  "observacoes_gerais": ""
}}
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        conteudo = resp.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", conteudo, re.DOTALL)
        campos = json.loads(match.group(0)) if match else {}
    except Exception as e:
        campos = {"erro_interna": f"Falha IA EDITAL: {e}"}

    return campos


def _normalizar_campos(campos: Dict[str, Any], contexto: dict) -> Dict[str, str]:
    """
    Aplica defaults e aproveita dados administrativos vindos do DFD/TR.
    Também gera 'numero_edital' e 'data_publicacao'.
    """
    hoje = datetime.now()
    numero_auto = f"TJSP-PE-{hoje.year}-{hoje.strftime('%m')}{hoje.strftime('%d')}"
    data_auto = hoje.strftime("%d/%m/%Y")

    dfd = (contexto or {}).get("dfd_campos_ai", {})
    tr = (contexto or {}).get("tr_campos_ai", {})

    defaults = {
        "objeto": dfd.get("objeto") or tr.get("objeto") or "",
        "tipo_licitacao": "Pregão eletrônico",
        "criterio_julgamento": tr.get("criterios_de_julgamento") or "Menor preço global",
        "condicoes_participacao": "",
        "exigencias_habilitacao": "",
        "obrigacoes_contratada": tr.get("obrigacoes_da_contratada") or "",
        "prazo_execucao": tr.get("prazo_execucao") or "",
        "fontes_recursos": tr.get("fonte_recurso") or "",
        "gestor_fiscal": dfd.get("responsavel") or "",
        "observacoes_gerais": "",
        # administrativos
        "numero_edital": numero_auto,
        "data_publicacao": data_auto,
        "unidade_solicitante": dfd.get("unidade_solicitante") or "",
        "responsavel": dfd.get("responsavel") or "",
    }

    normal = {}
    for k, v in defaults.items():
        normal[k] = (campos.get(k) or v or "").strip()

    # Higiene mínima
    for k in list(normal.keys()):
        normal[k] = re.sub(r"\s+", " ", normal[k]).strip()

    return normal


# ==========================================================
# 🧱 Geração do Rascunho textual + DOCX oficial
# ==========================================================
def gerar_rascunho_edital(campos: Dict[str, str], modelos_referencia: str = "") -> str:
    """
    Monta um rascunho textual estruturado do edital
    (usado como pré-visualização na página).
    """
    linhas = [
        f"EDITAL Nº {campos.get('numero_edital','')}",
        f"Data de Publicação: {campos.get('data_publicacao','')}",
        "",
        f"Unidade Solicitante: {campos.get('unidade_solicitante','')}",
        f"Responsável: {campos.get('responsavel','')}",
        "",
        "1. DO OBJETO",
        campos.get("objeto",""),
        "",
        "2. DO TIPO E CRITÉRIO DE JULGAMENTO",
        f"Tipo de licitação: {campos.get('tipo_licitacao','')}",
        f"Critério de julgamento: {campos.get('criterio_julgamento','')}",
        "",
        "3. DAS CONDIÇÕES DE PARTICIPAÇÃO",
        campos.get("condicoes_participacao",""),
        "",
        "4. DAS EXIGÊNCIAS DE HABILITAÇÃO",
        campos.get("exigencias_habilitacao",""),
        "",
        "5. DAS OBRIGAÇÕES DA CONTRATADA",
        campos.get("obrigacoes_contratada",""),
        "",
        "6. DO PRAZO DE EXECUÇÃO",
        campos.get("prazo_execucao",""),
        "",
        "7. DAS FONTES DE RECURSOS",
        campos.get("fontes_recursos",""),
        "",
        "8. DO GESTOR/FISCAL DO CONTRATO",
        campos.get("gestor_fiscal",""),
        "",
        "9. DAS DISPOSIÇÕES FINAIS",
        campos.get("observacoes_gerais",""),
    ]
    if modelos_referencia:
        linhas += ["", "ANEXO – ORIENTAÇÕES INSTITUCIONAIS (trecho da KB)", modelos_referencia[:1200] + " …"]
    return "\n".join(linhas)


def gerar_edital_docx(campos: Dict[str, str], texto_completo: Optional[str] = None) -> str:
    """
    Gera o documento oficial (DOCX) do edital e grava em /exports.
    Retorna o caminho do arquivo gerado.
    """
    doc = Document()
    doc.add_heading(f"EDITAL Nº {campos.get('numero_edital','')}", level=1)
    doc.add_paragraph(f"Data de Publicação: {campos.get('data_publicacao','')}")
    doc.add_paragraph(f"Unidade Solicitante: {campos.get('unidade_solicitante','')}")
    doc.add_paragraph(f"Responsável: {campos.get('responsavel','')}")
    doc.add_paragraph("")

    def bloco(titulo: str, corpo: str):
        doc.add_heading(titulo, level=2)
        doc.add_paragraph(corpo if corpo else "—")

    bloco("1. DO OBJETO", campos.get("objeto",""))
    bloco("2. DO TIPO E CRITÉRIO DE JULGAMENTO",
          f"Tipo: {campos.get('tipo_licitacao','')}. Critério: {campos.get('criterio_julgamento','')}.")
    bloco("3. DAS CONDIÇÕES DE PARTICIPAÇÃO", campos.get("condicoes_participacao",""))
    bloco("4. DAS EXIGÊNCIAS DE HABILITAÇÃO", campos.get("exigencias_habilitacao",""))
    bloco("5. DAS OBRIGAÇÕES DA CONTRATADA", campos.get("obrigacoes_contratada",""))
    bloco("6. DO PRAZO DE EXECUÇÃO", campos.get("prazo_execucao",""))
    bloco("7. DAS FONTES DE RECURSOS", campos.get("fontes_recursos",""))
    bloco("8. DO GESTOR/FISCAL DO CONTRATO", campos.get("gestor_fiscal",""))
    bloco("9. DAS DISPOSIÇÕES FINAIS", campos.get("observacoes_gerais",""))

    if texto_completo:
        doc.add_page_break()
        doc.add_heading("ANEXO – RASCUNHO INTEGRAL", level=2)
        for par in texto_completo.split("\n\n"):
            doc.add_paragraph(par)

    nome_arquivo = f"Edital_{campos.get('numero_edital','TJSP-PE')}.docx"
    caminho = str(EXPORTS_DIR / nome_arquivo)
    doc.save(caminho)
    return caminho


# ==========================================================
# 🚀 Função principal – chamada a partir da página Insumos
# ==========================================================
def processar_insumo_edital(arquivo, contexto_previo: dict = None, artefato: str = "EDITAL") -> dict:
    """
    1) Extrai texto do insumo.
    2) Integra contexto (DFD/ETP/TR).
    3) Chama IA para estruturar campos.
    4) Normaliza e gera rascunho + DOCX oficial.
    5) Retorna dicionário padronizado para a página.
    """
    texto = _extrair_texto_arquivo(arquivo)
    if not texto:
        return {"erro": "Falha na extração de texto do insumo de EDITAL."}

    modelos = ler_modelos_edital()
    campos_ia = _chamar_ia_edital(texto, modelos, contexto_previo or {})
    campos = _normalizar_campos(campos_ia if isinstance(campos_ia, dict) else {}, contexto_previo or {})

    # Rascunho textual + DOCX oficial
    rascunho = gerar_rascunho_edital(campos, modelos_referencia="")
    docx_path = gerar_edital_docx(campos, texto_completo=rascunho)

    print(f"[IA:EDITAL] Arquivo: {getattr(arquivo,'name','(sem nome)')} – Campos: {list(campos.keys())}")
    return {
        "artefato": artefato,
        "nome_arquivo": getattr(arquivo, "name", ""),
        "status": "processado",
        "campos_ai": campos,
        "docx_path": docx_path,
        "contexto_usado": list((contexto_previo or {}).keys())
    }
