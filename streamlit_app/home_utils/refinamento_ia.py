# -*- coding: utf-8 -*-
"""
Componente Reutilizável: Refinamento Iterativo com IA
Permite refinamento de seções específicas de documentos (DFD, ETP, TR, Contrato)
"""

import streamlit as st
import json


def render_refinamento_iterativo(
    secoes_disponiveis: list,
    dados_atuais: dict,
    artefato: str,
    campos_simples: list = None
):
    """
    Renderiza interface de refinamento iterativo com IA.
    
    Args:
        secoes_disponiveis: Lista de nomes das seções estruturadas
        dados_atuais: Dicionário com dados do artefato
        artefato: Nome do artefato ("DFD", "ETP", "TR", "Contrato")
        campos_simples: Lista de campos simples (fora de "secoes")
    
    Returns:
        dict: Dados atualizados (se houve aplicação de refinamento)
    """
    
    # Campos simples padrão se não fornecidos
    if campos_simples is None:
        campos_simples = [
            "unidade_demandante", "responsavel", "prazo_estimado", 
            "valor_estimado", "descricao_necessidade", "motivacao", 
            "texto_narrativo"
        ]
    
    # ======================================================================
    # Interface de Refinamento
    # ======================================================================
    with st.expander("🎨 Refinamento Iterativo (Comandos IA)", expanded=False):
        st.caption(f"💡 Use esta ferramenta para solicitar melhorias específicas em qualquer seção do {artefato}")
        
        # Dropdown para selecionar seção
        todas_secoes = [""] + campos_simples + secoes_disponiveis
        secao_selecionada = st.selectbox(
            "Selecione a seção a refinar:",
            todas_secoes,
            format_func=lambda x: "-- Selecione uma seção --" if x == "" else x,
            key=f"refinamento_{artefato}_secao"
        )
        
        # Comandos rápidos predefinidos
        col_cmd1, col_cmd2 = st.columns(2)
        with col_cmd1:
            st.markdown("**Comandos Rápidos:**")
            if st.button("➕ Adicionar mais detalhes técnicos", 
                        use_container_width=True, 
                        disabled=not secao_selecionada,
                        key=f"cmd1_{artefato}"):
                st.session_state[f'comando_ia_rapido_{artefato}'] = "Adicione mais detalhes técnicos e especificações"
            if st.button("📊 Incluir métricas e indicadores", 
                        use_container_width=True, 
                        disabled=not secao_selecionada,
                        key=f"cmd2_{artefato}"):
                st.session_state[f'comando_ia_rapido_{artefato}'] = "Inclua métricas quantitativas e indicadores mensuráveis"
        
        with col_cmd2:
            st.markdown("**&nbsp;**")
            if st.button("⚖️ Melhorar fundamentação legal", 
                        use_container_width=True, 
                        disabled=not secao_selecionada,
                        key=f"cmd3_{artefato}"):
                st.session_state[f'comando_ia_rapido_{artefato}'] = "Fortaleça a fundamentação legal com citações normativas"
            if st.button("🎯 Tornar mais objetivo e direto", 
                        use_container_width=True, 
                        disabled=not secao_selecionada,
                        key=f"cmd4_{artefato}"):
                st.session_state[f'comando_ia_rapido_{artefato}'] = "Torne o texto mais objetivo e direto, eliminando redundâncias"
        
        # Campo de comando personalizado
        comando_personalizado = st.text_area(
            "Ou digite um comando personalizado:",
            value=st.session_state.get(f'comando_ia_rapido_{artefato}', ''),
            placeholder="Ex: 'Adicione justificativa baseada em economia de recursos'",
            height=80,
            key=f"campo_comando_ia_{artefato}"
        )
        
        # Botão de execução
        if st.button("✨ Executar Refinamento IA", 
                    type="primary", 
                    disabled=not secao_selecionada,
                    key=f"executar_refinamento_{artefato}"):
            # Validação melhorada
            comando_final = comando_personalizado.strip()
            
            if not secao_selecionada:
                st.warning("⚠️ Selecione uma seção primeiro")
            elif not comando_final:
                st.warning("⚠️ Forneça um comando (use os botões rápidos ou digite)")
            else:
                # Limpar comando rápido ANTES de processar
                if f'comando_ia_rapido_{artefato}' in st.session_state:
                    del st.session_state[f'comando_ia_rapido_{artefato}']
                
                try:
                    with st.spinner(f"🧠 Refinando seção '{secao_selecionada}'..."):
                        # Obter conteúdo atual da seção
                        if secao_selecionada in secoes_disponiveis:
                            conteudo_atual = dados_atuais.get("secoes", {}).get(secao_selecionada, "")
                        else:
                            conteudo_atual = dados_atuais.get(secao_selecionada, "")
                        
                        # Chamar IA para refinamento
                        from utils.ai_client import AIClient
                        ai = AIClient()
                        
                        prompt_refinamento = f"""Você está refinando a seção '{secao_selecionada}' de um {artefato} institucional.

CONTEÚDO ATUAL:
{conteudo_atual}

COMANDO DO USUÁRIO:
{comando_final}

INSTRUÇÕES:
1. Mantenha o contexto e informações existentes
2. Aplique APENAS a melhoria solicitada
3. Retorne SOMENTE o texto refinado, sem explicações
4. Mantenha formatação profissional e institucional
5. Não invente informações, apenas reorganize/expanda as existentes

Responda com o texto refinado:"""
                        
                        resultado = ai.ask(
                            prompt=prompt_refinamento,
                            conteudo="",
                            artefato=f"refinamento_{artefato.lower()}"
                        )
                        
                        # Extrair texto refinado (lógica robusta)
                        texto_refinado = _extrair_texto_refinado(resultado, secao_selecionada)
                        
                        # Salvar no session_state para persistir o preview
                        st.session_state[f'refinamento_preview_{artefato}'] = {
                            'secao': secao_selecionada,
                            'antes': conteudo_atual,
                            'depois': texto_refinado
                        }
                        
                except Exception as e:
                    st.error(f"❌ Erro ao refinar: {e}")
        
        # Mostrar preview SE existir no session_state (fora do botão Executar)
        if f'refinamento_preview_{artefato}' in st.session_state:
            preview = st.session_state[f'refinamento_preview_{artefato}']
            
            st.success("✨ Refinamento concluído! Veja o resultado:")
            
            col_antes, col_depois = st.columns(2)
            with col_antes:
                st.markdown("**📝 Antes:**")
                st.info(preview['antes'] if preview['antes'] else "_[Vazio]_")
            
            with col_depois:
                st.markdown("**✨ Depois (preview):**")
                st.success(preview['depois'])
            
            # Botões de ação
            col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
            
            with col_btn1:
                if st.button("✅ Aplicar Refinamento", 
                           type="primary", 
                           use_container_width=True,
                           key=f"aplicar_{artefato}"):
                    # Atualizar dados
                    secao = preview['secao']
                    texto = preview['depois']
                    
                    if secao in secoes_disponiveis:
                        if "secoes" not in dados_atuais:
                            dados_atuais["secoes"] = {}
                        dados_atuais["secoes"][secao] = texto
                    else:
                        dados_atuais[secao] = texto
                    
                    # Salvar na sessão (chave específica do artefato)
                    st.session_state[f"{artefato.lower()}_dados_atualizados"] = dados_atuais
                    
                    # Limpar preview
                    del st.session_state[f'refinamento_preview_{artefato}']
                    
                    st.success("✅ Refinamento aplicado!")
                    st.rerun()
            
            with col_btn2:
                if st.button("📋 Copiar Texto Refinado", 
                           use_container_width=True,
                           key=f"copiar_{artefato}"):
                    st.code(preview['depois'], language=None)
                    st.info("💡 Use Ctrl+C para copiar o texto acima")
            
            with col_btn3:
                if st.button("❌ Cancelar", 
                           use_container_width=True,
                           key=f"cancelar_{artefato}"):
                    del st.session_state[f'refinamento_preview_{artefato}']
                    st.rerun()
    
    # Retornar dados atualizados se houver
    return st.session_state.get(f"{artefato.lower()}_dados_atualizados", dados_atuais)


