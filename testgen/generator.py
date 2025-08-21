from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Optional
import re, pathlib, textwrap

TEST_PROMPT = PromptTemplate.from_template(textwrap.dedent("""
Você gera **somente** o código de testes pytest. Sem explicações.
- Estilo AAA. Cobrir fluxos felizes, bordas e erros.
- Usar mocks quando necessário. Testes determinísticos.
- Nome do módulo sob teste: {module_name}.py
- Conteúdo do módulo:
"""{source_code}"""
Retorne o arquivo final tests/test_{module_name}.py
"""))

def extract_code_block(text: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()

def sanitize_filename(name: str) -> str:
    return re.sub(r"[^0-9a-zA-Z_]+", "_", pathlib.Path(name).stem)

def generate_tests_for_source(source_code: str, module_name: str, llm: Optional[AzureChatOpenAI]) -> str:
    chain = TEST_PROMPT | llm | StrOutputParser()
    out = chain.invoke({"module_name": sanitize_filename(module_name), "source_code": source_code})
    return extract_code_block(out)
