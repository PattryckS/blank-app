import streamlit as st
import os

st.title("Envie suas fotos aqui! 📸")

# Botão para upload de múltiplos arquivos
fotos = st.file_uploader("Selecione todas as fotos", accept_multiple_files=True, type=["jpg", "png", "jpeg"])

if st.button("Enviar Fotos"):
    if fotos:
        for foto in fotos:
            # Salva o arquivo original na pasta do servidor
            with open(os.path.join("pasta_recebidos", foto.name), "wb") as f:
                f.write(foto.getbuffer())
        st.success("Todas as fotos foram enviadas com sucesso e qualidade original!")
    else:
        st.error("Por favor, selecione pelo menos uma foto.")
