#!/usr/bin/env python3
# ==========================================================
# test_etp_agent.py - Teste local do ETPAgent
# ==========================================================

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_etp_agent():
    """Testa o ETPAgent com texto real de ETP"""
    print("=" * 70)
    print("TESTE: ETPAgent com texto de ETP real")
    print("=" * 70)
    
    from agents.etp_agent import ETPAgent
    
    texto_etp_real = """
    ESTUDO TÉCNICO PRELIMINAR (Lei 14.133/2021)
    
    1. OBJETO
    Contratação de empresa especializada para a execução de serviços para adequação da 
    acessibilidade, incluindo as disciplinas de hidráulica, elétrica, estrutura e sistemas 
    mecânicos no prédio do Fórum da Comarca de Rio Claro, situado na Av. Ulysses Guimarães, 
    2800 - Vila Alemã - Rio Claro/SP.
    
    2. DESCRIÇÃO DA NECESSIDADE DA CONTRATAÇÃO
    O edifício é composto por 3 pavimentos (térreo + 2 andares) com sistema construtivo 
    convencional, formado por estrutura de concreto armado, vedações em tijolos cerâmicos 
    e esquadrias metálicas. O Fórum possui área descoberta destinada ao estacionamento.
    
    4. PLANEJAMENTO ESTRATÉGICO
    A presente demanda está em conformidade com o Planejamento Estratégico 2021-2026 do 
    Tribunal de Justiça e atende ao "Objetivo 3 - Aumentar a satisfação pessoal e profissional 
    dos agentes públicos no ambiente de trabalho" e ao "Objetivo 9 - Adequar a infraestrutura 
    física dos prédios".
    
    13. ESTIMATIVA DE VALOR DA CONTRATAÇÃO
    O custo do valor da contratação, estimado em R$ 400.000,00 (quatrocentos mil Reais), 
    será consolidado quando da finalização da planilha orçamentária.
    
    25. EQUIPE DE PLANEJAMENTO DA CONTRATAÇÃO
    
    Unidade solicitante: Serviço de Administração do Prédio do Fórum de Rio Claro
    Secretaria/Diretoria responsável: SAAB – Secretaria de Administração e Abastecimento
    Gestor ou Gestora de Planejamento da contratação: Marcelo Donadon – Coordenador de 
    Administração da 4ª Região Administrativa Judiciária – DARAJ 4 – Campinas
    
    26. ESTIMATIVA DO PRAZO DE VIGÊNCIA
    O Prazo de vigência do contrato será estimado em dias corridos, a contar da data de 
    assinatura do contrato. OIS: Em até 30 dias. EXECUÇÃO: Em até 180 dias.
    
    27. AVALIAÇÃO CONCLUSIVA
    Com base nas informações levantadas ao longo do estudo técnico preliminar, resta 
    evidente que a contratação, nos termos propostos, atenderá às necessidades a que se destina.
    """
    
    try:
        agente = ETPAgent()
        if agente.ai is None:
            print("❌ ERRO: AIClient não inicializado (verifique OPENAI_API_KEY)")
            return False
        
        print("✅ ETPAgent inicializado com sucesso")
        print(f"📝 Processando {len(texto_etp_real)} caracteres...")
        
        resultado = agente.generate(texto_etp_real)
        
        if "erro" in resultado:
            print(f"❌ ERRO: {resultado['erro']}")
            return False
        
        print("✅ Processamento concluído\n")
        print("📊 DADOS ADMINISTRATIVOS EXTRAÍDOS:")
        print(f"   📍 Unidade: {resultado.get('unidade_demandante', 'N/A')}")
        print(f"   👤 Responsável: {resultado.get('responsavel', 'N/A')}")
        print(f"   ⏱️  Prazo: {resultado.get('prazo_estimado', 'N/A')}")
        print(f"   💰 Valor: R$ {resultado.get('valor_estimado', 'N/A')}")
        
        secoes = resultado.get('secoes', {})
        secoes_preenchidas = [k for k, v in secoes.items() if v and v.strip() and v != ""]
        print(f"\n📋 SEÇÕES ESTRUTURADAS: {len(secoes_preenchidas)}/27")
        
        if secoes_preenchidas:
            print("\n✅ Seções com conteúdo:")
            for i, secao in enumerate(secoes_preenchidas[:10], 1):  # Primeiras 10
                conteudo = secoes[secao][:80] + "..." if len(secoes[secao]) > 80 else secoes[secao]
                print(f"   {i}. {secao}: {conteudo}")
            
            if len(secoes_preenchidas) > 10:
                print(f"   ... e mais {len(secoes_preenchidas) - 10} seções")
        
        lacunas = resultado.get('lacunas', [])
        if lacunas:
            print(f"\n⚠️  Lacunas identificadas ({len(lacunas)}):")
            for lacuna in lacunas[:5]:
                print(f"   - {lacuna}")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa teste do ETPAgent"""
    print("\n🚀 TESTE DO AGENTE ETP ESPECIALIZADO\n")
    
    # Verificar OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY não encontrada no ambiente")
        print("   O teste pode falhar")
    else:
        print(f"✅ OPENAI_API_KEY encontrada\n")
    
    sucesso = test_etp_agent()
    
    print("\n" + "=" * 70)
    if sucesso:
        print("✅ TESTE PASSOU - ETPAgent funcionando corretamente")
    else:
        print("❌ TESTE FALHOU - Verifique os logs acima")
    print("=" * 70)
    
    return sucesso


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
