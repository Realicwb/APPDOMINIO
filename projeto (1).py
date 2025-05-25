import pandas as pd
import os
import streamlit as st
from streamlit.components.v1 import html
import glob
import time
import io
import requests
from pathlib import Path
import random
import base64
import zipfile
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="REALI AUTOMAÇÃO",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# URL da logo
LOGO_URL = "https://raw.githubusercontent.com/Realicwb/APPDOMINIO/main/logo%20(1).png"

# CSS personalizado com tema claro e logo centralizada e animação de carregamento
custom_css = f"""
<style>
[data-testid="stSidebar"] {{
    display: none !important;
}}

[data-testid="collapsedControl"] {{
    display: none !important;
}}

/* Efeito de partículas suaves */
.particles {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
}}

.particle {{
    position: absolute;
    background: rgba(100, 181, 246, 0.3);
    border-radius: 50%;
    pointer-events: none;
}}

/* Animação de fundo gradiente claro */
@keyframes gradientBG {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Efeito de flutuação suave */
@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
    100% {{ transform: translateY(0px); }}
}}

/* Efeito de pulso suave */
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(66, 165, 245, 0.4); }}
    70% {{ box-shadow: 0 0 0 10px rgba(66, 165, 245, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(66, 165, 245, 0); }}
}}

/* Animação do spinner de carregamento */
@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

body {{
    background: linear-gradient(135deg, #e3f2fd, #bbdefb, #90caf9, #64b5f6);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    color: #333;
}}

/* Container principal */
.stApp {{
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(8px);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(30, 136, 229, 0.1);
    padding: 2rem;
    max-width: 1000px;
    margin: 2rem auto;
    border: 1px solid rgba(255, 255, 255, 0.3);
    animation: float 6s ease-in-out infinite;
}}

/* Logo centralizada */
.logo-header {{
    display: flex;
    justify-content: center;
    margin-bottom: 1.5rem;
}}

.logo-img {{
    height: 80px;
    transition: all 0.3s ease;
}}

.logo-img:hover {{
    transform: scale(1.05);
}}

.subtitle {{
    color: #42a5f5;
    font-weight: 500;
    font-size: 1.1rem;
    text-align: center;
    margin-bottom: 2rem;
}}

/* Botões principais */
.stButton>button {{
    background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
    color: white;
    border: none;
    padding: 12px 28px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 8px 0;
    cursor: pointer;
    border-radius: 30px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.2);
    font-weight: 600;
    width: 100%;
    max-width: 350px;
}}

.stButton>button:hover {{
    background: linear-gradient(135deg, #3d9ae8 0%, #1976d2 100%);
    transform: translateY(-3px);
    box-shadow: 0 8px 16px rgba(30, 136, 229, 0.3);
    animation: pulse 1.5s infinite;
}}

/* Cards */
.card {{
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.1);
    border: 1px solid rgba(66, 165, 245, 0.1);
    transition: all 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(30, 136, 229, 0.15);
}}

/* Mensagens de sucesso */
.success-message {{
    background: rgba(200, 230, 201, 0.8);
    color: #2e7d32;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin-top: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-left: 5px solid #4caf50;
    animation: slideIn 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}}

@keyframes slideIn {{
    0% {{
        opacity: 0;
        transform: translateY(-20px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Spinner de carregamento */
.loader-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 20px;
}}

.loader {{
    border: 4px solid #f3f3f3; /* Light grey */
    border-top: 4px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}}

.loader-text {{
    margin-top: 10px;
    color: #555;
    font-size: 1.1em;
}}


/* Botão de download */
.btn-download {{
    background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%) !important;
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2) !important;
}}

.btn-download:hover {{
    background: linear-gradient(135deg, #43a047 0%, #1b5e20 100%) !important;
    box-shadow: 0 8px 16px rgba(46, 125, 50, 0.3) !important;
}}

/* Seção de contas sem depara */
.contas-sem-depara-info {{
    background: rgba(255, 243, 224, 0.8);
    border-left: 4px solid #ff9800;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin: 1.5rem 0;
    font-size: 0.95rem;
}}

/* Rodapé */
footer {{
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    color: #666;
    font-size: 0.9rem;
}}

/* Responsividade */
@media (max-width: 768px) {{
    .stApp {{
        padding: 1.5rem;
        margin: 1rem;
        border-radius: 12px;
    }}
    
    .logo-img {{
        height: 60px;
    }}
}}
</style>
"""

