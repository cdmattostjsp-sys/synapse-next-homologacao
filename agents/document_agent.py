"""
document_agent.py – SynapseNext vNext
Agente responsável pela leitura, interpretação e estruturação semântica de insumos documentais.
Compatível com OpenAI API e arquitetura de validação SynapseNext – SAAB 5.0.
"""

import os
import re
import json
from datetime import datetime
from openai import OpenAI

# Inicializa o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

class DocumentAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def _extract_metadata(self, text: str) -> dict:
        """
        Extrai metadados básicos do texto do documento.
        Detecta tipo, data, órgão e possíveis seções padronizadas.
        """
        metadata = {
            "tipo": None,
            "data": None,
            "orgao": None,
            "detectado_por": "regex+LLM",
        }

        patterns = {
            "tipo": r"\b(DFD|ETP|TERMO DE REFER[ÊE]NCIA|EDITAL|CONTRATO)\b",
            "data": r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b",
            "orgao": r"(Tribunal de Justiça|Secretaria de Administração|SAAB|TJSP)",
        }

        for k, p in patterns.items():
            m = re.search(p, text, re.IGNORECASE)
            metadata[k] = m.group(1) if m else None

        return metadata

    def _classify_document(self, text: str) -> str:
        """
        Classifica o tipo de documento via IA.
        """
        prompt = f"""
        Classifique o tipo do documento abaixo como um dos seguintes:
        [DFD, ETP, TR, EDITAL, CONTRATO].
        Documento:
        {text[:1500]}
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em gestão pública e licitações."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            classification = response.choices[0].message.content.strip().upper()
            if classification not in ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]:
                classification = "INDETERMINADO"
            return classification
        except Exception as e:
            print(f"⚠️ Erro na classificação IA: {e}")
            return "INDETERMINADO"

    def process_document(self, file_path: str) -> dict:
        """
        Lê o arquivo, extrai texto, metadados e classifica.
        Retorna uma estrutura JSON pronta para os validadores.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                text = f.read()

        metadata = self._extract_metadata(text)
        tipo = metadata["tipo"] or self._classify_document(text)

        data = {
            "arquivo": os.path.basename(file_path),
            "tipo": tipo,
            "metadados": metadata,
            "conteudo": text[:5000],
            "gerado_em": datetime.now().isoformat(),
        }

        return data

    def save_json(self, data: dict, output_dir="exports") -> str:
        """
        Salva o artefato JSON do documento processado.
        """
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{data['tipo'].lower()}_data.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Artefato salvo em {out_path}")
        return out_path


if __name__ == "__main__":
    print("🧠 Teste rápido do DocumentAgent – SynapseNext vNext")
    agent = DocumentAgent()
    insumo = "insumos_processados/DFD_Ficticio_SynapseNext.txt"

    if os.path.exists(insumo):
        resultado = agent.process_document(insumo)
        agent.save_json(resultado)
    else:
        print("⚠️ Nenhum arquivo de teste encontrado em /insumos_processados")
