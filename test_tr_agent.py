#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_tr_agent.py - Teste local do TRAgent
Valida extração das 9 seções estruturadas do TR
"""

import sys
from pathlib import Path

# Ajustar path para importar agents
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from agents.tr_agent import processar_tr_com_ia


def test_tr_agent():
    """Testa TRAgent com texto de exemplo."""
    
    # Texto de exemplo (fragmento do TR fornecido pelo usuário)
    texto_exemplo = """
**TERMO DE REFERÊNCIA**

**1. OBJETO**

O presente Termo de Referência tem por objeto a contratação de serviços de manutenção preventiva e corretiva de sistemas de climatização das unidades do Tribunal de Justiça de São Paulo (TJSP), visando garantir o pleno funcionamento e a eficiência dos equipamentos, assegurando o conforto e a saúde dos servidores e usuários.

**2. JUSTIFICATIVA TÉCNICA**

A manutenção adequada dos sistemas de climatização é essencial para a preservação das condições ambientais necessárias ao desempenho das atividades judiciais e administrativas.

**3. ESPECIFICAÇÃO TÉCNICA**

Os serviços a serem contratados incluem, mas não se limitam a:
- Manutenção preventiva programada, com inspeções periódicas e limpeza dos sistemas de climatização;
- Manutenção corretiva, com reparos e substituição de peças danificadas;

**4. CRITÉRIOS DE JULGAMENTO**

A seleção da proposta será realizada com base no critério de menor preço, desde que atendidas todas as exigências técnicas e administrativas estabelecidas no edital.

**5. RISCOS**

Os principais riscos identificados na execução deste contrato incluem:
- Falhas na execução dos serviços, que podem comprometer o funcionamento dos sistemas de climatização;
- Atrasos na entrega dos serviços, que podem afetar o ambiente de trabalho;

**6. OBSERVAÇÕES FINAIS**

É imprescindível que a empresa contratada mantenha um canal de comunicação aberto com a equipe técnica do TJSP.

**7. PRAZO DE EXECUÇÃO**

O prazo para a execução dos serviços será de 12 (doze) meses.

**8. ESTIMATIVA DE VALOR**

A estimativa de valor para a contratação dos serviços é de R$ 150.000,00 (cento e cinquenta mil reais).

**9. FONTE DE RECURSO**

Os recursos para a contratação dos serviços serão provenientes do orçamento da Secretaria da Administração do Tribunal de Justiça de São Paulo.
"""
    
    print("=" * 70)
    print("🧪 TESTE DO TRAgent")
    print("=" * 70)
    
    # Processar com TRAgent
    resultado = processar_tr_com_ia(texto_exemplo)
    
    # Verificar resultado
    if "erro" in resultado:
        print(f"\n❌ ERRO: {resultado['erro']}")
        return False
    
    # Extrair TR
    tr = resultado.get("TR", {})
    
    print(f"\n📊 Artefato: {resultado.get('artefato', 'N/A')}")
    print(f"🕐 Timestamp: {resultado.get('timestamp', 'N/A')}")
    print(f"\n📋 Seções extraídas:\n")
    
    secoes_preenchidas = 0
    for i, (secao, conteudo) in enumerate(tr.items(), 1):
        status = "✅" if conteudo and conteudo.strip() else "❌"
        if conteudo and conteudo.strip():
            secoes_preenchidas += 1
        
        # Mostrar preview do conteúdo (primeiros 100 chars)
        preview = conteudo[:100] + "..." if len(conteudo) > 100 else conteudo
        print(f"{status} {i}. {secao}:")
        if preview:
            print(f"   {preview}\n")
        else:
            print(f"   (vazio)\n")
    
    print("=" * 70)
    print(f"📊 Resultado: {secoes_preenchidas}/9 seções preenchidas")
    print("=" * 70)
    
    # Validação
    if secoes_preenchidas >= 8:  # Esperamos pelo menos 8/9 seções
        print("\n✅ TESTE PASSOU - TRAgent extraiu corretamente as seções!")
        return True
    else:
        print(f"\n⚠️ TESTE FALHOU - Apenas {secoes_preenchidas}/9 seções preenchidas")
        return False


if __name__ == "__main__":
    sucesso = test_tr_agent()
    sys.exit(0 if sucesso else 1)
