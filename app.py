import streamlit as st
import whisper
import google.generativeai as genai

st.set_page_config(page_title="Assistente Clínico")
st.title("🏥 Gerador de Prontuários")

api_key = st.sidebar.text_input("Gemini API Key:", type="password")
video = st.file_uploader("Suba o vídeo", type=['mp4', 'mov', 'mkv'])
notas = st.text_area("Notas da sessão:")

if st.button("Gerar"):
    if api_key and video:
        with st.spinner("Processando..."):
            with open("temp.mp4", "wb") as f:
                f.write(video.getbuffer())
            
            # Transcrição leve
            modelo_audio = whisper.load_model("tiny")
            transcricao = modelo_audio.transcribe("temp.mp4")["text"]
            
            # IA Gemini - VERSÃO DEFINITIVA PARA EVITAR 404
            genai.configure(api_key=api_key)
            # Aqui está o segredo: usamos o nome simples do modelo
            modelo_texto = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Gere um prontuário SOAP técnico. Notas: {notas}. Transcrição: {transcricao}"
            resultado = modelo_texto.generate_content(prompt)
            
            st.success("Concluído!")
            st.write(resultado.text)
    else:
        st.error("Falta a chave ou o vídeo!")
