from utils.formatter_docx import markdown_to_docx

# Gera um documento de teste
markdown_to_docx("# Teste Contrato\n\n- Cláusula 1: Vigência\n- Cláusula 2: Garantias", "exports/relatorios/test_markdown.docx")

print("✅ Teste concluído: verifique o arquivo 'exports/relatorios/test_markdown.docx'")
