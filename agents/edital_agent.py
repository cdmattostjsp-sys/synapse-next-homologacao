# ==========================================================
# agents/edital_agent.py — AGENTE ESPECÍFICO PARA EDITAL
# Extração estruturada de Editais de Licitação (Lei 14.133/2021)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


# 12 campos padronizados do Edital (Lei 14.133/2021)
CAMPOS_EDITAL = [
    "objeto",                       # 1
    "tipo_licitacao",              # 2
    "criterio_julgamento",         # 3
    "condicoes_participacao",      # 4
    "exigencias_habilitacao",      # 5
    "obrigacoes_contratada",       # 6
    "prazo_execucao",              # 7
    "fontes_recursos",             # 8
    "gestor_fiscal",               # 9
    "observacoes_gerais",          # 10
    "numero_edital",               # 11
    "data_publicacao",             # 12
]


class EditalAgent:
    """
    Agente especializado em extrair e estruturar Editais de Licitação.
    Otimizado para identificar os 12 campos padronizados.
    """

    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[EditalAgent] ERRO ao inicializar AIClient: {e}")
            self.ai = None

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str, contexto_previo: dict = None) -> dict:
        """
        Processa o texto do Edital e retorna estrutura completa com 12 campos.
        
        Args:
            conteudo_base: texto bruto extraído do PDF/DOCX
            contexto_previo: dados de DFD/ETP/TR para enriquecer (opcional)
        """
        
        # Verificar se AIClient foi inicializado
        if self.ai is None:
            return {
                "erro": "AIClient não disponível. Verifique OPENAI_API_KEY.",
                "EDITAL": self._get_template_vazio()
            }

        prompt = self._montar_prompt(contexto_previo)

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="EDITAL",
        )

        # AIClient.ask() já retorna dict estruturado
        if isinstance(resposta, dict):
            dados = resposta
        elif isinstance(resposta, str):
            # Fallback: tentar parsear JSON string
            try:
                dados = json.loads(resposta)
            except json.JSONDecodeError:
                print("[EditalAgent] ERRO: resposta não é JSON válido")
                dados = {}
        else:
            print(f"[EditalAgent] ERRO: tipo de resposta inesperado: {type(resposta)}")
            dados = {}

        # Estrutura final do Edital
        edital_estruturado = self._extrair_campos(dados, contexto_previo)
        
        return {
            "artefato": "EDITAL",
            "timestamp": datetime.now().isoformat(),
            "EDITAL": edital_estruturado,
        }

    # ==========================================================
    # Prompt otimizado para Edital (12 campos)
    # ==========================================================
    def _montar_prompt(self, contexto: dict = None) -> str:
        contexto_texto = ""
        if contexto:
            contexto_texto = f"""

**CONTEXTO DISPONÍVEL (DFD/ETP/TR):**
{json.dumps(contexto, ensure_ascii=False, indent=2)}

Use este contexto para enriquecer os campos do edital quando relevante.
"""

        return f"""
Você é um especialista em Editais de Licitação do setor público (Lei 14.133/2021).

**TAREFA**: Extraia os 12 campos padronizados do Edital abaixo e retorne em JSON.
{contexto_texto}

**CAMPOS DO EDITAL:**
1. objeto (descrição do que será licitado)
2. tipo_licitacao (pregão eletrônico, concorrência, etc.)
3. criterio_julgamento (menor preço, melhor técnica, etc.)
4. condicoes_participacao (requisitos para participar)
5. exigencias_habilitacao (documentação necessária)
6. obrigacoes_contratada (deveres da empresa vencedora)
7. prazo_execucao (tempo de vigência do contrato)
8. fontes_recursos (origem orçamentária)
9. gestor_fiscal (responsável pelo acompanhamento)
10. observacoes_gerais (informações complementares)
11. numero_edital (identificação única)
12. data_publicacao (data de divulgação)

**FORMATO DE SAÍDA (JSON):**
```json
{{
  "objeto": "texto extraído",
  "tipo_licitacao": "texto extraído",
  "criterio_julgamento": "texto extraído",
  "condicoes_participacao": "texto extraído",
  "exigencias_habilitacao": "texto extraído",
  "obrigacoes_contratada": "texto extraído",
  "prazo_execucao": "texto extraído",
  "fontes_recursos": "texto extraído",
  "gestor_fiscal": "texto extraído",
  "observacoes_gerais": "texto extraído",
  "numero_edital": "texto extraído",
  "data_publicacao": "texto extraído"
}}
```

**REGRAS:**
- Extraia APENAS o que existe no documento
- NÃO invente informações
- Se um campo não existir, deixe vazio ""
- Use contexto DFD/ETP/TR quando disponível para complementar
- Campos como número_edital e data_publicacao podem ser inferidos do cabeçalho
- Campos 1-6 devem ser detalhados, campos 7-12 mais sintéticos

Retorne APENAS o JSON, sem comentários.
"""

    # ==========================================================
    # Extração de campos do JSON
    # ==========================================================
    def _extrair_campos(self, dados: dict, contexto: dict = None) -> dict:
        """
        Extrai os 12 campos do JSON retornado pela IA.
        Enriquece com contexto DFD/ETP/TR quando disponível.
        """
        resultado = {}
        
        # Extrair dados do contexto (se disponível)
        dfd = (contexto or {}).get("dfd_campos_ai", {}) if contexto else {}
        etp = (contexto or {}).get("etp_campos_ai", {}) if contexto else {}
        tr = (contexto or {}).get("tr_campos_ai", {}) if contexto else {}
        
        # Helper: pegar primeiro valor não vazio
        def first_nonempty(*vals):
            for v in vals:
                if isinstance(v, str) and v.strip():
                    return v.strip()
            return ""
        
        for campo in CAMPOS_EDITAL:
            # Tentar extrair do documento primeiro
            valor = dados.get(campo, "")
            
            # Se vazio, tentar enriquecer com contexto
            if not valor or not valor.strip():
                if campo == "objeto":
                    valor = first_nonempty(tr.get("objeto"), etp.get("objeto"), dfd.get("objeto"))
                elif campo == "prazo_execucao":
                    valor = first_nonempty(tr.get("prazo_execucao"), etp.get("prazo_estimado"))
                elif campo == "fontes_recursos":
                    valor = first_nonempty(tr.get("fonte_recurso"))
                elif campo == "gestor_fiscal":
                    valor = first_nonempty(dfd.get("responsavel"), etp.get("responsavel"))
                elif campo == "obrigacoes_contratada":
                    valor = first_nonempty(tr.get("especificacao_tecnica"))
            
            # Limpar e validar
            if isinstance(valor, str):
                resultado[campo] = valor.strip()
            else:
                resultado[campo] = ""
        
        # Gerar número e data automáticos se não existirem
        if not resultado.get("numero_edital"):
            hoje = datetime.now()
            resultado["numero_edital"] = f"TJSP-PE-{hoje.year}-{hoje.strftime('%m%d')}"
        
        if not resultado.get("data_publicacao"):
            resultado["data_publicacao"] = datetime.now().strftime("%d/%m/%Y")
        
        return resultado

    # ==========================================================
    # Template vazio (fallback)
    # ==========================================================
    def _get_template_vazio(self) -> dict:
        """Retorna estrutura vazia do Edital."""
        return {campo: "" for campo in CAMPOS_EDITAL}


# ==========================================================
# Função wrapper para integração (compatível com UI)
# ==========================================================
def processar_edital_com_ia(conteudo_textual: str, contexto_previo: dict = None) -> dict:
    """
    Wrapper para processar Edital com IA.
    Compatível com utils/integration_edital.py
    
    Args:
        conteudo_textual: texto bruto extraído do PDF
        contexto_previo: dict com dados de DFD/ETP/TR (opcional)
    
    Returns:
        dict com estrutura: {"artefato": "EDITAL", "EDITAL": {...12 campos...}}
    """
    try:
        agent = EditalAgent()
        resultado = agent.generate(conteudo_textual, contexto_previo)
        return resultado
    except Exception as e:
        print(f"[processar_edital_com_ia] EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return {
            "erro": f"Falha ao processar Edital com IA: {e}",
            "conteudo_recebido": conteudo_textual[:500] if conteudo_textual else "",
        }
