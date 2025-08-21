# LangChain Azure TestGen

Gera testes unitários (pytest) com LangChain + Azure OpenAI.

## Requisitos

- Python 3.10+
- Conta Azure OpenAI com um deployment

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # preencha as variáveis
```

## Uso

Gerar testes para um arquivo:

```bash
python -m testgen.cli generate --file src/math_utils.py
```

Gerar para todos os .py em `src/`:

```bash
python -m testgen.cli generate --dir src
```

Rodar pytest:

```bash
python -m testgen.cli test
```

Auto-reparo (usa último log do pytest):

```bash
python -m testgen.cli repair --module math_utils
```

## Variáveis (.env)

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=
```

## Observações

- Testes são salvos em `tests/test_<module>.py`.
