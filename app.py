import streamlit as st
import whisper
import google.generativeai as genai
import os

# Configuração da Página
st.set_page_config(page_title="Assistente Clínico", layout="wide")

st.title("🏥 Gerador de Prontuários")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")

video_file = st.file_uploader("Selecione o vídeo da sessão", type=['mp4', 'mov', 'mkv'])
notas_medicas = st.text_area("Notas rápidas da sessão:")

if st.button("Gerar Prontuário"):
    if not api_key:
        st.error("Por favor, insira a sua API Key na lateral!")
    elif video_file is not None:
        try:
            with st.spinner("IA processando o vídeo... aguarde."):
                # Salva vídeo temporário
                with open("video_temp.mp4", "wb") as f:
                    f.write(video_file.getbuffer())
                
                # Transcrição com Whisper
                model_w = whisper.load_model("tiny")
                result = model_w.transcribe("video_temp.mp4")
                
                # Configuração do Gemini
                genai.configure(api_key=api_key)
                model_g = genai.GenerativeModel('gemini-1.5-flash')
                
                # Gerar o texto
                prompt = f"Crie um prontuário SOAP técnico baseado nestas notas: {notas_medicas} e nesta transcrição: {result['text']}"
                response = model_g.generate_content(prompt)
                
                st.subheader("📝 Prontuário Sugerido:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Suba um vídeo primeiro.")
