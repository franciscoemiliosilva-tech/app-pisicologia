import streamlit as st
import whisper
import google.generativeai as genai

st.set_page_config(page_title="Assistente Clínico")

st.title("🏥 Gerador de Prontuários")

# Configuração simples
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

video = st.file_uploader("Suba o vídeo aqui", type=['mp4', 'mov', 'mkv'])
notas = st.text_area("Notas da sessão:")

if st.button("Gerar"):
    if api_key and video:
        with st.spinner("Processando... aguarde um momento."):
            # Salva o vídeo para a IA ler
            with open("temp.mp4", "wb") as f:
                f.write(video.getbuffer())
            
            # Parte 1: Transcrição (Whisper)
            modelo_audio = whisper.load_model("tiny")
            transcricao = modelo_audio.transcribe("temp.mp4")["text"]
            
            # Parte 2: Inteligência (Gemini)
            genai.configure(api_key=api_key)
            modelo_texto = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Crie um prontuário SOAP técnico. Notas: {notas}. Transcrição: {transcricao}"
            resultado = modelo_texto.generate_content(prompt)
            
            # Exibe o resultado final
            st.success("Prontuário Gerado!")
            st.write(resultado.text)
    else:
        st.error("Por favor, coloque a API Key e o vídeo.")
