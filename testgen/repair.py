from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import textwrap, re

REPAIR_PROMPT = PromptTemplate.from_template(textwrap.dedent("""
Você gerou testes para {module_name}.py e eles falharam. Corrija.
- Responda somente com o arquivo final tests/test_{module_name}.py
- Baseie-se no log do pytest.
Código atual:
"""{current_test}"""
Log do pytest:
"""{pytest_log}"""
"""))

def extract_code_block(text: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()

def repair_test(module_name: str, current_test: str, pytest_log: str, llm: AzureChatOpenAI) -> str:
    chain = REPAIR_PROMPT | llm | StrOutputParser()
    out = chain.invoke({"module_name": module_name, "current_test": current_test, "pytest_log": pytest_log[:20000]})
    return extract_code_block(out)
