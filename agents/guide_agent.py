"""
guide_agent.py – SynapseNext vNext
Agente de orientação inteligente e tutor de homologação.
Fornece respostas institucionais, orientações de próxima etapa e diagnósticos.
Homologado: SAAB/TJSP – vNext 2025
"""

import os
import json
from datetime import datetime
from openai import OpenAI

# Inicializa cliente OpenAI (usa chave de ambiente ou secrets.toml)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

class GuideAgent:
    """
    Atua como assistente institucional do SynapseNext.
    Orienta a sequência da jornada de contratação com base em artefatos, metadados e padrões SAAB/TJSP.
    """

    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.contexto_base = (
            "Você é o assistente institucional SynapseNext, "
            "especializado em contratações públicas e na Lei 14.133/2021. "
            "Seu papel é orientar de forma técnica e objetiva o andamento "
            "dos artefatos (DFD → ETP → TR → Edital → Contrato), "
            "sempre conforme as diretrizes da SAAB/TJSP."
        )

    def gerar_orientacao(self, artefatos_dir="exports") -> str:
        """
        Analisa os artefatos existentes e gera um resumo da situação institucional.
        Exemplo: identifica se há documentos faltantes, inconsistentes ou desatualizados.
        """
        arquivos = [f for f in os.listdir(artefatos_dir) if f.endswith("_data.json")]
        if not arquivos:
            return "⚠️ Nenhum artefato encontrado para análise."

        situacao = []
        for nome in sorted(arquivos):
            path = os.path.join(artefatos_dir, nome)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                tipo = data.get("tipo", "INDEFINIDO")
                data_gerado = data.get("gerado_em", "sem data")
                situacao.append(f"📄 {tipo} – gerado em {data_gerado}")
            except Exception as e:
                situacao.append(f"⚠️ Erro ao ler {nome}: {e}")

        resumo = "\n".join(situacao)
        prompt = f"""
        {self.contexto_base}

        Abaixo está o estado atual dos artefatos no diretório 'exports':
        {resumo}

        Gere uma orientação institucional breve:
        - Quais etapas estão concluídas?
        - Qual a próxima ação recomendada?
        - Há alertas ou pendências?
        """

        try:
            resposta = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é o agente de orientação institucional do TJSP."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            conteudo = resposta.choices[0].message.content.strip()
            return conteudo

        except Exception as e:
            return f"⚠️ Erro ao gerar orientação: {e}"

    def responder_pergunta(self, pergunta: str) -> str:
        """
        Responde perguntas institucionais gerais sobre a jornada de contratação.
        Usa contexto SAAB/TJSP e diretrizes normativas.
        """
        prompt = f"""
        {self.contexto_base}

        Pergunta: {pergunta}
        Responda de forma técnica e concisa.
        """

        try:
            resposta = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é o orientador técnico da SAAB/TJSP."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            conteudo = resposta.choices[0].message.content.strip()
            return conteudo

        except Exception as e:
            return f"⚠️ Erro ao responder pergunta: {e}"

    def registrar_orientacao(self, conteudo: str, output_dir="exports/logs") -> str:
        """
        Salva o texto de orientação gerado pela IA em um arquivo de log institucional.
        """
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"guide_agent_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write("============================================================\n")
            f.write("🧭 SynapseNext – Guia de Orientação Institucional\n")
            f.write(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("============================================================\n\n")
            f.write(conteudo)

        return path


if __name__ == "__main__":
    print("🧭 Teste rápido do GuideAgent – SynapseNext vNext")
    agent = GuideAgent()

    orientacao = agent.gerar_orientacao()
    print("\n" + orientacao + "\n")

    arquivo_log = agent.registrar_orientacao(orientacao)
    print(f"📄 Log salvo em: {arquivo_log}")
