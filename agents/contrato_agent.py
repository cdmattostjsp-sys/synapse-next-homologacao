# ==========================================================
# agents/contrato_agent.py — AGENTE ESPECÍFICO PARA CONTRATO
# Extração estruturada de Contratos Administrativos (Lei 14.133/2021)
# ==========================================================

from __future__ import annotations

import json
from datetime import datetime
from utils.ai_client import AIClient


# 20 campos padronizados do Contrato (Lei 14.133/2021)
CAMPOS_CONTRATO = [
    "numero_contrato",           # 1
    "data_assinatura",           # 2
    "objeto",                    # 3
    "partes_contratante",        # 4
    "partes_contratada",         # 5
    "fundamentacao_legal",       # 6
    "vigencia",                  # 7
    "prazo_execucao",            # 8
    "valor_global",              # 9
    "forma_pagamento",           # 10
    "reajuste",                  # 11
    "garantia_contratual",       # 12
    "obrigacoes_contratada",     # 13
    "obrigacoes_contratante",    # 14
    "fiscalizacao",              # 15
    "penalidades",               # 16
    "rescisao",                  # 17
    "alteracoes",                # 18
    "foro",                      # 19
    "disposicoes_gerais",        # 20
]


class ContratoAgent:
    """
    Agente especializado em extrair e estruturar Contratos Administrativos.
    Otimizado para identificar os 20 campos padronizados.
    """

    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception as e:
            print(f"[ContratoAgent] ERRO ao inicializar AIClient: {e}")
            self.ai = None

    # ==========================================================
    # Processamento principal
    # ==========================================================
    def generate(self, conteudo_base: str, contexto_previo: dict = None) -> dict:
        """
        Processa o texto do Contrato e retorna estrutura completa com 20 campos.
        
        Args:
            conteudo_base: texto bruto extraído do PDF/DOCX
            contexto_previo: dados de DFD/ETP/TR/Edital para enriquecer (opcional)
        """
        
        # Verificar se AIClient foi inicializado
        if self.ai is None:
            return {
                "erro": "AIClient não disponível. Verifique OPENAI_API_KEY.",
                "CONTRATO": self._get_template_vazio()
            }

        prompt = self._montar_prompt(contexto_previo)

        resposta = self.ai.ask(
            prompt=prompt,
            conteudo=conteudo_base,
            artefato="CONTRATO",
        )

        # AIClient.ask() já retorna dict estruturado
        if isinstance(resposta, dict):
            dados = resposta
        elif isinstance(resposta, str):
            # Fallback: tentar parsear JSON string
            try:
                dados = json.loads(resposta)
            except json.JSONDecodeError:
                print("[ContratoAgent] ERRO: resposta não é JSON válido")
                dados = {}
        else:
            print(f"[ContratoAgent] ERRO: tipo de resposta inesperado: {type(resposta)}")
            dados = {}

        # Estrutura final do Contrato
        contrato_estruturado = self._extrair_campos(dados, contexto_previo)
        
        return {
            "artefato": "CONTRATO",
            "timestamp": datetime.now().isoformat(),
            "CONTRATO": contrato_estruturado,
        }

    # ==========================================================
    # Prompt otimizado para Contrato (20 campos)
    # ==========================================================
    def _montar_prompt(self, contexto: dict = None) -> str:
        # Preparar contexto enriquecido
        contexto_detalhado = self._preparar_contexto_enriquecido(contexto)
        
        return f"""
Você é um especialista em Contratos Administrativos do setor público brasileiro (Lei 14.133/2021).

**TAREFA**: ELABORE um Contrato completo e robusto usando o documento fornecido E o contexto dos documentos anteriores (DFD/ETP/TR/Edital).

{contexto_detalhado}

**CAMPOS DO CONTRATO (20 campos obrigatórios):**

1. **numero_contrato**: Identificação única (ex: 123/2025)
2. **data_assinatura**: Data de formalização (formato DD/MM/YYYY)
3. **objeto**: Descrição detalhada do objeto da contratação (use TR + Edital)
4. **partes_contratante**: CONTRATANTE - Tribunal de Justiça de São Paulo (dados completos)
5. **partes_contratada**: CONTRATADA - Empresa vencedora (razão social, CNPJ, endereço)
6. **fundamentacao_legal**: Base legal (Lei 14.133/2021, processo licitatório, etc.)
7. **vigencia**: Período de validade do contrato (início e fim)
8. **prazo_execucao**: Prazo para execução dos serviços/fornecimento
9. **valor_global**: Valor total do contrato (R$)
10. **forma_pagamento**: Condições, prazos, documentação necessária para pagamento
11. **reajuste**: Índice, periodicidade, condições de reajuste (IPCA, IGP-M, etc.)
12. **garantia_contratual**: Tipo e percentual de garantia exigida
13. **obrigacoes_contratada**: Lista DETALHADA de responsabilidades e deveres da empresa
14. **obrigacoes_contratante**: Lista de responsabilidades da Administração
15. **fiscalizacao**: Gestor e fiscal do contrato, atribuições, controles
16. **penalidades**: Sanções administrativas por descumprimento (art. 156 Lei 14.133/2021)
17. **rescisao**: Hipóteses e procedimentos de rescisão contratual
18. **alteracoes**: Condições para aditivos contratuais (art. 124 Lei 14.133/2021)
19. **foro**: Foro competente para dirimir controvérsias
20. **disposicoes_gerais**: Cláusulas finais, publicação, anexos, etc.

**FORMATO DE SAÍDA (JSON):**
```json
{{
  "numero_contrato": "XXX/YYYY",
  "data_assinatura": "DD/MM/YYYY",
  "objeto": "Descrição completa do objeto",
  "partes_contratante": "TJSP com endereço e dados",
  "partes_contratada": "Empresa com CNPJ e endereço",
  "fundamentacao_legal": "Lei 14.133/2021, art. X, Processo XXX/YYYY",
  "vigencia": "DD/MM/YYYY a DD/MM/YYYY (X meses)",
  "prazo_execucao": "X dias/meses",
  "valor_global": "R$ XXX.XXX,XX",
  "forma_pagamento": "Mensalmente mediante apresentação de nota fiscal...",
  "reajuste": "Anual pelo IPCA/IGP-M conforme...",
  "garantia_contratual": "5% do valor em seguro-garantia/caução",
  "obrigacoes_contratada": "Lista numerada de obrigações",
  "obrigacoes_contratante": "Lista de obrigações do TJSP",
  "fiscalizacao": "Gestor: [nome], Fiscal: [nome]",
  "penalidades": "Advertência, multas (X%), suspensão, declaração de inidoneidade",
  "rescisao": "Hipóteses dos arts. 137-138 da Lei 14.133/2021",
  "alteracoes": "Mediante termo aditivo conforme art. 124",
  "foro": "Comarca de São Paulo/SP",
  "disposicoes_gerais": "Publicação, vinculação ao edital, anexos"
}}
```

**INSTRUÇÕES CRÍTICAS:**
1. **SINTETIZE**: Combine informações do documento atual COM contexto DFD/ETP/TR/Edital
2. **DETALHE**: Campos 13, 14, 16 devem ser extremamente detalhados (use bullet points)
3. **ENRIQUEÇA**: Use objeto do TR, valores do Edital, prazos do ETP
4. **ESTRUTURE**: Use formatação clara (listas numeradas) para obrigações e penalidades
5. **COMPLETO**: Nenhum campo pode ficar vazio - use contexto para preencher
6. **LEGAL**: Mencione artigos da Lei 14.133/2021 quando relevante
7. **PADRÃO TJSP**: Use foro "Comarca de São Paulo/SP" sempre

**EXEMPLO DE BOM OUTPUT (campo "obrigacoes_contratada"):**
"1) Executar os serviços conforme especificações do TR; 2) Responsabilizar-se por todos os encargos trabalhistas, previdenciários, fiscais e comerciais; 3) Manter equipe qualificada e uniformizada; 4) Apresentar relatórios mensais; 5) Substituir profissionais inadequados em 24h; 6) Manter as condições de habilitação durante a vigência; 7) Reparar defeitos às suas expensas; 8) Manter sigilo sobre informações do TJSP."

Retorne APENAS o JSON, sem comentários ou markdown.
"""
    
    def _preparar_contexto_enriquecido(self, contexto: dict = None) -> str:
        """Prepara resumo estruturado do contexto DFD/ETP/TR/Edital."""
        if not contexto:
            return "**ATENÇÃO**: Nenhum contexto DFD/ETP/TR/Edital disponível. Baseie-se apenas no documento fornecido."
        
        dfd = contexto.get("dfd_campos_ai", {})
        etp = contexto.get("etp_campos_ai", {})
        tr = contexto.get("tr_campos_ai", {})
        edital = contexto.get("edital_campos_ai", {})
        
        resumo = ["**CONTEXTO DISPONÍVEL DOS DOCUMENTOS ANTERIORES:**", ""]
        
        # DFD
        if dfd:
            resumo.append("📋 **DFD (Documento de Formalização da Demanda):**")
            if dfd.get("objeto"):
                resumo.append(f"  - Objeto: {dfd['objeto'][:200]}")
            if dfd.get("valor_estimado"):
                resumo.append(f"  - Valor estimado: {dfd['valor_estimado']}")
            if dfd.get("responsavel"):
                resumo.append(f"  - Responsável: {dfd['responsavel']}")
            resumo.append("")
        
        # ETP
        if etp:
            resumo.append("📐 **ETP (Estudo Técnico Preliminar):**")
            if etp.get("prazo_estimado"):
                resumo.append(f"  - Prazo estimado: {etp['prazo_estimado']}")
            if etp.get("resultados_pretendidos"):
                resumo.append(f"  - Resultados: {etp['resultados_pretendidos'][:150]}")
            resumo.append("")
        
        # TR
        if tr:
            resumo.append("📄 **TR (Termo de Referência):**")
            if tr.get("objeto"):
                resumo.append(f"  - Objeto: {tr['objeto'][:200]}")
            if tr.get("especificacao_tecnica"):
                resumo.append(f"  - Especificação: {tr['especificacao_tecnica'][:250]}")
            if tr.get("prazo_execucao"):
                resumo.append(f"  - Prazo: {tr['prazo_execucao']}")
            if tr.get("fonte_recurso"):
                resumo.append(f"  - Recursos: {tr['fonte_recurso']}")
            resumo.append("")
        
        # Edital
        if edital:
            resumo.append("📜 **Edital:**")
            if edital.get("numero_edital"):
                resumo.append(f"  - Número: {edital['numero_edital']}")
            if edital.get("tipo_licitacao"):
                resumo.append(f"  - Modalidade: {edital['tipo_licitacao']}")
            if edital.get("criterio_julgamento"):
                resumo.append(f"  - Critério: {edital['criterio_julgamento']}")
            if edital.get("obrigacoes_contratada"):
                resumo.append(f"  - Obrigações (referência): {edital['obrigacoes_contratada'][:200]}")
            resumo.append("")
        
        resumo.append("**USE ESSAS INFORMAÇÕES PARA ENRIQUECER O CONTRATO.**")
        
        return "\n".join(resumo)

    # ==========================================================
    # Extração de campos do JSON
    # ==========================================================
    def _extrair_campos(self, dados: dict, contexto: dict = None) -> dict:
        """
        Extrai os 20 campos do JSON retornado pela IA.
        Aplica enriquecimento AGRESSIVO com contexto DFD/ETP/TR/Edital.
        """
        resultado = {}
        
        # Extrair dados do contexto (se disponível)
        dfd = (contexto or {}).get("dfd_campos_ai", {}) if contexto else {}
        etp = (contexto or {}).get("etp_campos_ai", {}) if contexto else {}
        tr = (contexto or {}).get("tr_campos_ai", {}) if contexto else {}
        edital = (contexto or {}).get("edital_campos_ai", {}) if contexto else {}
        
        # Helper: concatenar valores relevantes
        def merge_values(*vals):
            """Concatena valores não vazios com separador."""
            result = []
            for v in vals:
                if isinstance(v, str) and v.strip() and v.strip() not in result:
                    result.append(v.strip())
            return " | ".join(result) if result else ""
        
        for campo in CAMPOS_CONTRATO:
            # Sempre pegar valor da IA primeiro
            valor_ia = dados.get(campo, "")
            
            # Enriquecimento condicional POR CAMPO
            if campo == "objeto":
                # Objeto: combinar TR + Edital + ETP + DFD
                valor = merge_values(
                    valor_ia,
                    tr.get("objeto"),
                    edital.get("objeto"),
                    etp.get("objeto"),
                    dfd.get("objeto")
                ) or valor_ia
                
            elif campo == "valor_global":
                # Valor: DFD > ETP > Edital
                valor = valor_ia or merge_values(
                    dfd.get("valor_estimado"),
                    etp.get("valor_estimado"),
                    edital.get("fontes_recursos")
                )
                
            elif campo == "prazo_execucao" or campo == "vigencia":
                # Prazos: TR > ETP > Edital
                valor = valor_ia or merge_values(
                    tr.get("prazo_execucao"),
                    etp.get("prazo_estimado"),
                    edital.get("prazo_execucao")
                )
                
            elif campo == "obrigacoes_contratada":
                # Obrigações: TR + Edital (essenciais)
                valor = valor_ia or merge_values(
                    edital.get("obrigacoes_contratada"),
                    tr.get("especificacao_tecnica"),
                    tr.get("obrigacoes")
                )
                
            elif campo == "fiscalizacao":
                # Fiscal: Edital > DFD
                valor = valor_ia or merge_values(
                    edital.get("gestor_fiscal"),
                    dfd.get("responsavel")
                )
                
            elif campo == "fundamentacao_legal":
                # Legal: Edital + processo
                numero_edital = edital.get("numero_edital", "")
                valor = valor_ia or f"Lei Federal nº 14.133/2021, Edital nº {numero_edital}" if numero_edital else "Lei Federal nº 14.133/2021"
                
            elif campo == "foro":
                # Foro: padrão TJSP
                valor = valor_ia or "Comarca de São Paulo/SP"
                
            elif campo == "partes_contratante":
                # TJSP padrão
                valor = valor_ia or "TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO, pessoa jurídica de direito público, CNPJ 51.174.001/0001-50, com sede na Praça da Sé, s/nº, Centro, São Paulo/SP"
                
            else:
                # Demais campos: usar valor da IA diretamente
                valor = valor_ia
            
            # Limpar e validar
            if isinstance(valor, str):
                resultado[campo] = valor.strip()
            else:
                resultado[campo] = str(valor).strip() if valor else ""
        
        # Gerar número e data automáticos se não existirem
        if not resultado.get("numero_contrato") or resultado["numero_contrato"] == "":
            hoje = datetime.now()
            resultado["numero_contrato"] = f"TJSP-CONT-{hoje.year}-{hoje.strftime('%m%d%H%M')}"
        
        if not resultado.get("data_assinatura") or resultado["data_assinatura"] == "":
            resultado["data_assinatura"] = datetime.now().strftime("%d/%m/%Y")
        
        return resultado

    # ==========================================================
    # Template vazio (fallback)
    # ==========================================================
    def _get_template_vazio(self) -> dict:
        """Retorna estrutura vazia do Contrato."""
        return {campo: "" for campo in CAMPOS_CONTRATO}


# ==========================================================
# Função wrapper para integração (compatível com UI)
# ==========================================================
def processar_contrato_com_ia(conteudo_textual: str, contexto_previo: dict = None) -> dict:
    """
    Wrapper para processar Contrato com IA.
    Compatível com utils/integration_contrato.py
    
    Args:
        conteudo_textual: texto bruto extraído do PDF
        contexto_previo: dict com dados de DFD/ETP/TR/Edital (opcional)
    
    Returns:
        dict com estrutura: {"artefato": "CONTRATO", "CONTRATO": {...20 campos...}}
    """
    try:
        agent = ContratoAgent()
        resultado = agent.generate(conteudo_textual, contexto_previo)
        return resultado
    except Exception as e:
        print(f"[processar_contrato_com_ia] EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return {
            "erro": f"Falha ao processar Contrato com IA: {e}",
            "conteudo_recebido": conteudo_textual[:500] if conteudo_textual else "",
        }
