# Importando as bibliotecas necessárias
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from langchain_community.llms import Ollama, Langgraph
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

class Produtos(BaseModel):
    produtos: Dict[str, str]

class Sugestoes(BaseModel):
    sugestoes: Optional[Dict[str, str]]

# Inicializando o LLM do Ollama (Llama 2)
llama2 = Ollama(model="llama2")

# Inicializando o Langgraph
langgraph = Langgraph()

# Definindo um template de prompt para sugestões de vendas
template = ChatPromptTemplate.from_messages(["Based on your interest in {topic}, you might also like these products"])

# Criando uma cadeia de processamento de texto
chain = template | langgraph | llama2 | CommaSeparatedListOutputParser()

# Criando um gráfico de estado
state_graph = StateGraph()

# Adicionando nós ao gráfico de estado
state_graph.add_node("input", chain)

# Definindo o ponto de entrada do gráfico de estado
state_graph.set_entry_point("input")

# Criando uma instância do FastAPI
app = FastAPI(title="Agente de Vendas Inteligente para o Hackathon Bren", version="1.0", description="Sugestões de vendas casadas utilizando LangChain")

# Rota para processar as consultas dos clientes
@app.post("/sugerir_venda", response_model=Sugestoes)
def sugerir_venda(produtos: Produtos):
    # Processa os produtos recebidos e gera sugestões de vendas
    try:
        sugestoes = state_graph.invoke(produtos.produtos)
        return Sugestoes(sugestoes=sugestoes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Executando o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9001)
