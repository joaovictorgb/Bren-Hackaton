# Importando as bibliotecas necessárias
from typing import List, Dict
from fastapi import FastAPI
from langchain_community.llms import Ollama  # Corrigido
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Inicializando o LLM do Ollama (Llama 2)
llama2 = Ollama(model="llama2")

# Definindo um template de prompt para sugestões de vendas
template = ChatPromptTemplate.from_messages(["Based on your interest in {topic}, you might also like these products"])

# Criando uma cadeia de processamento de texto
chain = template | llama2 | CommaSeparatedListOutputParser()

# Criando uma instância do FastAPI
app = FastAPI(title="Agente de Vendas Inteligente para o Hackathon Bren", version="1.0", description="Sugestões de vendas casadas utilizando LangChain")
# Rota para processar as consultas dos clientes
@app.post("/sugerir_venda")
def sugerir_venda(produtos: Dict[str, str]):
    # Processa os produtos recebidos e gera sugestões de vendas
    sugestoes = chain.invoke(produtos)
    return {"sugestoes": sugestoes}

# Executando o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9001)
