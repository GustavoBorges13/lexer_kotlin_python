FROM python:3.9-slim

WORKDIR /app

# Copia tudo (incluindo a pasta exemplos e LexerProject)
COPY . /app

# ENTRYPOINT define o executável fixo
ENTRYPOINT ["python", "-m", "LexerProject.main"]

# CMD define os argumentos padrão (caso você não passe nada)
CMD []