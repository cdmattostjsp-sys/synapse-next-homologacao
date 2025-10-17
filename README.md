# 🧠 SynapseNext – Ecossistema SAAB 5.0  
**Secretaria de Administração e Abastecimento – Tribunal de Justiça de São Paulo (TJSP)**  

---

## 📘 Descrição Geral
O **SynapseNext** integra o **Ecossistema SAAB 5.0**, concebido como uma plataforma de apoio inteligente para a **gestão e automação das fases internas de contratações públicas** no TJSP.  
Ele foi desenvolvido a partir da evolução do **SynapseTutor**, incorporando módulos de análise semântica, recomendação textual e exportação automatizada de artefatos administrativos (DFD → ETP → TR → Contrato).  

O projeto busca fortalecer a autonomia tecnológica do Tribunal, reduzindo dependência de fornecedores externos e consolidando uma arquitetura de agentes internos baseada em **IA explicável, auditável e institucional**.

---

## ⚙️ Estrutura do Repositório
synapse-next/
│
├── agents/ # Agentes internos (guia e detecção de estágios)
├── journey/ # Configurações e fluxos das jornadas (DFD, ETP, TR)
├── knowledge/ # Base de conhecimento institucional (leis e manuais)
├── knowledge_base/ # Modelos e checklists de conformidade
├── prompts/ # Conjuntos de prompts orientados por classe
├── streamlit_app/ # Aplicações interativas e interface do Tutor
├── utils/ # Módulos de suporte (formatação, recomendação, etc.)
└── tests/ # Scripts de validação e testes automatizados
