# utils/next_pipeline.py (trecho adicional)
def run_semantic_validation(artefato: str, markdown_text: str, client=None) -> dict:
    """
    Executa a validação semântica com o motor validator_engine_vNext.
    Retorna dict com rigid_score, semantic_score, guided_markdown, etc.
    """
    from openai import OpenAI
    import os
    from validator_engine_vNext import validate_document

    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Chave OPENAI_API_KEY não configurada nas secrets.")
        client = OpenAI(api_key=api_key)

    result = validate_document(markdown_text, artefato, client)

    # logs
    save_log(artefato, {
        "acao": "validar_semantico",
        "scores": {
            "rigid_score": result.get("rigid_score"),
            "semantic_score": result.get("semantic_score")
        }
    })
    return result
