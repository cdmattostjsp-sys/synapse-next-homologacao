# ==========================================================
# agents/tr_agent.py — AGENTE ESPECÍFICO PARA TR
# Extração estruturada de Termos de Referência (Lei 14.133/2021)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


# 9 seções padronizadas do TR (Lei 14.133/2021 + padrão TJSP)
SECOES_TR = [
    "objeto",                       # 1
    "justificativa_tecnica",        # 2
    "especificacao_tecnica",        # 3
    "criterios_julgamento",         # 4
    "riscos",                       # 5
    "observacoes_finais",           # 6
    "prazo_execucao",               # 7
    "estimativa_valor",             # 8
    "fonte_recurso",                # 9
]


class TRAgent:
    """
    Agente especializado em extrair e estruturar TRs (Termos de Referência).
    Otimizado para identificar as 9 seções padronizadas.
    """

    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[TRAgent] ERRO ao inicializar AIClient: {e}")
            self.ai = None

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str) -> dict:
        """
        Processa o texto do TR e retorna estrutura completa com 9 seções.
        """
        
        # Verificar se AIClient foi inicializado
        if self.ai is None:
            return {
                "erro": "AIClient não disponível. Verifique OPENAI_API_KEY.",
                "TR": self._get_template_vazio()
            }

        prompt = self._montar_prompt()

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="TR",
        )

        # AIClient.ask() já retorna dict estruturado
        if isinstance(resposta, dict):
            dados = resposta
        elif isinstance(resposta, str):
            # Fallback: tentar parsear JSON string
            try:
                dados = json.loads(resposta)
            except json.JSONDecodeError:
                print("[TRAgent] ERRO: resposta não é JSON válido")
                dados = {}
        else:
            print(f"[TRAgent] ERRO: tipo de resposta inesperado: {type(resposta)}")
            dados = {}

        # Estrutura final do TR
        tr_estruturado = self._extrair_secoes(dados)
        
        return {
            "artefato": "TR",
            "timestamp": datetime.now().isoformat(),
            "TR": tr_estruturado,
        }

    # ==========================================================
    # Prompt otimizado para TR (9 seções)
    # ==========================================================
    def _montar_prompt(self) -> str:
        return """
Você é um especialista em Termos de Referência do setor público (Lei 14.133/2021).

**TAREFA**: Extraia as 9 seções padronizadas do TR abaixo e retorne em JSON.

**SEÇÕES DO TR:**
1. objeto
2. justificativa_tecnica
3. especificacao_tecnica
4. criterios_julgamento
5. riscos
6. observacoes_finais
7. prazo_execucao
8. estimativa_valor
9. fonte_recurso

**FORMATO DE SAÍDA (JSON):**
```json
{
  "objeto": "texto extraído da seção 1",
  "justificativa_tecnica": "texto extraído da seção 2",
  "especificacao_tecnica": "texto extraído da seção 3",
  "criterios_julgamento": "texto extraído da seção 4",
  "riscos": "texto extraído da seção 5",
  "observacoes_finais": "texto extraído da seção 6",
  "prazo_execucao": "texto extraído da seção 7",
  "estimativa_valor": "texto extraído da seção 8",
  "fonte_recurso": "texto extraído da seção 9"
}
```

**REGRAS:**
- Extraia APENAS o que existe no documento
- NÃO invente informações
- Se uma seção não existir, deixe vazio ""
- Mantenha a estrutura JSON válida
- Seções 7-9 devem ser sintéticas (prazo, valor, fonte)
- Seções 1-6 podem ter texto mais longo

Retorne APENAS o JSON, sem comentários.
"""

    # ==========================================================
    # Extração de seções do JSON
    # ==========================================================
    def _extrair_secoes(self, dados: dict) -> dict:
        """
        Extrai as 9 seções do JSON retornado pela IA.
        """
        resultado = {}
        
        for secao in SECOES_TR:
            # Buscar seção no JSON
            valor = dados.get(secao, "")
            
            # Limpar e validar
            if isinstance(valor, str):
                resultado[secao] = valor.strip()
            else:
                resultado[secao] = ""
        
        return resultado

    # ==========================================================
    # Template vazio (fallback)
    # ==========================================================
    def _get_template_vazio(self) -> dict:
        """Retorna estrutura vazia do TR."""
        return {secao: "" for secao in SECOES_TR}


# ==========================================================
# Função wrapper para integração (compatível com UI)
# ==========================================================
def processar_tr_com_ia(conteudo_textual: str) -> dict:
    """
    Wrapper para processar TR com IA.
    Compatível com utils/integration_tr.py
    
    Args:
        conteudo_textual: texto bruto extraído do PDF
    
    Returns:
        dict com estrutura: {"artefato": "TR", "TR": {...9 seções...}}
    """
    try:
        agent = TRAgent()
        resultado = agent.generate(conteudo_textual)
        
        # ✅ NOVO: Registrar evento de auditoria
        try:
            from utils.audit_logger import registrar_evento_auditoria
            word_count = len(conteudo_textual.split())
            char_count = len(conteudo_textual)
            registrar_evento_auditoria(
                artefato="TR",
                word_count=word_count,
                char_count=char_count,
                etapa="processamento",
                conteudo_textual=conteudo_textual
            )
        except Exception as e:
            print(f"[processar_tr_com_ia] ⚠️ Falha ao registrar auditoria: {e}")
        
        return resultado
    except Exception as e:
        print(f"[processar_tr_com_ia] EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return {
            "erro": f"Falha ao processar TR com IA: {e}",
            "conteudo_recebido": conteudo_textual[:500],
        }
