#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_edital_agent.py - Teste local do EditalAgent
Valida extração dos 12 campos estruturados do Edital
"""

import sys
from pathlib import Path

# Ajustar path para importar agents
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from agents.edital_agent import processar_edital_com_ia


def test_edital_agent():
    """Testa EditalAgent com texto de exemplo."""
    
    # Texto de exemplo de um Edital
    texto_exemplo = """
EDITAL DE PREGÃO ELETRÔNICO Nº 2025/001-TJSP
Data de Publicação: 08/12/2025

TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO
SECRETARIA DE ADMINISTRAÇÃO

1. DO OBJETO

Contratação de serviços especializados de manutenção preventiva e corretiva de sistemas de climatização 
das unidades do Tribunal de Justiça de São Paulo (TJSP), incluindo fornecimento de peças, 
mão de obra qualificada e relatórios técnicos.

2. DO TIPO E CRITÉRIO DE JULGAMENTO

Tipo de licitação: Pregão Eletrônico
Critério de julgamento: Menor preço global
Regime de execução: Empreitada por preço global

3. DAS CONDIÇÕES DE PARTICIPAÇÃO

Poderão participar desta licitação empresas especializadas do ramo pertinente ao objeto licitado,
regularmente estabelecidas no País, que atendam às exigências deste Edital.

4. DAS EXIGÊNCIAS DE HABILITAÇÃO

Registro comercial, no caso de empresa individual;
Ato constitutivo, estatuto ou contrato social em vigor;
Prova de regularidade fiscal (FGTS, INSS, Fazendas);
Certidão negativa de falência ou recuperação judicial.

5. DAS OBRIGAÇÕES DA CONTRATADA

Executar os serviços conforme especificações técnicas;
Fornecer mão de obra qualificada e materiais adequados;
Manter equipe técnica disponível para atendimento emergencial;
Emitir relatórios técnicos mensais sobre os serviços executados.

6. DO PRAZO DE EXECUÇÃO

O prazo de vigência do contrato será de 12 (doze) meses, contados da assinatura, 
podendo ser prorrogado nos termos da Lei 14.133/2021.

7. DAS FONTES DE RECURSOS

Dotação Orçamentária: 02.122.0571.4256.0001
Fonte: Recursos Ordinários - Tesouro do Estado
Elemento de Despesa: 3.3.90.39 - Outros Serviços de Terceiros - Pessoa Jurídica

8. DO GESTOR E FISCAL DO CONTRATO

Gestor: Marcelo Donadon - Diretor do Departamento de Administração
Fiscal Técnico: João Silva - Engenheiro Responsável

9. OBSERVAÇÕES GERAIS

Os licitantes deverão realizar vistoria técnica prévia nas unidades do TJSP.
Não será admitida a participação de empresas em consórcio.
As propostas deverão ter validade mínima de 60 dias.

São Paulo, 08 de dezembro de 2025.

[Assinatura]
Dr. Roberto Santos
Secretário de Administração - TJSP
"""
    
    print("=" * 70)
    print("🧪 TESTE DO EditalAgent")
    print("=" * 70)
    
    # Processar com EditalAgent
    resultado = processar_edital_com_ia(texto_exemplo)
    
    # Verificar resultado
    if "erro" in resultado:
        print(f"\n❌ ERRO: {resultado['erro']}")
        return False
    
    # Extrair Edital
    edital = resultado.get("EDITAL", {})
    
    print(f"\n📊 Artefato: {resultado.get('artefato', 'N/A')}")
    print(f"🕐 Timestamp: {resultado.get('timestamp', 'N/A')}")
    print(f"\n📋 Campos extraídos:\n")
    
    campos_preenchidos = 0
    for i, (campo, conteudo) in enumerate(edital.items(), 1):
        status = "✅" if conteudo and conteudo.strip() else "❌"
        if conteudo and conteudo.strip():
            campos_preenchidos += 1
        
        # Mostrar preview do conteúdo (primeiros 80 chars)
        preview = conteudo[:80] + "..." if len(conteudo) > 80 else conteudo
        print(f"{status} {i}. {campo}:")
        if preview:
            print(f"   {preview}\n")
        else:
            print(f"   (vazio)\n")
    
    print("=" * 70)
    print(f"📊 Resultado: {campos_preenchidos}/12 campos preenchidos")
    print("=" * 70)
    
    # Validação
    if campos_preenchidos >= 10:  # Esperamos pelo menos 10/12 campos
        print("\n✅ TESTE PASSOU - EditalAgent extraiu corretamente os campos!")
        return True
    else:
        print(f"\n⚠️ TESTE FALHOU - Apenas {campos_preenchidos}/12 campos preenchidos")
        return False


if __name__ == "__main__":
    sucesso = test_edital_agent()
    sys.exit(0 if sucesso else 1)
