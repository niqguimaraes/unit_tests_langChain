from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def make_llm(temperature: float = 0.2, max_tokens: int = 2000) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
        temperature=temperature,
        max_tokens=max_tokens,
    )
