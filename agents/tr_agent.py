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
Você é um especialista em Termos de Referência do TJSP (Lei 14.133/2021).

**TAREFA**: Extraia as 9 seções padronizadas do TR e retorne em JSON estruturado.

**INSTRUÇÕES CRÍTICAS:**
1. **IDENTIFIQUE o tipo de documento** (TR próprio, Edital de Licitação, ETP, DFD, Contrato)
2. **EXTRAIA todas as informações disponíveis** - NÃO deixe campos vazios se houver dados no documento
3. **Se o documento for um EDITAL DE LICITAÇÃO:**
   - objeto → Seção "OBJETO" do edital (descrição COMPLETA da licitação)
   - justificativa_tecnica → Seção "JUSTIFICATIVA" ou contexto que fundamenta a necessidade
   - especificacao_tecnica → Seções "ESPECIFICAÇÕES TÉCNICAS", "REQUISITOS", "DESCRIÇÃO TÉCNICA" (detalhamento completo)
   - criterios_julgamento → Seção "CRITÉRIOS DE JULGAMENTO" ou "CRITÉRIOS DE ACEITAÇÃO" (menor preço, melhor técnica, etc.)
   - riscos → Seção "RISCOS", "PENALIDADES" ou inferir de cláusulas contratuais
   - observacoes_finais → Seção "DISPOSIÇÕES FINAIS", "OBSERVAÇÕES", "INFORMAÇÕES COMPLEMENTARES"
   - prazo_execucao → Seção "PRAZO DE EXECUÇÃO", "VIGÊNCIA", "CRONOGRAMA" (extrair prazos)
   - estimativa_valor → Seção "VALOR ESTIMADO", "ORÇAMENTO", valores em R$ (se não houver: "Valor não divulgado no edital")
   - fonte_recurso → Seção "DOTAÇÃO ORÇAMENTÁRIA", "FONTE DE RECURSOS", classificação orçamentária

4. **Se o documento for um ETP ou DFD:**
   - objeto → Seção "OBJETO" ou "DESCRIÇÃO DA NECESSIDADE"
   - justificativa_tecnica → Seções "JUSTIFICATIVA", "MOTIVAÇÃO", "FUNDAMENTAÇÃO"
   - especificacao_tecnica → Seções "ESPECIFICAÇÕES", "REQUISITOS TÉCNICOS", "DESCRIÇÃO TÉCNICA"
   - criterios_julgamento → Seções "CRITÉRIOS", "AVALIAÇÃO"
   - riscos → Seção "RISCOS", "ANÁLISE DE RISCOS"
   - prazo_execucao → Seção "PRAZO", "CRONOGRAMA"
   - estimativa_valor → Seção "ESTIMATIVA DE VALOR", "VALOR ESTIMADO"
   - fonte_recurso → Seção "RECURSOS ORÇAMENTÁRIOS", "DOTAÇÃO"

5. **Para CADA SEÇÃO do TR:**
   - Extraia o MÁXIMO de informação possível
   - Se a informação não estiver explícita mas puder ser INFERIDA logicamente do contexto, faça isso
   - NUNCA deixe vazio se houver dados no documento
   - Seja DETALHADO e COMPLETO - não resuma excessivamente

6. **MAPEAMENTO ESPECÍFICO PARA EDITAIS:**
   - Objeto → Procure por "DO OBJETO", "OBJETO DA LICITAÇÃO", cabeçalho
   - Justificativa Técnica → Procure por "JUSTIFICATIVA", "DOS MOTIVOS", contexto introdutório
   - Especificações Técnicas → Procure por "ESPECIFICAÇÕES", "DESCRIÇÃO TÉCNICA", "ANEXOS TÉCNICOS"
   - Critérios de Julgamento → Procure por "CRITÉRIO DE JULGAMENTO", "TIPO DE LICITAÇÃO"
   - Riscos → Procure por "PENALIDADES", "SANÇÕES", "INADIMPLÊNCIA"
   - Observações → Procure por "DISPOSIÇÕES FINAIS", "INFORMAÇÕES COMPLEMENTARES"
   - Prazo → Procure por "PRAZO DE EXECUÇÃO", "VIGÊNCIA DO CONTRATO"
   - Valor → Procure por "VALOR ESTIMADO", "VALOR MÁXIMO ACEITÁVEL", números com R$
   - Fonte → Procure por "DOTAÇÃO ORÇAMENTÁRIA", "CLASSIFICAÇÃO ORÇAMENTÁRIA", códigos orçamentários

**FORMATO DE SAÍDA (JSON):**
```json
{
  "objeto": "Descrição COMPLETA e DETALHADA do objeto da contratação extraída do documento",
  "justificativa_tecnica": "Justificativa COMPLETA da necessidade da contratação com fundamentação técnica",
  "especificacao_tecnica": "Especificações técnicas DETALHADAS dos serviços/produtos a contratar",
  "criterios_julgamento": "Critérios claros de julgamento das propostas (menor preço, melhor técnica, etc.)",
  "riscos": "Riscos identificados e medidas de mitigação (se não houver: 'Não identificados riscos específicos')",
  "observacoes_finais": "Observações complementares, disposições finais, informações adicionais",
  "prazo_execucao": "Prazo de execução em meses/dias (ex: '12 meses', '180 dias')",
  "estimativa_valor": "Valor estimado em R$ (ex: 'R$ 150.000,00' ou 'Valor não divulgado')",
  "fonte_recurso": "Dotação orçamentária ou fonte de recursos (ex: 'Recursos Próprios - Dotação 33.90.39')"
}
```

**REGRAS FINAIS:**
- Extraia TODO o conteúdo relevante - seja COMPLETO e DETALHADO
- Se uma seção não existir no documento, deixe ""
- NÃO invente informações que não existem no documento
- Mantenha a estrutura JSON válida
- Seções 1-6 devem ter texto LONGO e DETALHADO (mínimo 2-3 parágrafos quando houver conteúdo)
- Seções 7-9 devem ser sintéticas mas precisas (prazo, valor, fonte)
- Se o documento for muito completo (Edital, ETP), TODAS as seções devem ficar ricas em informação

Retorne APENAS o JSON, sem comentários ou explicações adicionais.
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
