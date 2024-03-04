# Importando as bibliotecas necessárias
from fastapi import FastAPI
from typing import Dict
from langchain_community.llms import Ollama, Langgraph
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

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
@app.post("/sugerir_venda")
def sugerir_venda(produtos: Dict[str, str] = {
    "Camiseta Polo": "Azul",
    "Calça Jeans": "Preta",
    "Blusa de Frio": "Vermelha",
    "Vestido Floral": "Multicolorido",
    "Shorts de Algodão": "Branco",
    "Regata": "Verde",
    "Saia Longa": "Preto",
    "Blazer": "Cinza",
    "Camisa Social": "Branca",
    "Jaqueta de Couro": "Preto"
}):
    # Processa os produtos recebidos e gera sugestões de vendas
    sugestoes = state_graph.invoke(produtos)
    return {"sugestoes": sugestoes}

# Executando o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9001)