def _extrair_texto_refinado(resultado, secao_selecionada):
    """
    Extrai texto refinado de diferentes formatos de resposta da IA.
    """
    texto_refinado = ""
    
    if isinstance(resultado, dict):
        # Tentar extrair de estruturas aninhadas
        for key in resultado.keys():
            if key.startswith('refinamento_'):
                refinamento_data = resultado[key]
                if isinstance(refinamento_data, dict):
                    # Pegar o valor do campo específico
                    texto_refinado = refinamento_data.get(secao_selecionada, "")
                    # Se não encontrou, pegar o primeiro valor não-vazio
                    if not texto_refinado:
                        for valor in refinamento_data.values():
                            if isinstance(valor, str) and valor.strip():
                                texto_refinado = valor
                                break
                elif isinstance(refinamento_data, str):
                    texto_refinado = refinamento_data
                break
        
        # Caso 2: campos diretos no dict
        if not texto_refinado:
            texto_refinado = (
                resultado.get("resposta") or 
                resultado.get("content") or 
                resultado.get("texto") or 
                resultado.get(secao_selecionada) or
                ""
            )
        
        # Caso 3: se ainda vazio, converter dict para string
        if not texto_refinado:
            texto_refinado = json.dumps(resultado, ensure_ascii=False, indent=2)
    else:
        texto_refinado = str(resultado)
    
    return texto_refinado.strip()
