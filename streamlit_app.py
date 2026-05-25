import streamlit as st
import os
import zipfile
import datetime

# Pasta onde os arquivos ZIP de cada envio serão guardados
PASTA_DESTINO = "lotes_recebidos"

if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

st.title("Envie suas fotos aqui! 📸")
st.write("Selecione suas fotos e clique em enviar. Cada envio gera um pacote fechado com qualidade original.")

# Botão para upload de múltiplos arquivos
fotos = st.file_uploader("Selecione as fotos deste envio:", accept_multiple_files=True, type=["jpg", "png", "jpeg"])

if st.button("Enviar Fotos", type="primary"):
    if fotos:
        # Gera um nome único para o ZIP baseado na data e hora exata do envio
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_zip = f"envio_{timestamp}.zip"
        caminho_zip = os.path.join(PASTA_DESTINO, nome_zip)
        
        # Cria o arquivo ZIP e coloca as fotos deste lote dentro dele
        with zipfile.ZipFile(caminho_zip, "w") as zip_lote:
            for foto in fotos:
                # Lê os bytes da imagem e salva dentro do ZIP
                zip_lote.writestr(foto.name, foto.getvalue())
                
        st.success(f"Sucesso! Esse lote de {len(fotos)} fotos foi enviado e salvo como `{nome_zip}`.")
    else:
        st.error("Por favor, selecione pelo menos uma foto antes de enviar.")

# --- ÁREA DO ORGANIZADOR COM SELEÇÃO DE LOTES ---
st.markdown("---")
with st.expander("🔒 Área do Organizador (Baixar Lotes Separados)"):
    SENHA_CORRETA = "minha_senha_123"
    
    senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
    
    if senha_digitada == SENHA_CORRETA:
        # Lista apenas os arquivos ZIP dentro da pasta
        arquivos_zip = [f for f in os.listdir(PASTA_DESTINO) if f.endswith('.zip')]
        
        if arquivos_zip:
            st.write(f"Total de lotes recebidos: **{len(arquivos_zip)}**")
            
            # Cria uma caixinha de seleção para você escolher qual lote quer baixar
            lote_selecionado = st.selectbox("Escolha o lote que deseja baixar:", sorted(arquivos_zip, reverse=True))
            
            caminho_lote = os.path.join(PASTA_DESTINO, lote_selecionado)
            
            # Lê o arquivo ZIP selecionado para disponibilizar para download
            with open(caminho_lote, "rb") as f:
                bytes_zip = f.read()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label=f"📥 Baixar {lote_selecionado}",
                    data=bytes_zip,
                    file_name=lote_selecionado,
                    mime="application/zip",
                    use_container_width=True
                )
                
            with col2:
                if st.button("🗑️ Apagar Todos os Lotes (Zerar)", type="secondary", use_container_width=True):
                    for arq in arquivos_zip:
                        os.remove(os.path.join(PASTA_DESTINO, arq))
                    st.success("Todos os lotes foram apagados do servidor!")
                    st.rerun()
        else:
            st.info("Nenhum lote de fotos foi enviado ainda.")
    elif senha_digitada != "":
        st.error("Senha incorreta!")
