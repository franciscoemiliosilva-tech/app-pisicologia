import streamlit as st
import google.generativeai as genai

# Configuração da API (Use sua secret do Streamlit ou string direta para testar)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# SOLUÇÃO DEFINITIVA PARA O ERRO 404:
# Use o nome simples 'gemini-1.5-flash' e certifique-se de NÃO usar v1beta no código.
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_prontuario(transcricao, notas):
    prompt = f"Gere um prontuário psicológico baseado nesta transcrição: {transcricao}. Notas extras: {notas}"
    
    try:
        # Chamada direta sem enrolação
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao chamar a API: {e}"
