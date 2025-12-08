#!/usr/bin/env python3
# ==========================================================
# test_dfd_processing.py - Teste local do processamento DFD
# ==========================================================

import os
import sys
import json

# Garantir que imports funcionem
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_document_agent():
    """Testa o DocumentAgent diretamente"""
    print("=" * 70)
    print("TESTE 1: DocumentAgent com texto simples")
    print("=" * 70)
    
    from agents.document_agent import DocumentAgent
    
    texto_teste = """
    ESTUDO TÉCNICO PRELIMINAR
    
    1. OBJETO
    Contratação de serviços de manutenção predial para o Fórum de Rio Claro.
    
    2. DESCRIÇÃO DA NECESSIDADE
    O edifício necessita de manutenção urgente devido ao desgaste natural.
    
    13. ESTIMATIVA DE VALOR
    Valor estimado: R$ 450.000,00
    
    25. EQUIPE DE PLANEJAMENTO
    Unidade solicitante: Serviço de Administração do Fórum
    Gestor: João Silva - Coordenador DARAJ 4
    """
    
    try:
        agente = DocumentAgent("DFD")
        if agente.ai is None:
            print("❌ ERRO: AIClient não inicializado (verifique OPENAI_API_KEY)")
            return False
        
        print("✅ AIClient inicializado com sucesso")
        print(f"📝 Processando {len(texto_teste)} caracteres...")
        
        resultado = agente.generate(texto_teste)
        
        if "erro" in resultado:
            print(f"❌ ERRO: {resultado['erro']}")
            return False
        
        print("✅ Processamento concluído")
        print(f"📊 Campos extraídos:")
        print(f"   - Unidade: {resultado.get('unidade_demandante', 'N/A')}")
        print(f"   - Responsável: {resultado.get('responsavel', 'N/A')}")
        print(f"   - Valor: {resultado.get('valor_estimado', 'N/A')}")
        print(f"   - Seções: {len(resultado.get('secoes', {}))}")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_processar_dfd():
    """Testa a função wrapper processar_dfd_com_ia"""
    print("\n" + "=" * 70)
    print("TESTE 2: processar_dfd_com_ia (wrapper)")
    print("=" * 70)
    
    from agents.document_agent import processar_dfd_com_ia
    
    texto_teste = """
    ESTUDO TÉCNICO PRELIMINAR
    
    OBJETO: Contratação de obras de acessibilidade
    VALOR: R$ 400.000,00
    UNIDADE: Fórum de Rio Claro
    GESTOR: Marcelo Donadon
    """
    
    try:
        resultado = processar_dfd_com_ia(texto_teste)
        
        if "erro" in resultado:
            print(f"❌ ERRO: {resultado['erro']}")
            return False
        
        print("✅ Processamento wrapper concluído")
        print(f"📅 Timestamp: {resultado.get('timestamp', 'N/A')}")
        
        dfd = resultado.get('resultado_ia', {})
        if 'DFD' in dfd:
            dfd = dfd['DFD']
        
        print(f"📊 Resultado DFD:")
        print(f"   - Unidade: {dfd.get('unidade_demandante', 'N/A')}")
        print(f"   - Valor: {dfd.get('valor_estimado', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_client():
    """Testa o AIClient isoladamente"""
    print("\n" + "=" * 70)
    print("TESTE 3: AIClient isolado")
    print("=" * 70)
    
    try:
        from utils.ai_client import AIClient
        
        print("🔧 Inicializando AIClient...")
        client = AIClient()
        
        print("✅ AIClient inicializado")
        print(f"📡 Modelo: {client.model}")
        
        print("🧪 Testando chamada simples...")
        resultado = client.ask(
            prompt="Responda apenas com JSON: {'teste': 'sucesso'}",
            conteudo="Teste de conectividade",
            artefato="TESTE"
        )
        
        if "erro" in resultado:
            print(f"❌ ERRO na chamada: {resultado['erro']}")
            return False
        
        print(f"✅ Resposta recebida: {resultado}")
        return True
        
    except Exception as e:
        print(f"❌ EXCEÇÃO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n🚀 INICIANDO BATERIA DE TESTES DFD\n")
    
    resultados = []
    
    # Verificar OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY não encontrada no ambiente")
        print("   O teste 1 e 2 falharão, mas teste 3 pode mostrar o erro")
    else:
        print(f"✅ OPENAI_API_KEY encontrada (primeiros 10 chars: {api_key[:10]}...)")
    
    print()
    
    # Teste 1: AIClient isolado (mais básico)
    resultados.append(("AIClient isolado", test_ai_client()))
    
    # Teste 2: DocumentAgent completo
    resultados.append(("DocumentAgent", test_document_agent()))
    
    # Teste 3: Wrapper processar_dfd_com_ia
    resultados.append(("Wrapper processar_dfd_com_ia", test_processar_dfd()))
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    for nome, sucesso in resultados:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"{status} - {nome}")
    
    total_passou = sum(1 for _, s in resultados if s)
    print(f"\n📊 Total: {total_passou}/{len(resultados)} testes passaram")
    
    return all(s for _, s in resultados)


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
