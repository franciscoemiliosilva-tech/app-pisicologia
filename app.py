import streamlit as st
import whisper
import google.generativeai as genai
import os

st.set_page_config(page_title="Assistente de Voz Clínico")
st.title("🎙️ Gerador de Prontuário por Áudio")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")

audio_file = st.file_uploader("Selecione o áudio (MP3, WAV, M4A)", type=['mp3', 'wav', 'm4a'])
notas_medicas = st.text_area("Anotações da sessão:")

if st.button("✨ Gerar Prontuário"):
    if not api_key:
        st.error("Por favor, insira a sua API Key na lateral!")
    elif audio_file is not None:
        try:
            with st.status("Processando...", expanded=True) as status:
                with open("audio_temp.mp3", "wb") as f:
                    f.write(audio_file.getbuffer())
                
                status.write("🎧 Transcrevendo áudio...")
                # Whisper leve para não travar
                model_w = whisper.load_model("tiny")
                result = model_w.transcribe("audio_temp.mp3")
                
                status.write("🧠 Criando prontuário técnico...")
                # FORÇA A VERSÃO ESTÁVEL v1 PARA MATAR O ERRO 404
                genai.configure(api_key=api_key, transport='rest') 
                model_g = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Gere um prontuário SOAP profissional. Notas: {notas_medicas}. Transcrição: {result['text']}"
                response = model_g.generate_content(prompt)
                
                status.update(label="✅ Concluído!", state="complete")
                st.divider()
                st.subheader("📝 Resultado:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Erro detectado: {e}")
    else:
        st.warning("Suba um arquivo de áudio primeiro.")
