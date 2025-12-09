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
        # Preparar contexto enriquecido
        contexto_detalhado = self._preparar_contexto_enriquecido(contexto)
        
        return f"""
Você é um especialista em Editais de Licitação do setor público brasileiro (Lei 14.133/2021).

**TAREFA**: ELABORE um Edital completo e robusto usando o documento fornecido E o contexto dos documentos anteriores (DFD/ETP/TR).

{contexto_detalhado}

**CAMPOS DO EDITAL (12 campos obrigatórios):**

1. **objeto**: Descrição detalhada do objeto da licitação. Use informações do TR e DFD para enriquecer.
2. **tipo_licitacao**: Modalidade (Pregão Eletrônico, Concorrência, etc.)
3. **criterio_julgamento**: Critério (Menor Preço, Melhor Técnica e Preço, etc.)
4. **condicoes_participacao**: Requisitos para participar. Exemplo: credenciamento SICAF, regularidade fiscal, enquadramento ME/EPP, etc.
5. **exigencias_habilitacao**: Documentação obrigatória (habilitação jurídica, fiscal, trabalhista, técnica, econômico-financeira). SEJA ESPECÍFICO usando o TR como base.
6. **obrigacoes_contratada**: Responsabilidades da empresa. Use especificações técnicas do TR e obrigações do Contrato (se disponível).
7. **prazo_execucao**: Vigência do contrato (meses/dias). Extraia do TR ou DFD.
8. **fontes_recursos**: Origem orçamentária (rubrica, programa, natureza de despesa).
9. **gestor_fiscal**: Nome e cargo do responsável pelo acompanhamento do contrato.
10. **observacoes_gerais**: Informações complementares (horário de atendimento, garantia contratual, reajustes, etc.)
11. **numero_edital**: Identificação do edital (ex: 90207/2025)
12. **data_publicacao**: Data de divulgação (formato DD/MM/YYYY)

**FORMATO DE SAÍDA (JSON):**
```json
{{
  "objeto": "Texto completo e detalhado do objeto",
  "tipo_licitacao": "Modalidade",
  "criterio_julgamento": "Critério",
  "condicoes_participacao": "Lista detalhada de condições",
  "exigencias_habilitacao": "Lista completa de documentos e requisitos técnicos",
  "obrigacoes_contratada": "Lista detalhada de obrigações e responsabilidades",
  "prazo_execucao": "Vigência do contrato",
  "fontes_recursos": "Origem orçamentária",
  "gestor_fiscal": "Nome e cargo",
  "observacoes_gerais": "Informações complementares",
  "numero_edital": "Número de identificação",
  "data_publicacao": "DD/MM/YYYY"
}}
```

**INSTRUÇÕES CRÍTICAS:**
1. **SINTETIZE**: Combine informações do documento atual COM o contexto DFD/ETP/TR
2. **DETALHE**: Campos 4, 5 e 6 devem ser extremamente detalhados (use bullet points quando apropriado)
3. **ENRIQUEÇA**: Se o Edital não tiver detalhes, busque no TR/ETP/DFD
4. **ESTRUTURE**: Use formatação clara (listas numeradas/bullets) para legibilidade
5. **COMPLETO**: Nenhum campo pode ficar vazio - use contexto para preencher
6. **LEGAL**: Mencione artigos da Lei 14.133/2021 quando relevante

**EXEMPLO DE BOM OUTPUT (campo "exigencias_habilitacao"):**
"Habilitação Jurídica: ato constitutivo, CNPJ, prova de representação legal. Qualificação Técnica: atestado de capacidade técnica comprovando execução de serviços similares (manutenção elétrica em MT/BT), registro no CREA. Qualificação Econômico-Financeira: balanço patrimonial, certidões negativas INSS/FGTS/Fazenda. Regularidade Fiscal: CND Federal, Estadual, Municipal, CNDT-TST."

Retorne APENAS o JSON, sem comentários ou markdown.
"""
    
    def _preparar_contexto_enriquecido(self, contexto: dict = None) -> str:
        """Prepara resumo estruturado do contexto DFD/ETP/TR."""
        if not contexto:
            return "**ATENÇÃO**: Nenhum contexto DFD/ETP/TR disponível. Baseie-se apenas no documento fornecido."
        
        dfd = contexto.get("dfd_campos_ai", {})
        etp = contexto.get("etp_campos_ai", {})
        tr = contexto.get("tr_campos_ai", {})
        
        resumo = ["**CONTEXTO DISPONÍVEL DOS DOCUMENTOS ANTERIORES:**", ""]
        
        # DFD
        if dfd:
            resumo.append("📋 **DFD (Documento de Formalização da Demanda):**")
            if dfd.get("objeto"):
                resumo.append(f"  - Objeto: {dfd['objeto'][:200]}")
            if dfd.get("justificativa"):
                resumo.append(f"  - Justificativa: {dfd['justificativa'][:200]}")
            if dfd.get("valor_estimado"):
                resumo.append(f"  - Valor estimado: {dfd['valor_estimado']}")
            resumo.append("")
        
        # ETP
        if etp:
            resumo.append("📐 **ETP (Estudo Técnico Preliminar):**")
            if etp.get("objeto"):
                resumo.append(f"  - Objeto: {etp['objeto'][:200]}")
            if etp.get("prazo_estimado"):
                resumo.append(f"  - Prazo: {etp['prazo_estimado']}")
            if etp.get("resultados_pretendidos"):
                resumo.append(f"  - Resultados: {etp['resultados_pretendidos'][:200]}")
            resumo.append("")
        
        # TR
        if tr:
            resumo.append("📄 **TR (Termo de Referência):**")
            if tr.get("objeto"):
                resumo.append(f"  - Objeto: {tr['objeto'][:200]}")
            if tr.get("especificacao_tecnica"):
                resumo.append(f"  - Especificação técnica: {tr['especificacao_tecnica'][:300]}")
            if tr.get("prazo_execucao"):
                resumo.append(f"  - Prazo: {tr['prazo_execucao']}")
            if tr.get("fonte_recurso"):
                resumo.append(f"  - Fonte de recursos: {tr['fonte_recurso']}")
            resumo.append("")
        
        resumo.append("**USE ESSAS INFORMAÇÕES PARA ENRIQUECER O EDITAL.**")
        
        return "\n".join(resumo)

    # ==========================================================
    # Extração de campos do JSON
    # ==========================================================
    def _extrair_campos(self, dados: dict, contexto: dict = None) -> dict:
        """
        Extrai os 12 campos do JSON retornado pela IA.
        Aplica enriquecimento AGRESSIVO com contexto DFD/ETP/TR.
        """
        resultado = {}
        
        # Extrair dados do contexto (se disponível)
        dfd = (contexto or {}).get("dfd_campos_ai", {}) if contexto else {}
        etp = (contexto or {}).get("etp_campos_ai", {}) if contexto else {}
        tr = (contexto or {}).get("tr_campos_ai", {}) if contexto else {}
        
        # Helper: concatenar valores relevantes
        def merge_values(*vals):
            """Concatena valores não vazios com separador."""
            result = []
            for v in vals:
                if isinstance(v, str) and v.strip() and v.strip() not in result:
                    result.append(v.strip())
            return " | ".join(result) if result else ""
        
        for campo in CAMPOS_EDITAL:
            # Sempre pegar valor da IA primeiro
            valor_ia = dados.get(campo, "")
            
            # Enriquecimento condicional POR CAMPO
            if campo == "objeto":
                # Objeto: combinar TR + ETP + DFD
                valor = merge_values(
                    valor_ia,
                    tr.get("objeto"),
                    etp.get("objeto"),
                    dfd.get("objeto")
                ) or valor_ia
                
            elif campo == "exigencias_habilitacao":
                # Habilitação: usar TR (especificações técnicas) + contexto
                valor = valor_ia or merge_values(
                    tr.get("especificacao_tecnica"),
                    tr.get("qualificacao_tecnica"),
                    etp.get("requisitos_solucao")
                )
                
            elif campo == "obrigacoes_contratada":
                # Obrigações: TR (especificações) é essencial
                valor = valor_ia or merge_values(
                    tr.get("especificacao_tecnica"),
                    tr.get("obrigacoes"),
                    etp.get("descricao_solucao")
                )
                
            elif campo == "prazo_execucao":
                # Prazo: TR > ETP > DFD
                valor = valor_ia or merge_values(
                    tr.get("prazo_execucao"),
                    etp.get("prazo_estimado"),
                    dfd.get("prazo")
                )
                
            elif campo == "fontes_recursos":
                # Recursos: TR > DFD
                valor = valor_ia or merge_values(
                    tr.get("fonte_recurso"),
                    dfd.get("dotacao_orcamentaria"),
                    dfd.get("valor_estimado")
                )
                
            elif campo == "gestor_fiscal":
                # Gestor: DFD > ETP > TR
                valor = valor_ia or merge_values(
                    dfd.get("responsavel"),
                    etp.get("responsavel"),
                    tr.get("fiscal")
                )
                
            elif campo == "condicoes_participacao":
                # Condições: se IA não preencheu, usar padrão TJSP
                valor = valor_ia or "Poderão participar interessados previamente credenciados no Sistema de Cadastramento Unificado de Fornecedores - SICAF e no portal de compras governamental, com situação regular."
                
            else:
                # Demais campos: usar valor da IA diretamente
                valor = valor_ia
            
            # Limpar e validar
            if isinstance(valor, str):
                resultado[campo] = valor.strip()
            else:
                resultado[campo] = str(valor).strip() if valor else ""
        
        # Gerar número e data automáticos se não existirem
        if not resultado.get("numero_edital") or resultado["numero_edital"] == "":
            # Tentar extrair do TR/DFD
            numero = (tr.get("numero") or etp.get("numero") or dfd.get("numero") or "").strip()
            if not numero:
                hoje = datetime.now()
                numero = f"TJSP-PE-{hoje.year}-{hoje.strftime('%m%d')}"
            resultado["numero_edital"] = numero
        
        if not resultado.get("data_publicacao") or resultado["data_publicacao"] == "":
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
