import streamlit as st
import whisper
import google.generativeai as genai

st.set_page_config(page_title="Assistente Clínico")
st.title("🏥 Gerador de Prontuários")

# Configuração simples na barra lateral
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

video = st.file_uploader("Suba o vídeo aqui", type=['mp4', 'mov', 'mkv'])
notas = st.text_area("Notas rápidas da sessão:")

if st.button("Gerar Prontuário"):
    if api_key and video:
        try:
            with st.spinner("Processando... aguarde um momento."):
                # Salva o vídeo temporariamente
                with open("temp.mp4", "wb") as f:
                    f.write(video.getbuffer())
                
                # Transcrição (Whisper)
                modelo_audio = whisper.load_model("tiny")
                transcricao = modelo_audio.transcribe("temp.mp4")["text"]
                
                # Inteligência (Gemini) - Versão estável
                genai.configure(api_key=api_key)
                modelo_texto = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Gere um prontuário SOAP técnico. Notas: {notas}. Transcrição: {transcricao}"
                resultado = modelo_texto.generate_content(prompt)
                
                st.success("Concluído!")
                st.write(resultado.text)
        except Exception as e:
            st.error(f"Erro detectado: {e}")
    else:
        st.error("Por favor, coloque a API Key e o vídeo.")
