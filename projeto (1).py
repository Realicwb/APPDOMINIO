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

# --- Configuração da Página e CSS/JS Globais ---
st.set_page_config(
    page_title="REALI AUTOMAÇÃO",
    page_icon="https://www.realiconsultoria.com.br/wp-content/uploads/2022/02/cropped-fav_Prancheta-1-150x150.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# URL da logo
LOGO_URL = "https://raw.githubusercontent.com/Realicwb/APPDOMINIO/main/logo%20(1).png"

# CSS personalizado com tema claro e logo centralizada e animação de carregamento
custom_css = f"""
<style>
/* Esconde a barra lateral e o controle de recolher */
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

/* Estilo para o botão "Voltar" */
.back-button-container .stButton>button {{
    background: linear-gradient(135deg, #ff7043 0%, #e64a19 100%); /* Cor laranja/avermelhada */
    box-shadow: 0 4px 12px rgba(255, 112, 67, 0.2);
    max-width: 200px; /* Largura ajustada para o botão de voltar */
    margin-top: 20px; /* Margem superior para separação */
}}

.back-button-container .stButton>button:hover {{
    background: linear-gradient(135deg, #ff5722 0%, #d84315 100%);
    box-shadow: 0 8px 16px rgba(255, 112, 67, 0.3);
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

/* Formulário de login - ESTILO ATUALIZADO */
.login-container {{
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(30, 136, 229, 0.2);
    animation: float 6s ease-in-out infinite;
}}

.login-title {{
    text-align: center;
    color: #1565c0;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 600;
}}

.login-input {{
    margin-bottom: 1.5rem;
}}

.login-input label {{
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}}

.login-input input {{
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-sizing: border-box;
}}

.login-input input:focus {{
    border-color: #42a5f5;
    box-shadow: 0 0 0 3px rgba(66, 165, 245, 0.2);
    outline: none;
}}

.login-button {{
    width: 100%;
    margin-top: 1rem;
    padding: 12px;
    background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.login-button:hover {{
    background: linear-gradient(135deg, #3d9ae8 0%, #1976d2 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(30, 136, 229, 0.3);
}}

/* Estilo para os campos de entrada do Streamlit */
.stTextInput>div>div>input {{
    width: 100% !important;
    padding: 12px !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-sizing: border-box !important;
}}

.stTextInput>div>div>input:focus {{
    border-color: #42a5f5 !important;
    box-shadow: 0 0 0 3px rgba(66, 165, 245, 0.2) !important;
    outline: none !important;
}}

.stTextInput>label {{
    display: block !important;
    margin-bottom: 0.5rem !important;
    color: #333 !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
}}

/* Container para alinhar os campos de login */
.login-fields-container {{
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(30, 136, 229, 0.2);
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
    
    .login-container {{
        padding: 1.5rem;
        max-width: 100%;
    }}
    
    .login-fields-container {{
        padding: 1rem;
        max-width: 100%;
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

# --- Funções Auxiliares ---

# Função para formatar a data no padrão DD/MM/AAAA
def formatar_data(data):
    try:
        if pd.isna(data):
            return None
        if not isinstance(data, (datetime, pd.Timestamp)):
            data = pd.to_datetime(data, errors='coerce')
        return data.strftime('%d/%m/%Y')
    except:
        return None

# Função para criar um arquivo Excel em memória
def criar_excel_em_memoria(df, sheet_name='Sheet1'):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
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

# Função para processar as planilhas do Importador Domínio
def processar_planilhas_dominio(arquivos_importados, spinner_placeholder, button_placeholder):
    try:
        with spinner_placeholder:
            st.markdown("""
            <div class="loader-container">
                <div class="loader"></div>
                <div class="loader-text">Processando...</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("Baixando arquivo de regras...")

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
                # Inclui a coluna "Cta.cont./Nome PN" se existir no arquivo importado
                extra_cols = []
                if 'Cta.cont./Nome PN' in df.columns:
                    extra_cols.append('Cta.cont./Nome PN')
                cols_to_use = required_cols + extra_cols

                if not all(col in df.columns for col in required_cols):
                    st.warning(f"Arquivo {uploaded_file.name} não contém todas as colunas necessárias")
                    continue

                df['Conta controle'] = df['Conta controle'].astype(str).str.replace('.', '', regex=False)
                df = df.dropna(subset=['Conta controle'])
                df['Data'] = df['Data'].apply(formatar_data)
                df = df.dropna(subset=['Data'])

                dfs_import.append(df[cols_to_use])
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
        
        df_import1['Conta controle'] = df_import1['Conta controle'].astype(str).str.replace('.', '', regex=False)
        df_import1 = df_import1.dropna(subset=['Conta controle'])
        # REMOVE DUPLICIDADES NO DEPARA ANTES DO MERGE
        merge_cols = ['Conta controle', 'conta contabil']
        if 'Cta.cont./Nome PN' in df_import1.columns:
            merge_cols.append('Cta.cont./Nome PN')
        df_import1 = df_import1.drop_duplicates(subset=['Conta controle'])  # <-- ADICIONE ESTA LINHA

        df_final = pd.merge(
            df_import,
            df_import1[merge_cols],
            on='Conta controle',
            how='left'
        )
        
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
        
        # Seleciona as colunas finais, incluindo 'Cta.cont./Nome PN' se veio do import
        final_cols = ['Data', 'conta contabil', 'Débito', 'Crédito']
        if 'Cta.cont./Nome PN' in df_import.columns:
            final_cols.append('Cta.cont./Nome PN')
        df_final = df_final[final_cols]
        df_final.columns = final_cols

        df_final = df_final.dropna(subset=['conta contabil'])

        # Geração dos lançamentos
        lancamentos = []
        tem_nome_pn = 'Cta.cont./Nome PN' in df_final.columns
        for _, row in df_final.iterrows():
            # Lançamento de débito
            if pd.notna(row['Débito']) and row['Débito'] != 0:
                lanc = {
                    'Data': row['Data'],
                    'valor': row['Débito'],
                    'Débito': row['conta contabil'],
                    'Crédito': 266,
                    'Historico': ''
                }
                if tem_nome_pn:
                    lanc['Cta.cont./Nome PN'] = row['Cta.cont./Nome PN']
                lancamentos.append(lanc)
            # Lançamento de crédito
            if pd.notna(row['Crédito']) and row['Crédito'] != 0:
                lanc = {
                    'Data': row['Data'],
                    'valor': row['Crédito'],
                    'Débito': 266,
                    'Crédito': row['conta contabil'],
                    'Historico': ''
                }
                if tem_nome_pn:
                    lanc['Cta.cont./Nome PN'] = row['Cta.cont./Nome PN']
                lancamentos.append(lanc)
        df_lancamentos = pd.DataFrame(lancamentos)

        # Calcule o total de linhas e número de arquivos antes do loop
        total_linhas = len(df_lancamentos)
        num_arquivos = (total_linhas // 1000) + (1 if total_linhas % 1000 != 0 else 0)
        arquivos_gerados = []

        # Garante a ordem das colunas na exportação
        lanc_cols = ['Data', 'Débito', 'Crédito', 'valor', 'Historico']
        if 'Cta.cont./Nome PN' in df_lancamentos.columns:
            lanc_cols.append('Cta.cont./Nome PN')
        for i in range(num_arquivos):
            inicio = i * 1000
            fim = (i + 1) * 1000
            parte = df_lancamentos.iloc[inicio:fim]
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                parte.to_excel(writer, index=False, columns=lanc_cols)
            output.seek(0)
            arquivos_gerados.append(output)
        
        spinner_placeholder.empty()
        
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
        
        with button_placeholder:
            if st.button('🔄 PROCESSAR NOVAMENTE', key='importar_again'):
                st.session_state.processing_dominio = True
        
        return df_lancamentos, contas_sem_depara, arquivos_gerados
        
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
        spinner_placeholder.empty()
        with button_placeholder:
            if st.button('🔄 PROCESSAR NOVAMENTE', key='importar_again'):
                st.session_state.processing_dominio = True
        return None, None, None

# --- Telas do Aplicativo ---

def tela_importador_dominio():
    st.markdown(f"""
    <div class="logo-header">
        <img src="{LOGO_URL}" class="logo-img" alt="Logo RealI Consultoria">
    </div>
    <p class="subtitle">Consolidação automática de planilhas</p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Card de instruções
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 style="color: #1565c0; margin-bottom: 1rem;">Instruções de Uso - Importador Domínio</h3>
            <ol style="color: #333; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.5rem;">Selecione os arquivos Excel/CSV no botão abaixo</li>
                <li style="margin-bottom: 0.5rem;">Clique em "PROCESSAR" para iniciar a consolidação</li>
                <li>Após o processamento, clique em "BAIXAR ARQUIVOS" para obter os resultados</li>
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
        spinner_placeholder = st.empty()
        
        if 'processing_dominio' not in st.session_state:
            st.session_state.processing_dominio = False
            st.session_state.contas_sem_depara_dominio = None
            st.session_state.arquivos_gerados_dominio = None
        
        if not st.session_state.processing_dominio:
            if uploaded_files and button_placeholder.button('⚙️ PROCESSAR', key='processar_dominio'):
                st.session_state.processing_dominio = True
                st.rerun()
            elif not uploaded_files:
                button_placeholder.button('⚙️ PROCESSAR', key='processar_dominio_disabled', disabled=True)
        else:
            df_final, contas_sem_depara, arquivos_gerados = processar_planilhas_dominio(uploaded_files, spinner_placeholder, button_placeholder)
            
            if contas_sem_depara is not None:
                st.session_state.contas_sem_depara_dominio = contas_sem_depara
            if arquivos_gerados is not None:
                st.session_state.arquivos_gerados_dominio = arquivos_gerados
            
            time.sleep(1)
            spinner_placeholder.empty()
            st.session_state.processing_dominio = False

    # Seção de download dos arquivos processados
    if st.session_state.get('arquivos_gerados_dominio'):
        st.markdown("---")
        
        zip_buffer = criar_zip_em_memoria(st.session_state.arquivos_gerados_dominio)
        st.download_button(
            label="📥 BAIXAR ARQUIVOS (ZIP)",
            data=zip_buffer,
            file_name="lancamentos_processados_dominio.zip",
            mime="application/zip",
            key='download_zip_dominio',
            help="Clique para baixar todos os arquivos processados em um ZIP",
            use_container_width=True
        )
    
    # Seção para contas sem depara
    if st.session_state.get('contas_sem_depara_dominio') is not None and not st.session_state.contas_sem_depara_dominio.empty:
        st.markdown("---")
        
        num_contas_sem_depara = len(st.session_state.contas_sem_depara_dominio)
        
        st.markdown(f"""
        <div class="contas-sem-depara-info">
            <strong>⚠️ Foram encontradas {num_contas_sem_depara} contas sem correspondência no depara.</strong><br>
            Você pode baixar a lista completa clicando no botão abaixo.
        </div>
        """, unsafe_allow_html=True)
        
        excel_file = criar_excel_em_memoria(st.session_state.contas_sem_depara_dominio, sheet_name='Contas sem depara Domínio')
        st.download_button(
            label="📥 BAIXAR CONTAS SEM DEPARA",
            data=excel_file,
            file_name="contas_sem_depara_dominio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key='download_contas_sem_depara_dominio',
            help="Clique para baixar todas as contas que não foram encontradas no depara",
            use_container_width=True
        )

    # Botão de voltar na parte inferior esquerda
    st.markdown("<div class='back-button-container'>", unsafe_allow_html=True)
    if st.button('⬅️ VOLTAR PARA O INÍCIO', key='back_to_home_dominio_bottom', use_container_width=False):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def tela_cruzamento_ecd():
    st.markdown(f"""
    <div class="logo-header">
        <img src="{LOGO_URL}" class="logo-img" alt="Logo RealI Consultoria">
    </div>
    <p class="subtitle">Cruzamento e Análise de Balancetes ECD</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Card de instruções para Cruzamento ECD
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 style="color: #1565c0; margin-bottom: 1rem;">Instruções de Uso - Cruzamento ECD</h3>
            <ol style="color: #333; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.5rem;">Importe o <strong>Plano de Contas Referenciais</strong> da Receita Federal (Aba 'L100A').</li>
                <li style="margin-bottom: 0.5rem;">Importe o seu <strong>Balancete</strong> em formato Excel.</li>
                <li style="margin-bottom: 0.5rem;">Clique em <strong>"PROCESSAR"</strong> para cruzar os dados.</li>
                <li>O sistema identificará contas sem depara e gerará os resultados para download.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    # Inicialização do estado da sessão para esta tela
    if 'df_balancete_ecd' not in st.session_state:
        st.session_state.df_balancete_ecd = None
    if 'df_referencial_ecd' not in st.session_state:
        st.session_state.df_referencial_ecd = None
    if 'processing_ecd' not in st.session_state:
        st.session_state.processing_ecd = False
    if 'contas_sem_depara_ecd' not in st.session_state:
        st.session_state.contas_sem_depara_ecd = None
    if 'df_cruzado_ecd' not in st.session_state:
        st.session_state.df_cruzado_ecd = None
    if 'downloads_ecd' not in st.session_state:
        st.session_state.downloads_ecd = []

    col_upload_referencial, col_upload_balancete = st.columns(2)

    with col_upload_referencial:
        # Botão "IMPORTAR PLANO DE CONTAS REFERENCIAIS"
        uploaded_referencial = st.file_uploader(
            "⬆️ IMPORTAR PLANO DE CONTAS RFB",
            type=['xlsx', 'xls'],
            key='upload_referencial',
            help="Selecione o arquivo Excel do Plano de Contas Referenciais da Receita Federal."
        )
        if uploaded_referencial:
            try:
                # Carrega a planilha específica da Receita Federal
                st.session_state.df_referencial_ecd = pd.read_excel(
                    uploaded_referencial, 
                    sheet_name='L100A',
                    usecols=['CÓDIGO', 'DESCRIÇÃO']  # Apenas as colunas necessárias
                )
                st.session_state.df_referencial_ecd['CÓDIGO'] = st.session_state.df_referencial_ecd['CÓDIGO'].astype(str).str.strip()
                st.success(f"Plano de Contas Referenciais '{uploaded_referencial.name}' (Aba L100A) importado com sucesso!")
            except KeyError:
                st.error("A aba 'L100A' não foi encontrada no arquivo ou as colunas 'CÓDIGO' e 'DESCRIÇÃO' não existem.")
                st.session_state.df_referencial_ecd = None
            except Exception as e:
                st.error(f"Erro ao ler o arquivo do Plano de Contas Referenciais: {e}")
                st.session_state.df_referencial_ecd = None

    with col_upload_balancete:
        # Botão "IMPORTAR BALANCETE"
        uploaded_balancete = st.file_uploader(
            "📊 IMPORTAR BALANCETE",
            type=['xlsx', 'xls'],
            key='upload_balancete',
            help="Selecione o arquivo Excel do seu balancete ECD."
        )
        if uploaded_balancete:
            try:
                st.session_state.df_balancete_ecd = pd.read_excel(uploaded_balancete)
                # Verifica se a coluna AccountCode existe
                if 'AccountCode' not in st.session_state.df_balancete_ecd.columns:
                    st.error("A coluna 'AccountCode' não foi encontrada no balancete.")
                    st.session_state.df_balancete_ecd = None
                else:
                    st.session_state.df_balancete_ecd['AccountCode'] = st.session_state.df_balancete_ecd['AccountCode'].astype(str).str.strip()
                    st.success(f"Balancete '{uploaded_balancete.name}' importado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo Excel do balancete: {e}")
                st.session_state.df_balancete_ecd = None

    st.markdown("---")

    # Botão "PROCESSAR"
    col_processar1, col_processar2, col_processar3 = st.columns([1,2,1])
    with col_processar2:
        button_processar_placeholder = st.empty()
        spinner_processar_placeholder = st.empty()

        if not st.session_state.processing_ecd:
            if st.session_state.df_balancete_ecd is not None and st.session_state.df_referencial_ecd is not None:
                if button_processar_placeholder.button('⚙️ PROCESSAR', key='processar_ecd'):
                    st.session_state.processing_ecd = True
                    st.rerun()
            else:
                button_processar_placeholder.button('⚙️ PROCESSAR', key='processar_ecd_disabled', disabled=True)
        else:
            # Lógica de processamento e cruzamento
            with spinner_processar_placeholder:
                st.markdown("""
                <div class="loader-container">
                    <div class="loader"></div>
                    <div class="loader-text">Processando cruzamento...</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1) # Simula um tempo de processamento

                try:
                    df_balancete = st.session_state.df_balancete_ecd.copy()
                    df_referencial = st.session_state.df_referencial_ecd.copy()

                    # Realiza o cruzamento pela coluna "CÓDIGO" da planilha de referência e "AccountCode" do balancete
                    df_cruzado = pd.merge(
                        df_balancete,
                        df_referencial,
                        left_on='AccountCode',
                        right_on='CÓDIGO',
                        how='left'
                    )
                    
                    st.session_state.df_cruzado_ecd = df_cruzado
                    
                    # Identificar contas sem depara
                    contas_sem_depara = df_cruzado[df_cruzado['CÓDIGO'].isna()][['AccountCode']].drop_duplicates()
                    st.session_state.contas_sem_depara_ecd = contas_sem_depara
                    
                    # Prepara os arquivos para download
                    excel_cruzado = criar_excel_em_memoria(df_cruzado, sheet_name='Balancete Cruzado')
                    st.session_state.downloads_ecd = [excel_cruzado]
                    
                    if not contas_sem_depara.empty:
                        excel_sem_depara = criar_excel_em_memoria(contas_sem_depara, sheet_name='Contas sem Depara')
                        st.session_state.downloads_ecd.append(excel_sem_depara)
                    
                    success_message = f"""
                    <div class="success-message">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2E7D32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                        <h3 style="margin-top: 10px; margin-bottom: 5px;">Cruzamento concluído com sucesso!</h3>
                        <p style="margin: 5px 0;">Total de contas cruzadas: <strong>{len(df_cruzado)}</strong></p>
                        <p style="margin: 5px 0;">Contas sem depara: <strong>{len(contas_sem_depara)}</strong></p>
                    </div>
                    """
                    st.markdown(success_message, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erro durante o processamento do cruzamento: {e}")
                    st.session_state.df_cruzado_ecd = None
                    st.session_state.contas_sem_depara_ecd = None
                    st.session_state.downloads_ecd = []
            
            spinner_processar_placeholder.empty()
            st.session_state.processing_ecd = False
            # Re-renderiza o botão para permitir novo processamento ou desabilitá-lo
            if st.session_state.df_balancete_ecd is not None and st.session_state.df_referencial_ecd is not None:
                button_processar_placeholder.button('⚙️ PROCESSAR NOVAMENTE', key='processar_ecd_again')
            else:
                button_processar_placeholder.button('⚙️ PROCESSAR', key='processar_ecd_disabled_after', disabled=True)

    # Seção de DOWNLOADS após o processamento
    if st.session_state.get('df_cruzado_ecd') is not None and not st.session_state.processing_ecd:
        st.markdown("---")
        st.subheader("📥 DOWNLOADS")
        
        # Cria um container para os botões de download
        download_container = st.container()
        
        with download_container:
            # Download do arquivo cruzado
            st.download_button(
                label="📥 BAIXAR BALANCETE CRUZADO",
                data=st.session_state.downloads_ecd[0],
                file_name="balancete_cruzado_ecd.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key='download_cruzado_ecd',
                help="Baixa o balancete com as contas referenciais cruzadas.",
                use_container_width=True
            )

            # Seção para contas sem depara
            if len(st.session_state.downloads_ecd) > 1:
                num_contas_sem_depara = len(st.session_state.contas_sem_depara_ecd)
                
                st.markdown(f"""
                <div class="contas-sem-depara-info">
                    <strong>⚠️ Foram encontradas {num_contas_sem_depara} contas no balancete sem correspondência no plano referencial.</strong><br>
                </div>
                """, unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 BAIXAR CONTAS SEM DEPARA (ECD)",
                    data=st.session_state.downloads_ecd[1],
                    file_name="contas_sem_depara_ecd.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key='download_sem_depara_ecd',
                    help="Baixa a lista de contas do balancete que não foram encontradas no plano referencial.",
                    use_container_width=True
                )
    
    # Botão de voltar na parte inferior esquerda
    st.markdown("<div class='back-button-container'>", unsafe_allow_html=True)
    if st.button('⬅️ VOLTAR PARA O INÍCIO', key='back_to_home_ecd_bottom', use_container_width=False):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# --- Tela de Login ---
def tela_login():
    st.markdown(f"""
    <div class="logo-header">
        <img src="{LOGO_URL}" class="logo-img" alt="Logo RealI Consultoria">
    </div>
    <p class="subtitle">Acesso Restrito</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Container para os campos de login - agora usando os componentes nativos do Streamlit
    with st.container():
        st.markdown("""
        <div class="login-fields-container">
            <h3 class="login-title">AUTENTICAÇÃO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Usando os componentes nativos do Streamlit com estilos personalizados
        username = st.text_input("Login", key="username_input")
        password = st.text_input("Senha", type="password", key="password_input")
        
        if st.button("ACESSAR", key="login_button", use_container_width=True):
            if username == "ADMIN" and password == "REALI@2025":
                st.session_state.logged_in = True
                st.session_state.page = 'home'
                st.rerun()
            else:
                st.error("Credenciais inválidas. Tente novamente.")

# --- Função Principal do Aplicativo ---
def app():
    # Aplicar o CSS e JavaScript no início
    st.markdown(custom_css, unsafe_allow_html=True)
    html(particles_js, height=0, width=0)

    # Inicializa o estado da página e login se não existir
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Verifica se o usuário está logado
    if not st.session_state.logged_in:
        tela_login()
        return

    # Renderiza a página com base no estado
    if st.session_state.page == 'home':
        tela_inicial()
    elif st.session_state.page == 'importador_dominio':
        tela_importador_dominio()
    elif st.session_state.page == 'cruzamento_ecd':
        tela_cruzamento_ecd()
    elif st.session_state.page == 'login':
        tela_login()

    # Rodapé (comum a todas as telas, exceto login)
    if st.session_state.page != 'login':
        st.markdown("""
        <footer>
            Desenvolvido por RealI Automação. © 2025
        </footer>
        """, unsafe_allow_html=True)

# --- Tela Inicial ---
def tela_inicial():
    st.markdown(f"""
    <div class="logo-header">
        <img src="{LOGO_URL}" class="logo-img" alt="Logo RealI Consultoria">
    </div>
    <p class="subtitle">Bem-vindo à Automação RealI!</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1565c0; margin-bottom: 1rem;">Importador Domínio</h3>
            <p>Automatize a importação e consolidação de lançamentos do sistema Domínio.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button('➡️ IMPORTADOR DOMINIO', key='btn_dominio', use_container_width=True):
            st.session_state.page = 'importador_dominio'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1565c0; margin-bottom: 1rem;">Cruzamento ECD</h3>
            <p>Realize cruzamentos e análises com seus balancetes do ECD.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button('➡️ CRUZAMENTO ECD', key='btn_ecd', use_container_width=True):
            st.session_state.page = 'cruzamento_ecd'
            st.rerun()

    # Botão de logout
    st.markdown("<div class='back-button-container'>", unsafe_allow_html=True)
    if st.button('🔒 SAIR', key='logout_button', use_container_width=False):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