# JavaScript para partículas animadas
particles_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);
    
    const particleCount = 20;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 5 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        particle.style.opacity = Math.random() * 0.4 + 0.1;
        
        const duration = Math.random() * 15 + 10;
        const delay = Math.random() * 5;
        particle.style.animation = `float ${duration}s ease-in-out ${delay}s infinite`;
        
        particlesContainer.appendChild(particle);
    }
});
</script>
"""

# Função para formatar a data no padrão DD/MM/AAAA
def formatar_data(data):
    try:
        if pd.isna(data):
            return None
        # Converter para datetime se ainda não for
        if not isinstance(data, (datetime, pd.Timestamp)):
            data = pd.to_datetime(data, errors='coerce')
        # Formatar como string no padrão desejado
        return data.strftime('%d/%m/%Y')
    except:
        return None

# Função para criar um arquivo Excel em memória
def criar_excel_em_memoria(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contas sem depara')
    output.seek(0)
    return output

# Função para criar um arquivo ZIP em memória com todos os arquivos
def criar_zip_em_memoria(arquivos):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, arquivo in enumerate(arquivos):
            zip_file.writestr(f"planilha_consolidada_parte_{i+1}.xlsx", arquivo.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

# Função para baixar o arquivo de regras do GitHub
def baixar_regras_github():
    url = "https://raw.githubusercontent.com/Realicwb/APPDOMINIO/main/Regras00.xlsx"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except Exception as e:
        st.error(f"Erro ao baixar arquivo de regras: {str(e)}")
        return None

# Função para processar as planilhas
def processar_planilhas(arquivos_importados, spinner_placeholder, button_placeholder):
    try:
        # Exibir spinner e texto de carregamento
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Processando...</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("Baixando arquivo de regras...") # Exibe um texto adicional

        # Baixar arquivo de regras do GitHub
        regras_file = baixar_regras_github()
        if regras_file is None:
            spinner_placeholder.empty()
            return None, None, None
        
        try:
            df_import1 = pd.read_excel(regras_file)
        except Exception as e:
            spinner_placeholder.empty()
            st.error(f"Erro ao ler arquivo de regras: {str(e)}")
            return None, None, None
        
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Processando arquivos importados...</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
        
        # Processar arquivos importados
        dfs_import = []
        total_files = len(arquivos_importados)
        
        for i, uploaded_file in enumerate(arquivos_importados):
            try:
                with spinner_placeholder:
                    st.markdown(f"""
                    <div class="loader-container">
                        <div class="loader"></div>
                        <div class="loader-text">Processando arquivo {i+1} de {total_files}...</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                required_cols = ['Data', 'Conta controle', 'Débito', 'Crédito']
                if not all(col in df.columns for col in required_cols):
                    st.warning(f"Arquivo {uploaded_file.name} não contém todas as colunas necessárias")
                    continue
                
                # Processar a coluna 'Conta controle'
                df['Conta controle'] = df['Conta controle'].astype(str).str.replace('.', '', regex=False)
                df = df.dropna(subset=['Conta controle'])
                
                # Processar a coluna 'Data' para o formato DD/MM/AAAA
                df['Data'] = df['Data'].apply(formatar_data)
                df = df.dropna(subset=['Data'])
                
                dfs_import.append(df[required_cols])
            except Exception as e:
                st.warning(f"Erro ao ler arquivo {uploaded_file.name}: {str(e)}")
                continue
        
        if not dfs_import:
            spinner_placeholder.empty()
            st.error("Nenhum arquivo válido encontrado")
            return None, None, None
        
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Concatenando dados...</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
        
        df_import = pd.concat(dfs_import, ignore_index=True)
        
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Mesclando dados...</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
        
        # Processar a coluna 'Conta controle' no dataframe de regras
        df_import1['Conta controle'] = df_import1['Conta controle'].astype(str).str.replace('.', '', regex=False)
        df_import1 = df_import1.dropna(subset=['Conta controle'])
        
        # Fazer o merge das planilhas
        df_final = pd.merge(
            df_import,
            df_import1[['Conta controle', 'conta contabil']],
            on='Conta controle',
            how='left'
        )
        
        # Criar dataframe com contas sem depara
        contas_sem_depara = df_final[df_final['conta contabil'].isna()].copy()
        contas_sem_depara = contas_sem_depara[['Conta controle', 'Data', 'Débito', 'Crédito']]
        contas_sem_depara = contas_sem_depara.drop_duplicates(subset=['Conta controle'])
        
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Processando colunas...</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
        
        # Selecionar e renomear colunas
        df_final = df_final[['Data', 'conta contabil', 'Débito', 'Crédito']]
        df_final.columns = ['Data', 'conta contabil', 'Débito', 'Crédito']
        
        # Remover linhas com conta contabil vazia
        df_final = df_final.dropna(subset=['conta contabil'])
        
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Preparando arquivos para download...</div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
        
        # Salvar a planilha consolidada em arquivos de 1000 linhas cada (em memória)
        total_linhas = len(df_final)
        num_arquivos = (total_linhas // 1000) + (1 if total_linhas % 1000 != 0 else 0)
        arquivos_gerados = []
        
        for i in range(num_arquivos):
            inicio = i * 1000
            fim = (i + 1) * 1000
            parte = df_final.iloc[inicio:fim]
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                parte.to_excel(writer, index=False)
            output.seek(0)
            arquivos_gerados.append(output)
        
        spinner_placeholder.empty() # Remove o spinner após o processamento
        
        success_message = f"""
        <div class="success-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2E7D32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <h3 style="margin-top: 10px; margin-bottom: 5px;">Processamento concluído com sucesso!</h3>
            <p style="margin: 5px 0;">Total de linhas processadas: <strong>{total_linhas}</strong></p>
            <p style="margin: 5px 0;">Arquivos gerados: <strong>{num_arquivos}</strong></p>
        </div>
        """
        st.markdown(success_message, unsafe_allow_html=True)
        
        # Restaurar o botão original
        with button_placeholder:
            if st.button('🔄 PROCESSAR NOVAMENTE', key='importar_again'):
                st.session_state.processing = True
        
        return df_final, contas_sem_depara, arquivos_gerados
        
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
        spinner_placeholder.empty() # Garante que o spinner seja removido em caso de erro
        with button_placeholder:
            if st.button('🔄 PROCESSAR NOVAMENTE', key='importar_again'):
                st.session_state.processing = True
        return None, None, None

# Interface do aplicativo
def main():
    # Aplicar o CSS e JavaScript
    st.markdown(custom_css, unsafe_allow_html=True)
    html(particles_js, height=0, width=0)
    
    # Logo centralizada
    st.markdown(f"""
    <div class="logo-header">
        <img src="{LOGO_URL}" class="logo-img" alt="Logo RealI Consultoria">
    </div>
    <p class="subtitle">Consolidação automática de planilhas</p>
    """, unsafe_allow_html=True)
    
    # Card de instruções
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 style="color: #1565c0; margin-bottom: 1rem;">Instruções de Uso</h3>
            <ol style="color: #333; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.5rem;">Selecione os arquivos Excel/CSV no botão abaixo</li>
                <li style="margin-bottom: 0.5rem;">Clique em "Processar" para iniciar a consolidação</li>
                <li>Após o processamento, clique em "Baixar Arquivos" para obter os resultados</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Upload de arquivos
    uploaded_files = st.file_uploader(
        "📤 Selecione os arquivos para importar", 
        type=['xlsx', 'xls', 'csv'], 
        accept_multiple_files=True,
        help="Selecione os arquivos Excel ou CSV que deseja processar"
    )
    
    # Botão de processamento e placeholder para o spinner
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        button_placeholder = st.empty()
        spinner_placeholder = st.empty() # Placeholder para o spinner
        
        if 'processing' not in st.session_state:
            st.session_state.processing = False
            st.session_state.contas_sem_depara = None
            st.session_state.arquivos_gerados = None
        
        if not st.session_state.processing:
            if uploaded_files and button_placeholder.button('⚙️ PROCESSAR', key='processar'):
                st.session_state.processing = True
                st.rerun()
            elif not uploaded_files:
                button_placeholder.button('⚙️ PROCESSAR', key='processar_disabled', disabled=True)
        else:
            # Ao invés da barra de progresso, chamamos o processar_planilhas com o placeholder do spinner
            df_final, contas_sem_depara, arquivos_gerados = processar_planilhas(uploaded_files, spinner_placeholder, button_placeholder)
            
            if contas_sem_depara is not None:
                st.session_state.contas_sem_depara = contas_sem_depara
            if arquivos_gerados is not None:
                st.session_state.arquivos_gerados = arquivos_gerados
            
            time.sleep(1) # Pequena pausa para garantir que a mensagem de sucesso apareça
            spinner_placeholder.empty() # Garante que o spinner é removido ao final
            st.session_state.processing = False
    
    # Seção de download dos arquivos processados
    if st.session_state.get('arquivos_gerados'):
        st.markdown("---")
        
        # Botão para baixar todos os arquivos como ZIP
        zip_buffer = criar_zip_em_memoria(st.session_state.arquivos_gerados)
        st.download_button(
            label="📥 BAIXAR ARQUIVOS (ZIP)",
            data=zip_buffer,
            file_name="lancamentos_processados.zip",
            mime="application/zip",
            key='download_zip',
            help="Clique para baixar todos os arquivos processados em um ZIP",
            use_container_width=True
        )
    
    # Seção para contas sem depara
    if st.session_state.get('contas_sem_depara') is not None and not st.session_state.contas_sem_depara.empty:
        st.markdown("---")
        
        num_contas_sem_depara = len(st.session_state.contas_sem_depara)
        
        st.markdown(f"""
        <div class="contas-sem-depara-info">
            <strong>⚠️ Foram encontradas {num_contas_sem_depara} contas sem correspondência no depara.</strong><br>
            Você pode baixar a lista completa clicando no botão abaixo.
        </div>
        """, unsafe_allow_html=True)
        
        excel_file = criar_excel_em_memoria(st.session_state.contas_sem_depara)
        st.download_button(
            label="📥 BAIXAR CONTAS SEM DEPARA",
            data=excel_file,
            file_name="contas_sem_depara.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key='download_contas_sem_depara',
            help="Clique para baixar todas as contas que não foram encontradas no depara",
            use_container_width=True
        )
    
    
    # Rodapé
    st.markdown("""
    <footer>
        Desenvolvido por RealI Automação. © 2025
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
