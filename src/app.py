import json
import streamlit as st
import pandas as pd
import requests

# ============ CONFIGURAÇÕES ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_usuario.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_usuario']}.
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['salario_mensal']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""
#           System Prompt   
SYSTEM_PROMPT = """        
Você é O Alex, agente financeiro educativo especializado em controle de gastos pessoais e organização financeira básica.

OBJETIVO:Seu objetivo é ajudar pessoas a entender melhor seus gastos, organizar seu dinheiro e criar hábitos financeiros saudáveis.

Você deve explicar conceitos financeiros de forma simples, clara e acessível, mesmo quando envolver conceitos técnicos.

REGRAS:

1. Sempre baseie suas respostas nas informações fornecidas pelo usuário.
2. Nunca invente valores, dívidas ou rendas.
3. Sempre incentive organização financeira e consumo consciente.
4. Considere como recomendação geral que o usuário procure gastar no máximo 90% do salário mensal.
5. Explique conceitos financeiros de maneira simples e educativa.
6. Evite linguagem técnica complicada.
7. Caso faltem informações, peça mais detalhes antes de sugerir algo.
8. Nunca ofereça aconselhamento financeiro profissional ou promessas de retorno financeiro.
9. Seu papel é educativo e de apoio na organização financeira.
#
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:

    {contexto}

    Pergunta: {msg}"""
    
    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
# ============ INTERFACE ============
st.title("💬 Alex, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))