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
    # Prompt otimizado para Contrato (20 campos) - VERSÃO ROBUSTA
    # ==========================================================
    def _montar_prompt(self, contexto: dict = None) -> str:
        # Preparar contexto enriquecido
        contexto_detalhado = self._preparar_contexto_enriquecido(contexto)
        
        return f"""
Você é um REDATOR SÊNIOR de Contratos Administrativos do Tribunal de Justiça de São Paulo, especialista em Lei Federal nº 14.133/2021.

**MISSÃO CRÍTICA**: ELABORE um Contrato Administrativo COMPLETO, DETALHADO e PROFISSIONAL, consolidando TODAS as informações do documento fornecido E do contexto DFD/ETP/TR/Edital.

⚠️ **ATENÇÃO**: NÃO faça resumos genéricos. CADA CAMPO deve ter NO MÍNIMO 150-400 caracteres com informações ESPECÍFICAS e DETALHADAS.

{contexto_detalhado}

═══════════════════════════════════════════════════════════════════
📋 ESTRUTURA DO CONTRATO (20 CAMPOS OBRIGATÓRIOS)
═══════════════════════════════════════════════════════════════════

**1. numero_contrato** (FORMATO: XXX/AAAA)
   - Extrair do documento ou gerar baseado no ano atual
   - Exemplo: "245/2025" ou "TJSP-CONT-2025/134"

**2. data_assinatura** (FORMATO: DD/MM/AAAA)
   - Extrair do documento ou usar data estimada
   - Exemplo: "15/12/2025"

**3. objeto** ⭐ CAMPO CRÍTICO - MÍNIMO 400 CARACTERES
   - SINTETIZE: Especificação técnica do TR + Objeto do Edital + Objeto do DFD
   - INCLUA: Natureza da contratação (serviço/fornecimento/obra), quantitativos, local de execução
   - EXEMPLO REAL: "Contratação de empresa especializada para prestação de serviços continuados de limpeza, conservação e higienização das dependências dos Fóruns da Comarca de São Paulo, compreendendo: a) Limpeza geral de pisos, paredes, tetos, vidros, esquadrias, mobiliário e equipamentos; b) Higienização e desinfecção de sanitários, copas e áreas comuns; c) Coleta, transporte e destinação de resíduos sólidos; d) Fornecimento de materiais de limpeza, equipamentos e EPIs; e) Manutenção preventiva e corretiva dos equipamentos utilizados. Área total aproximada: 15.000m², distribuída em 8 prédios da Capital. Regime de execução: Empreitada por preço global. Fundamentação: arts. 6º, XXIII e 47, II da Lei 14.133/2021."

**4. partes_contratante** (PADRÃO INSTITUCIONAL TJSP)
   SEMPRE use: "TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO, pessoa jurídica de direito público, inscrito no CNPJ sob o nº 51.174.001/0001-50, com sede na Praça da Sé, s/nº, Centro, São Paulo/SP, CEP 01016-030, neste ato representado por seu Presidente, nos termos do art. 24 da Lei Complementar Estadual nº 646/1990, doravante denominado CONTRATANTE"

**5. partes_contratada** (EXTRAIR DO EDITAL/DOCUMENTO)
   - Razão social COMPLETA
   - CNPJ, Inscrição Estadual/Municipal
   - Endereço completo com CEP
   - Representante legal com CPF e RG
   - EXEMPLO: "EMPRESA XYZ SERVIÇOS LTDA, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº 12.345.678/0001-99, Inscrição Estadual nº 123.456.789.110, com sede na Rua Exemplo, nº 1000, Bairro Centro, Cidade/SP, CEP 01000-000, neste ato representada por seu sócio-administrador, Sr. João da Silva, portador do CPF nº 123.456.789-00 e RG nº 12.345.678-9 SSP/SP, doravante denominada CONTRATADA"

**6. fundamentacao_legal** ⭐ MÍNIMO 250 CARACTERES
   SEMPRE inclua:
   - Lei Federal nº 14.133/2021 (art. 92 e seguintes)
   - Processo administrativo completo (ex: Processo SEI nº 0012345-67.2025.8.26.0001)
   - Modalidade licitatória (Pregão Eletrônico nº XXX/2025)
   - Edital completo (Edital nº XXX/2025 e anexos)
   - Proposta vencedora (data, valor, item)
   - Dotação orçamentária específica
   - EXEMPLO: "Lei Federal nº 14.133/2021, especialmente arts. 92 a 136 (contratos administrativos); Processo Administrativo SEI nº 0012345-67.2025.8.26.0001; Pregão Eletrônico nº 045/2025, realizado em 10/11/2025; Edital nº 045/2025 e seus anexos (Termo de Referência, Planilha de Custos, Minuta Contratual); Ata de Julgamento de 15/11/2025; Proposta comercial da CONTRATADA datada de 05/11/2025, valor global de R$ 850.000,00; Dotação Orçamentária: 01.01.04.122.0001.2001.3390.39.00 - Fonte 100."

**7. vigencia** (SER ESPECÍFICO)
   - Data de início E término em DD/MM/AAAA
   - Duração em meses/anos
   - Possibilidade de prorrogação (art. 107 Lei 14.133/2021)
   - EXEMPLO: "O contrato terá vigência de 12 (doze) meses, contados da data de sua assinatura, com início previsto em 01/01/2026 e término em 31/12/2026, podendo ser prorrogado por iguais e sucessivos períodos, até o limite de 10 (dez) anos, conforme art. 107 da Lei Federal nº 14.133/2021, mediante termo aditivo e desde que comprovada a vantajosidade para a Administração."

**8. prazo_execucao** (DO TR/EDITAL)
   - Prazo ESPECÍFICO em dias corridos/úteis
   - Marco inicial (ordem de serviço/empenho/assinatura)
   - Etapas ou fases se houver
   - EXEMPLO: "A CONTRATADA deverá iniciar a execução dos serviços em até 5 (cinco) dias úteis contados do recebimento da Ordem de Serviço emitida pelo Gestor do Contrato. O prazo de execução será durante toda a vigência contratual, com prestação continuada dos serviços de limpeza e conservação, em regime de 8 horas diárias, 6 dias por semana (segunda a sábado), conforme cronograma estabelecido no Anexo I do Termo de Referência."

**9. valor_global** ⭐ USAR VALOR DO DFD/EDITAL
   - Valor EXATO em R$ (numérico e por extenso)
   - Mensal e total anual
   - Fonte: DFD > Edital > ETP
   - EXEMPLO: "O valor global do contrato é de R$ 850.000,00 (oitocentos e cinquenta mil reais), correspondente a R$ 70.833,33 (setenta mil, oitocentos e trinta e três reais e trinta e três centavos) mensais, para o período de 12 (doze) meses, conforme proposta da CONTRATADA e planilha de custos detalhada no Anexo II do Edital."

**10. forma_pagamento** ⭐ MÍNIMO 300 CARACTERES
    INCLUA:
    - Periodicidade (mensal, quinzenal, após entrega)
    - Documentação fiscal necessária (NF, relatórios)
    - Prazo para pagamento (dias após aprovação)
    - Glosas e descontos
    - Retenções tributárias
    - EXEMPLO: "O pagamento será efetuado mensalmente, até o 10º (décimo) dia útil do mês subsequente à prestação dos serviços, mediante apresentação de: a) Nota Fiscal Eletrônica discriminando os serviços executados; b) Relatório Mensal de Execução Contratual assinado pelo Fiscal; c) Certidões de regularidade fiscal (FGTS, INSS, Fazendas Federal/Estadual/Municipal) e trabalhista; d) Comprovante de pagamento dos salários, vale-transporte e vale-refeição dos empregados alocados; e) Guias de recolhimento do INSS e FGTS. O pagamento será efetuado mediante crédito em conta bancária indicada pela CONTRATADA. Serão retidos na fonte: ISS (conforme legislação municipal), IR, PIS, COFINS e CSLL (conforme IN RFB 1.234/2012). Havendo erro na Nota Fiscal ou irregularidade nas certidões, o prazo de pagamento será suspenso e reiniciado após regularização, sem ônus para o CONTRATANTE."

**11. reajuste** (LEI 14.133/2021 ART. 136)
     - Índice oficial (IPCA, INPC, IGP-M)
     - Periodicidade (anual a partir da assinatura)
     - Fórmula de cálculo
     - Vedações
     - EXEMPLO: "Os preços contratuais poderão ser reajustados após o 12º (décimo segundo) mês da data de apresentação da proposta, utilizando-se o Índice Nacional de Preços ao Consumidor Amplo (IPCA/IBGE), mediante aplicação da fórmula: R = Vo x (I - Io) / Io, onde R = valor do reajuste, Vo = valor original do contrato, I = índice de reajuste no mês de aplicação, Io = índice no mês da proposta. O reajuste será aplicado mediante solicitação expressa da CONTRATADA e aprovação do Gestor do Contrato, conforme art. 136 da Lei 14.133/2021. É vedado o reajuste parcial ou antecipado."

**12. garantia_contratual** (SE EXIGIDA NO EDITAL)
      - Tipo: caução, seguro-garantia, fiança bancária
      - Percentual sobre o valor do contrato (geralmente 5%)
      - Prazo de apresentação
      - Condições de liberação
      - EXEMPLO: "A CONTRATADA deverá prestar garantia de execução contratual no valor correspondente a 5% (cinco por cento) do valor global do contrato, no montante de R$ 42.500,00 (quarenta e dois mil e quinhentos reais), em até 10 (dez) dias após a assinatura, mediante uma das modalidades previstas no art. 96 da Lei 14.133/2021: caução em dinheiro, seguro-garantia ou fiança bancária. A garantia será liberada após o término da vigência contratual e cumprimento integral das obrigações, inclusive período de garantia dos serviços (90 dias), mediante requerimento da CONTRATADA e atestado favorável do Fiscal do Contrato."

**13. obrigacoes_contratada** ⭐⭐⭐ CAMPO CRÍTICO - MÍNIMO 800 CARACTERES
      DEVE SER EXTREMAMENTE DETALHADO - USE O EDITAL + TR
      Liste NO MÍNIMO 15 obrigações numeradas, incluindo:
      - Execução conforme especificações técnicas
      - Fornecimento de materiais/equipamentos/mão de obra
      - Responsabilidade por encargos trabalhistas/fiscais/previdenciários
      - Qualificação e treinamento de pessoal
      - Apresentação de relatórios e documentação
      - Substituição de produtos/profissionais inadequados
      - Manutenção das condições de habilitação
      - Seguros e responsabilidade civil
      - Sigilo e confidencialidade
      - Garantia dos serviços/produtos
      - EXEMPLO: "1) Executar os serviços de limpeza, conservação e higienização das dependências indicadas, conforme especificações técnicas do Termo de Referência, normas da ANVISA e legislação sanitária aplicável; 2) Fornecer todos os materiais de limpeza (detergentes, desinfetantes, sacos de lixo, papel higiênico, sabonetes, etc.) e equipamentos necessários (aspiradores, enceradeiras, escadas, carrinhos), com qualidade comprovada e em quantidade suficiente; 3) Disponibilizar equipe de 45 (quarenta e cinco) profissionais qualificados, sendo 40 auxiliares de limpeza, 3 encarregados e 2 supervisores, todos devidamente uniformizados, identificados e treinados; 4) Responsabilizar-se integralmente por todos os encargos trabalhistas, previdenciários, fiscais, comerciais e tributários decorrentes da execução do contrato, incluindo salários, 13º, férias, FGTS, INSS, vale-transporte, vale-alimentação, EPIs e uniformes; 5) Apresentar mensalmente até o 5º dia útil: relatório de execução dos serviços, lista de presença dos funcionários, comprovantes de pagamento de salários e benefícios, certidões de regularidade fiscal e trabalhista; 6) Substituir, no prazo máximo de 24 (vinte e quatro) horas, qualquer empregado cuja atuação, permanência ou comportamento seja julgado inconveniente, prejudicial, insatisfatório ou inseguro à disciplina do CONTRATANTE; 7) Refazer, às suas expensas e sem ônus adicional, os serviços executados em desacordo com as especificações técnicas ou que apresentem vícios, defeitos ou imperfeições; 8) Manter durante toda a vigência contratual as condições de habilitação e qualificação exigidas no Edital, apresentando anualmente ou quando solicitado as certidões de regularidade fiscal, trabalhista e previdenciária; 9) Manter seguro de responsabilidade civil com cobertura mínima de R$ 200.000,00 para danos materiais e corporais causados a terceiros; 10) Guardar sigilo absoluto sobre dados, informações, documentos e materiais de propriedade do CONTRATANTE aos quais tenha acesso, sob pena de responsabilização civil, penal e administrativa; 11) Acatar as orientações do Fiscal e Gestor do Contrato, executando de imediato as correções apontadas; 12) Coletar, segregar, transportar e destinar adequadamente os resíduos sólidos gerados, conforme Política Nacional de Resíduos Sólidos (Lei 12.305/2010); 13) Fornecer EPIs adequados aos trabalhadores e exigir sua utilização, conforme NRs do Ministério do Trabalho; 14) Comunicar ao Fiscal do Contrato, por escrito, qualquer anormalidade que impeça ou dificulte a execução dos serviços; 15) Reparar ou indenizar danos causados ao patrimônio do CONTRATANTE ou de terceiros, por culpa ou dolo de seus empregados ou prepostos."

**14. obrigacoes_contratante** ⭐ MÍNIMO 400 CARACTERES
      Liste NO MÍNIMO 8 obrigações, incluindo:
      - Fornecer informações necessárias
      - Permitir acesso às dependências
      - Efetuar pagamentos
      - Fiscalizar a execução
      - EXEMPLO: "1) Proporcionar todas as facilidades para que a CONTRATADA possa cumprir suas obrigações dentro das normas e condições contratuais; 2) Permitir o livre acesso dos empregados da CONTRATADA, devidamente identificados e uniformizados, às dependências dos Fóruns objeto da prestação dos serviços, nos horários estabelecidos; 3) Fornecer água e energia elétrica necessárias à execução dos serviços, bem como pontos de tomada para conexão de equipamentos; 4) Disponibilizar local adequado para guarda de materiais, produtos de limpeza e equipamentos da CONTRATADA; 5) Indicar formalmente o Gestor e Fiscal do Contrato, com suas respectivas atribuições, conforme art. 117 da Lei 14.133/2021; 6) Fiscalizar a execução dos serviços, anotando em registro próprio as ocorrências, falhas e irregularidades constatadas, determinando as correções necessárias; 7) Efetuar os pagamentos devidos nas condições e prazos estabelecidos, mediante apresentação da documentação fiscal e comprobatória exigida; 8) Comunicar oficialmente à CONTRATADA qualquer irregularidade na execução dos serviços, estipulando prazo para correção; 9) Aplicar as sanções administrativas cabíveis em caso de descumprimento contratual, garantido o contraditório e a ampla defesa; 10) Prestar as informações e esclarecimentos que venham a ser solicitados pela CONTRATADA."

**15. fiscalizacao** ⭐ MÍNIMO 300 CARACTERES
      - Nomear Gestor E Fiscal do Contrato
      - Atribuições específicas de cada um
      - Periodicidade de fiscalização
      - Instrumentos de controle
      - EXEMPLO: "A fiscalização e gestão do contrato serão exercidas nos termos dos arts. 117 e 140 da Lei Federal nº 14.133/2021, sendo designados: GESTOR DO CONTRATO: [Nome completo], matrícula TJSP nº [XXXXXX], cargo [Diretor/Chefe], responsável pelos aspectos administrativos, contratuais e orçamentários, incluindo acompanhamento de prazos, análise de aditivos, aplicação de sanções e controle de pagamentos. FISCAL DO CONTRATO: [Nome completo], matrícula TJSP nº [YYYYYY], cargo [Analista/Técnico], responsável pelo acompanhamento técnico da execução dos serviços, verificação de conformidade com especificações do TR, atestação de notas fiscais e elaboração de relatórios mensais de fiscalização. A fiscalização será exercida diariamente in loco, com inspeções programadas e aleatórias, registro em sistema informatizado, reuniões mensais com a CONTRATADA e aplicação de check-lists de qualidade conforme padrões da ANVISA e normas técnicas ABNT."

**16. penalidades** ⭐⭐ MÍNIMO 600 CARACTERES
      BASEADO NO ART. 156 DA LEI 14.133/2021 - SEJA DETALHADO
      Inclua:
      - Advertência (infrações leves)
      - Multas (percentuais específicos por tipo de infração)
      - Suspensão temporária
      - Declaração de inidoneidade
      - Condições de aplicação
      - EXEMPLO: "Pelo descumprimento total ou parcial das obrigações contratuais, a CONTRATADA estará sujeita às seguintes sanções, conforme art. 156 da Lei Federal nº 14.133/2021, garantidos o contraditório e a ampla defesa: a) ADVERTÊNCIA: por escrito, em caso de faltas leves que não causem prejuízo à Administração, como atrasos pontuais na entrega de documentos ou pequenas irregularidades sanáveis; b) MULTA DE MORA: 0,3% (três décimos por cento) ao dia sobre o valor mensal do contrato, limitada a 10% do valor total, por atraso injustificado na execução dos serviços, contado a partir do 1º dia de inadimplência; c) MULTA COMPENSATÓRIA: 10% (dez por cento) sobre o valor total do contrato, em caso de inexecução total ou rescisão por culpa da CONTRATADA, sem prejuízo da apuração de perdas e danos; d) MULTAS ESPECÍFICAS: 0,5% sobre o valor mensal por empregado não reposto em 24h; 1% por não fornecimento de material de limpeza; 2% por ausência de uniforme/identificação; 5% por descumprimento de normas de segurança do trabalho; 3% por não apresentação de certidões de regularidade; e) SUSPENSÃO TEMPORÁRIA: impedimento de contratar com a Administração Pública por até 2 (dois) anos, em caso de faltas graves como prestação de informações falsas, fraude, adulteração de documentos ou reincidência em infrações anteriormente punidas; f) DECLARAÇÃO DE INIDONEIDADE: impedimento de contratar com qualquer órgão da Administração Pública enquanto perdurarem os motivos determinantes da punição ou até reabilitação, aplicável em casos de faltas gravíssimas com dano ao erário ou lesão ao interesse público. As multas serão descontadas da garantia contratual, dos pagamentos devidos ou, se necessário, cobradas judicialmente. As sanções poderão ser aplicadas cumulativamente."

**17. rescisao** ⭐ MÍNIMO 400 CARACTERES
      BASEADO NOS ARTS. 137-138 DA LEI 14.133/2021
      Inclua:
      - Hipóteses de rescisão unilateral pela Administração
      - Rescisão amigável
      - Rescisão judicial
      - Procedimentos
      - EXEMPLO: "O contrato poderá ser rescindido nas seguintes hipóteses previstas nos arts. 137 e 138 da Lei Federal nº 14.133/2021: I) RESCISÃO UNILATERAL pela Administração, independentemente de interpelação judicial ou extrajudicial: a) não cumprimento ou cumprimento irregular de cláusulas contratuais; b) lentidão ou paralisação dos serviços sem justa causa; c) desatendimento às determinações da fiscalização; d) cometimento reiterado de faltas na execução; e) decretação de falência ou dissolução da empresa; f) alteração social que implique inidoneidade; g) razões de interesse público justificadas; h) ocorrência de caso fortuito ou força maior que impeça a execução; II) RESCISÃO AMIGÁVEL por acordo entre as partes, mediante autorização escrita e fundamentada da autoridade competente; III) RESCISÃO JUDICIAL requerida pela CONTRATADA nos casos de supressão além dos limites legais, suspensão superior a 120 dias ou atraso superior a 90 dias nos pagamentos. A rescisão unilateral será precedida de procedimento administrativo assegurando contraditório e ampla defesa. A CONTRATADA reconhece os direitos da Administração previstos no art. 137, §1º da Lei 14.133/2021."

**18. alteracoes** (ART. 124 LEI 14.133/2021)
      - Condições para aditivos
      - Limites legais de acréscimo/supressão
      - Procedimentos
      - EXEMPLO: "O contrato poderá ser alterado, com as devidas justificativas, nas seguintes hipóteses previstas no art. 124 da Lei Federal nº 14.133/2021: a) unilateralmente pela Administração: modificação do projeto ou especificações para melhor adequação técnica; acréscimo ou supressão de até 25% do valor inicial atualizado (ou 50% no caso de reforma de edifício); b) por acordo entre as partes: substituição da garantia contratual; modificação do regime de execução ou forma de pagamento; restabelecimento do equilíbrio econômico-financeiro; suspensão temporária da execução. As alterações serão formalizadas mediante Termo Aditivo, precedidas de justificativa técnica, parecer jurídico favorável e autorização da autoridade competente. É vedada alteração que desvirtue o objeto original do contrato."

**19. foro** (PADRÃO INSTITUCIONAL)
      SEMPRE: "Comarca de São Paulo/SP"
      EXEMPLO: "Fica eleito o Foro da Comarca de São Paulo, Capital do Estado de São Paulo, com expressa renúncia a qualquer outro, por mais privilegiado que seja, para dirimir questões oriundas do presente contrato que não possam ser resolvidas administrativamente."

**20. disposicoes_gerais** ⭐ MÍNIMO 300 CARACTERES
      Inclua:
      - Vinculação ao Edital e anexos
      - Publicação (art. 94 Lei 14.133/2021)
      - Documentos integrantes
      - Sucessão
      - Vedações (subcontratação, cessão)
      - EXEMPLO: "1) O presente contrato vincula-se integralmente aos termos do Edital de Pregão Eletrônico nº 045/2025, seus anexos (Termo de Referência, Planilha de Custos, Minuta Contratual) e à proposta da CONTRATADA, independentemente de transcrição; 2) O contrato será publicado no Diário Oficial do Estado de São Paulo e no Portal Nacional de Contratações Públicas (PNCP) como condição de eficácia, conforme art. 94 da Lei 14.133/2021; 3) Integram o contrato: Anexo I - Termo de Referência; Anexo II - Planilha de Custos e Formação de Preços; Anexo III - Cronograma de Execução; Anexo IV - Modelo de Relatório Mensal; 4) A CONTRATADA não poderá subcontratar, ceder ou transferir, total ou parcialmente, o objeto do contrato, sem prévia e expressa anuência do CONTRATANTE; 5) As sucessoras ou cessionárias da CONTRATADA assumirão todos os direitos e obrigações do contrato; 6) Os casos omissos serão resolvidos à luz da Lei Federal nº 14.133/2021 e demais normas aplicáveis; 7) Quaisquer tolerâncias ou concessões recíprocas não importarão em novação, mantendo-se íntegras todas as cláusulas contratuais."

═══════════════════════════════════════════════════════════════════
⚠️ INSTRUÇÕES CRÍTICAS DE REDAÇÃO
═══════════════════════════════════════════════════════════════════

1. **NUNCA USE TEXTOS GENÉRICOS** do tipo "conforme estabelecido", "a definir", "nos termos da lei"
2. **SEMPRE SEJA ESPECÍFICO**: datas, valores, nomes, números de processo, artigos de lei
3. **COMBINE MÚLTIPLAS FONTES**: TR + Edital + DFD + ETP para ENRIQUECER cada campo
4. **CAMPOS 3, 10, 13, 16 SÃO CRÍTICOS**: devem ter 400-800 caracteres CADA
5. **USE LISTAS NUMERADAS**: para obrigações e penalidades (facilita leitura)
6. **CITE ARTIGOS DA LEI 14.133/2021**: dá credibilidade jurídica
7. **MANTENHA COERÊNCIA**: valores, prazos e informações devem bater entre os campos
8. **NÃO INVENTE DADOS**: se não houver informação no documento/contexto, use padrões TJSP realistas

═══════════════════════════════════════════════════════════════════
📤 FORMATO DE SAÍDA (JSON PURO)
═══════════════════════════════════════════════════════════════════

Retorne APENAS o JSON abaixo, sem comentários, sem markdown, sem explicações:

{{
  "numero_contrato": "",
  "data_assinatura": "",
  "objeto": "",
  "partes_contratante": "",
  "partes_contratada": "",
  "fundamentacao_legal": "",
  "vigencia": "",
  "prazo_execucao": "",
  "valor_global": "",
  "forma_pagamento": "",
  "reajuste": "",
  "garantia_contratual": "",
  "obrigacoes_contratada": "",
  "obrigacoes_contratante": "",
  "fiscalizacao": "",
  "penalidades": "",
  "rescisao": "",
  "alteracoes": "",
  "foro": "Comarca de São Paulo/SP",
  "disposicoes_gerais": ""
}}
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
