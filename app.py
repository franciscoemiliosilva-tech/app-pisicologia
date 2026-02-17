import streamlit as st
import whisper
import google.generativeai as genai
import os

st.set_page_config(page_title="Assistente Clínico", layout="wide")
st.title("🏥 Gerador de Prontuários")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Gemini API Key:", type="password")

video_file = st.file_uploader("Selecione o vídeo da sessão", type=['mp4', 'mov', 'mkv'])
notas_medicas = st.text_area("Notas rápidas da sessão:")

if st.button("🚀 Gerar Prontuário Agora"):
    if not api_key:
        st.error("Por favor, insira a sua API Key na lateral!")
    elif video_file is not None:
        try:
            # 1. Fase de Preparação
            progresso = st.status("Iniciando processamento...")
            
            with open("video_temp.mp4", "wb") as f:
                f.write(video_file.getbuffer())
            
            # 2. Fase de Audição (Whisper)
            progresso.update(label="🎧 A IA está ouvindo o vídeo... (Passo 1/2)", state="running")
            model_w = whisper.load_model("tiny")
            result = model_w.transcribe("video_temp.mp4")
            
            # 3. Fase de Escrita (Gemini)
            progresso.update(label="✍️ A IA está escrevendo o prontuário... (Passo 2/2)", state="running")
            genai.configure(api_key=api_key)
            model_g = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Gere um prontuário SOAP profissional. Notas: {notas_medicas}. Transcrição: {result['text']}"
            response = model_g.generate_content(prompt)
            
            progresso.update(label="✅ Concluído!", state="complete")

            # 4. Exibição em destaque
            st.divider()
            st.subheader("📝 Prontuário Finalizado:")
            # Usamos um campo de texto que permite copiar facilmente
            st.text_area("Resultado (Copia daqui):", value=response.text, height=400)
            st.balloons() # Balões para comemorar a vitória!
            
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Selecione um vídeo primeiro.")
