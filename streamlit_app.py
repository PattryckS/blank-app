import streamlit as st
import os
import zipfile
import io

# Nome da pasta temporária no servidor da nuvem
PASTA_DESTINO = "pasta_recebidos"

if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

st.title("Envie suas fotos aqui! 📸")
st.write("Selecione e envie suas fotos com a qualidade original intacta.")

# Botão para upload de múltiplos arquivos
fotos = st.file_uploader("Selecione todas as fotos de uma vez:", accept_multiple_files=True, type=["jpg", "png", "jpeg"])

if st.button("Enviar Fotos", type="primary"):
    if fotos:
        for foto in fotos:
            caminho_arquivo = os.path.join(PASTA_DESTINO, foto.name)
            with open(caminho_arquivo, "wb") as f:
                f.write(foto.getbuffer())
                
        st.success(f"Sucesso! {len(fotos)} fotos foram enviadas.")
    else:
        st.error("Por favor, selecione pelo menos uma foto antes de enviar.")

# --- ÁREA DO ORGANIZADOR PARA BAIXAR AS FOTOS ---
st.markdown("---")
with st.expander("🔒 Área do Organizador (Para você baixar as fotos)"):
    # RECOMENDAÇÃO: Altere a senha abaixo para uma de sua preferência
    SENHA_CORRETA = "4775"
    
    senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
    
    if senha_digitada == SENHA_CORRETA:
        arquivos = os.listdir(PASTA_DESTINO)
        
        if arquivos:
            st.write(f"Total de fotos recebidas até agora: **{len(arquivos)}**")
            
            # Cria o arquivo ZIP diretamente na memória do servidor
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zip_file:
                for arquivo in arquivos:
                    caminho_completo = os.path.join(PASTA_DESTINO, arquivo)
                    zip_file.write(caminho_completo, arquivo)
            
            buffer.seek(0)
            
            # Botão para você fazer o download do pacote de fotos
            st.download_button(
                label="📥 Baixar Todas as Fotos (.ZIP)",
                data=buffer,
                file_name="fotos_originais.zip",
                mime="application/zip"
            )
        else:
            st.info("Nenhuma foto foi enviada ainda.")
    elif senha_digitada != "":
        st.error("Senha incorreta!")
