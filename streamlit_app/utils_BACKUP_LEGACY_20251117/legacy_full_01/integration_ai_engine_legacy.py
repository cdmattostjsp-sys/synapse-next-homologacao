# ==========================================================
# utils/integration_ai_engine.py
# SynapseNext – SAAB / TJSP – IA Ativa v3.2
# ==========================================================
# Motor institucional de IA para pré-preenchimento de artefatos
# Compatível com DFD, ETP e TR – integrado ao ecossistema SynapseNext
# ==========================================================

from __future__ import annotations
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
import streamlit as st
from openai import OpenAI

# ==========================================================
# ⚙️ Configuração do cliente OpenAI
# ==========================================================
_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Retorna instância única do cliente OpenAI."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    return _client


# ==========================================================
# 🧰 Utilitários de extração de texto
# ==========================================================
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    import docx2txt
except Exception:
    docx2txt = None


def _extract_txt_from_pdf(file) -> str:
    """Extrai texto de PDF usando PyMuPDF."""
    if fitz is None:
        return ""
    try:
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            doc = fitz.open(stream=data, filetype="pdf")
        else:
            doc = fitz.open(stream=data.getvalue(), filetype="pdf")
        texts = [page.get_text() for page in doc]
        return "\n".join(texts)
    except Exception as e:
        st.error(f"Erro ao extrair PDF: {e}")
        return ""


def _extract_txt_from_docx(file) -> str:
    """Extrai texto de DOCX."""
    if docx2txt is None:
        return ""
    try:
        import io
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            bio = io.BytesIO(data)
            return docx2txt.process(bio)
        return docx2txt.process(file)
    except Exception as e:
        st.error(f"Erro ao extrair DOCX: {e}")
        return ""


def _extract_txt_from_plain(file) -> str:
    """Lê texto puro (TXT)."""
    try:
        data = file.read() if hasattr(file, "read") else file
        if isinstance(data, bytes):
            return data.decode("utf-8", errors="ignore")
        return str(data)
    except Exception as e:
        st.error(f"Erro ao ler TXT: {e}")
        return ""


def extrair_texto(uploaded_file) -> str:
    """Detecta o tipo de arquivo e extrai o texto bruto."""
    if uploaded_file is None:
        return ""
    name = getattr(uploaded_file, "name", "").lower()
    if name.endswith(".pdf"):
        return _extract_txt_from_pdf(uploaded_file)
    if name.endswith(".docx"):
        return _extract_txt_from_docx(uploaded_file)
    if name.endswith(".txt"):
        return _extract_txt_from_plain(uploaded_file)
    return _extract_txt_from_plain(uploaded_file)


# ==========================================================
# 📦 Modelo de retorno
# ==========================================================
@dataclass
class IAResultado:
    modulo: str
    campos: Dict[str, Any]
    lacunas: list[str]
    inferido_de: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "modulo": self.modulo,
            "campos_ai": self.campos,
            "lacunas": self.lacunas,
            "inferido_de": self.inferido_de,
        }


# ==========================================================
# 🧠 Montagem do prompt institucional
# ==========================================================
def _montar_prompt(modulo: str, texto: str, metadados: Dict[str, Any]) -> list[Dict[str, str]]:
    schema_comum = {
        "DFD": [
            "objeto",
            "justificativa",
            "resultados_esperados",
            "requisitos_minimos",
            "criterio_julgamento",
            "prazo_execucao",
            "base_legal",
        ],
        "ETP": [
            "objeto",
            "motivacao",
            "alternativas",
            "vantagem_da_solucao",
            "riscos",
            "estimativa_custos",
            "criterios_aceitacao",
            "base_legal",
        ],
        "TR": [
            "objeto",
            "escopo_detalhado",
            "requisitos_tecnicos",
            "condicoes_entrega",
            "indicadores_de_desempenho",
            "criterio_julgamento",
            "prazos",
            "garantias",
            "base_legal",
        ],
    }

    chaves = schema_comum.get(modulo.upper(), [])

    system = (
        "Você é redator técnico do SAAB/TJSP, especialista na Lei 14.133/2021. "
        "Seu trabalho é inferir campos administrativos a partir de insumos fornecidos. "
        "Responda ESTRITAMENTE em JSON válido (um único objeto) conforme o schema solicitado. "
        "Se um campo não puder ser inferido, deixe-o vazio e liste em 'lacunas'. "
        "Não adicione comentários fora do JSON."
    )

    user = (
        f"MÓDULO ALVO: {modulo}\n"
        f"METADADOS DO FORMULÁRIO:\n{json.dumps(metadados, ensure_ascii=False)}\n\n"
        f"EXTRATO DO INSUMO:\n{texto[:12000]}\n\n"
        f"RETORNE JSON COM AS CHAVES: {chaves}, incluindo 'lacunas'."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


# ==========================================================
# 🔄 Validação e coerção de JSON
# ==========================================================
def _coagir_json(conteudo: str) -> Dict[str, Any]:
    try:
        return json.loads(conteudo)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", conteudo)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {"raw": conteudo}


# ==========================================================
# 🧩 Função pública principal – processar_insumo
# ==========================================================
def processar_insumo(
    uploaded_file,
    tipo_artefato: str,
    metadados_form: Optional[Dict[str, Any]] = None,
    filename: Optional[str] = None,
) -> Dict[str, Any]:
    """Processa um insumo e retorna um dicionário JSON com campos inferidos."""
    modulo = (tipo_artefato or "").upper()
    metadados_form = metadados_form or {}

    texto = extrair_texto(uploaded_file)
    model = st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")

    try:
        st.info(f"🔍 Utilizando modelo IA: **{model}**")
        client = _get_client()
        messages = _montar_prompt(modulo, texto, metadados_form)

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
            max_tokens=2000,
        )
        conteudo = resp.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Falha na chamada IA: {e}")
        conteudo = json.dumps({
            "modulo": modulo,
            "campos": {},
            "lacunas": [f"Erro IA: {e}"],
        }, ensure_ascii=False)

    parsed = _coagir_json(conteudo)
    if "campos" not in parsed:
        parsed["campos"] = {}
    if "lacunas" not in parsed:
        parsed["lacunas"] = []

    resultado = IAResultado(
        modulo=modulo,
        campos=parsed.get("campos", {}),
        lacunas=parsed.get("lacunas", []),
        inferido_de={
            "arquivo": filename or getattr(uploaded_file, "name", None),
            "bytes": True,
        },
    ).to_dict()

    # ==========================================================
    # 💾 Salvar automaticamente para integração com DFD
    # ==========================================================
    out_dir = Path("exports") / "insumos" / "json"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{modulo}_ultimo.json"

    try:
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        st.success(f"💾 Resultado IA salvo em: {out_file}")
    except Exception as e:
        st.error(f"Erro ao salvar JSON: {e}")

    # Atualiza sessão
    key_map = {"DFD": "dfd_campos_ai", "ETP": "etp_campos_ai", "TR": "tr_campos_ai"}
    target_key = key_map.get(modulo)
    if target_key:
        st.session_state[target_key] = resultado.get("campos_ai", {})

    return resultado
