import streamlit as st
import whisper
import google.generativeai as genai
import os

st.set_page_config(page_title="Assistente de Voz Clínico", layout="wide")

st.title("🎙️ Gerador de Prontuário por Áudio")

# Barra lateral para a chave
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")

# Upload focado em Áudio
audio_file = st.file_uploader("Selecione a gravação da sessão (Áudio)", type=['mp3', 'wav', 'm4a'])
notas_medicas = st.text_area("Anotações complementares:")

if st.button("✨ Gerar Prontuário"):
    if not api_key:
        st.error("Por favor, insira a sua API Key na lateral!")
    elif audio_file is not None:
        try:
            with st.status("Processando áudio...", expanded=True) as status:
                # Salva o arquivo de áudio
                with open("audio_temp.mp3", "wb") as f:
                    f.write(audio_file.getbuffer())
                
                # Transcrição ultra-rápida
                status.write("🎧 Transcrevendo falas...")
                model_w = whisper.load_model("tiny")
                result = model_w.transcribe("audio_temp.mp3")
                
                # Inteligência Gemini
                status.write("🧠 Criando prontuário técnico...")
                genai.configure(api_key=api_key)
                model_g = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""Crie um prontuário SOAP técnico para psicóloga. 
                Notas da sessão: {notas_medicas}
                Transcrição do áudio: {result['text']}"""
                
                response = model_g.generate_content(prompt)
                status.update(label="✅ Prontuário Gerado com Sucesso!", state="complete")
                
                st.divider()
                st.subheader("📝 Resultado:")
                st.write(response.text)
                st.balloons()
        except Exception as e:
            st.error(f"Ocorreu um ajuste necessário: {e}")
    else:
        st.warning("Suba um arquivo de áudio primeiro.")
