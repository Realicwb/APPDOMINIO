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

# Configuração da página para remover a barra lateral
st.set_page_config(
    page_title="REALI CONSULTORIA",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado premium com container ampliado
custom_css = """
<style>
[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

/* Efeito de partículas */
.particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
}

.particle {
    position: absolute;
    background: rgba(76, 175, 80, 0.5);
    border-radius: 50%;
    pointer-events: none;
}

/* Animação de fundo gradiente premium */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Animação de flutuação 3D */
@keyframes float3D {
    0% { transform: translateY(0px) rotateX(0deg) rotateY(0deg); }
    50% { transform: translateY(-20px) rotateX(5deg) rotateY(5deg); }
    100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg); }
}

/* Efeito de pulso neon */
@keyframes pulseNeon {
    0% { box-shadow: 0 0 5px 0 rgba(76, 175, 80, 0.7), 0 0 20px 0 rgba(76, 175, 80, 0.5); }
    70% { box-shadow: 0 0 20px 15px rgba(76, 175, 80, 0), 0 0 40px 30px rgba(76, 175, 80, 0); }
    100% { box-shadow: 0 0 5px 0 rgba(76, 175, 80, 0), 0 0 20px 0 rgba(76, 175, 80, 0); }
}

/* Efeito de digitação */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

/* Efeito de cursor piscando */
@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: #4CAF50 }
}

/* Efeito de onda */
@keyframes wave {
    0% { transform: rotate(0deg); }
    10% { transform: rotate(14deg); }
    20% { transform: rotate(-8deg); }
    30% { transform: rotate(14deg); }
    40% { transform: rotate(-4deg); }
    50% { transform: rotate(10deg); }
    60% { transform: rotate(0deg); }
    100% { transform: rotate(0deg); }
}

/* Efeito de zoom suave */
@keyframes smoothZoom {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

body {
    background: linear-gradient(270deg, #0a192f, #172a45, #303f60, #4a648f);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    color: #f8f9fa;
    overflow-x: hidden;
}

/* CONTAINER PRINCIPAL AMPLIADO */
.stApp {
    background-color: rgba(10, 25, 47, 0.92);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3);
    padding: 3rem;
    max-width: 1200px;  /* AUMENTEI A LARGURA MÁXIMA */
    min-width: 900px;   /* ADICIONEI LARGURA MÍNIMA */
    margin: 3rem auto;
    border: 1px solid rgba(76, 175, 80, 0.2);
    animation: float3D 8s ease-in-out infinite;
    position: relative;
    z-index: 1;
    transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
    min-height: 80vh;   /* ADICIONEI ALTURA MÍNIMA */
}

.stApp:hover {
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
    transform: translateY(-5px) scale(1.005);
}

/* Botões premium com efeitos avançados */
.stButton>button {
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    color: white;
    border: none;
    padding: 20px 40px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 18px;
    margin: 12px 0;
    cursor: pointer;
    border-radius: 50px;
    transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 8px 16px rgba(46, 125, 50, 0.4);
    font-weight: 700;
    width: 100%;
    max-width: 400px;
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    z-index: 1;
    font-family: 'Poppins', sans-serif;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.stButton>button:hover {
    background: linear-gradient(135deg, #43A047 0%, #1B5E20 100%);
    transform: translateY(-8px) scale(1.05);
    box-shadow: 0 16px 24px rgba(46, 125, 50, 0.6);
    animation: pulseNeon 2s infinite;
}

.stButton>button:active {
    transform: translateY(4px) scale(0.98);
    box-shadow: 0 6px 12px rgba(46, 125, 50, 0.5);
    transition: all 0.1s;
}

.stButton>button:after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 10px;
    height: 10px;
    background: rgba(255, 255, 255, 0.6);
    opacity: 0;
    border-radius: 100%;
    transform: scale(1, 1) translate(-50%);
    transform-origin: 50% 50%;
    z-index: -1;
}

.stButton>button:focus:not(:active)::after {
    animation: ripple 1.2s ease-out;
}

@keyframes ripple {
    0% {
        transform: scale(0, 0);
        opacity: 0.6;
    }
    100% {
        transform: scale(50, 50);
        opacity: 0;
    }
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: -4px;
    left: -4px;
    right: -4px;
    bottom: -4px;
    z-index: -2;
    background: linear-gradient(135deg, #4CAF50, #81C784, #A5D6A7, #C8E6C9);
    background-size: 400%;
    border-radius: 54px;
    opacity: 0;
    transition: 0.7s;
    filter: blur(8px);
}

.stButton>button:hover::before {
    opacity: 0.8;
    animation: gradientBG 4s linear infinite;
}

/* Título com efeito de digitação */
.title-container {
    text-align: center;
    margin-bottom: 3rem;
}

.title {
    color: #64ffda;
    font-weight: 800;
    font-size: 2.8rem;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    position: relative;
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    border-right: 4px solid #64ffda;
}

.title::after {
    content: '';
    display: block;
    width: 120px;
    height: 4px;
    background: linear-gradient(90deg, #64ffda, transparent);
    margin: 15px auto;
    border-radius: 2px;
}

/* Mensagem de sucesso premium */
.success-message {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.2));
    color: #64ffda;
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    margin-top: 2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    border-left: 5px solid #64ffda;
    animation: slideIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
    transform-origin: top center;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(100, 255, 218, 0.2);
}

@keyframes slideIn {
    0% {
        opacity: 0;
        transform: perspective(600px) rotateX(-45deg) translateY(-30px);
    }
    100% {
        opacity: 1;
        transform: perspective(600px) rotateX(0deg) translateY(0);
    }
}

/* Card hover effects */
.card {
    transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
    background: rgba(23, 42, 69, 0.7);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(100, 255, 218, 0.1);
}

.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    background: rgba(23, 42, 69, 0.9);
    border: 1px solid rgba(100, 255, 218, 0.3);
}

/* Spinner personalizado */
.stSpinner>div>div {
    border-color: #64ffda transparent transparent transparent !important;
}

/* Tooltip premium */
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 220px;
    background-color: #1B5E20;
    color: #fff;
    text-align: center;
    border-radius: 8px;
    padding: 12px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 14px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(76, 175, 80, 0.3);
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Barra de progresso premium */
.progress-container {
    width: 100%;
    height: 8px;
    background: rgba(23, 42, 69, 0.8);
    border-radius: 4px;
    margin-top: 12px;
    overflow: hidden;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #64ffda, #4CAF50);
    border-radius: 4px;
    width: 0%;
    transition: width 0.4s ease;
    position: relative;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, 
                              rgba(255,255,255,0) 0%, 
                              rgba(255,255,255,0.3) 50%, 
                              rgba(255,255,255,0) 100%);
    animation: shine 2s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Botão de extrair premium */
.btn-extrair {
    background: linear-gradient(135deg, #FF5722 0%, #E64A19 100%) !important;
    box-shadow: 0 8px 16px rgba(230, 74, 25, 0.4) !important;
}

.btn-extrair:hover {
    background: linear-gradient(135deg, #F4511E 0%, #D84315 100%) !important;
    box-shadow: 0 16px 24px rgba(230, 74, 25, 0.6) !important;
    animation: pulseNeon 2s infinite !important;
}

/* Seção de contas sem depara premium */
.contas-sem-depara-info {
    background: rgba(255, 243, 224, 0.1);
    border-left: 4px solid #FF9800;
    padding: 1.5rem;
    border-radius: 0 12px 12px 0;
    margin: 2rem 0;
    font-size: 1rem;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 152, 0, 0.2);
    animation: smoothZoom 3s ease infinite;
}

/* Efeito de onda no ícone */
.wave {
    animation-name: wave;
    animation-duration: 2.5s;
    animation-iteration-count: infinite;
    transform-origin: 70% 70%;
    display: inline-block;
}

/* Responsividade premium */
@media (max-width: 1200px) {
    .stApp {
        max-width: 95%;
        min-width: auto;
        padding: 2.5rem;
        margin: 2rem auto;
    }
}

@media (max-width: 768px) {
    .stApp {
        padding: 2rem;
        margin: 1.5rem;
        border-radius: 20px;
        max-width: 95%;
    }
    
    .title {
        font-size: 2.2rem;
        animation: none;
        border-right: none;
        white-space: normal;
    }
    
    .stButton>button {
        padding: 18px 32px;
        font-size: 16px;
    }
    
    .card {
        padding: 1.5rem;
    }
}

/* Efeito de foco nos inputs */
.stTextInput>div>div>input:focus, 
.stFileUploader>div>div>div>div>button:focus {
    border-color: #64ffda !important;
    box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.3) !important;
}

/* Efeito de hover no file uploader */
.stFileUploader>div>div>div>div>button:hover {
    border-color: #64ffda !important;
    background-color: rgba(100, 255, 218, 0.1) !important;
}

/* Efeito de transição suave para todos os elementos */
* {
    transition: all 0.3s ease-out;
}
</style>
"""

# JavaScript para partículas animadas
particles_js = """
<script>
// Criação de partículas animadas
document.addEventListener('DOMContentLoaded', function() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);
    
    // Criar partículas
    const particleCount = 30;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Tamanho aleatório entre 2px e 6px
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Posição aleatória
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        // Opacidade aleatória
        particle.style.opacity = Math.random() * 0.6 + 0.1;
        
        // Animação individual
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 10;
        particle.style.animation = `float ${duration}s ease-in-out ${delay}s infinite alternate`;
        
        // Adicionar ao container
        particlesContainer.appendChild(particle);
    }
});
</script>
"""

# Função para criar um arquivo Excel em memória
def criar_excel_em_memoria(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contas sem depara')
    output.seek(0)
    return output

# Função para baixar o arquivo de regras do GitHub
def baixar_regras_github():
    url = "https://raw.githubusercontent.com/Realicwb/APPDOMINIO/main/Regras.xlsx"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except Exception as e:
        st.error(f"Erro ao baixar arquivo de regras: {str(e)}")
        return None

# Função para processar as planilhas
def processar_planilhas(arquivos_importados, progress_bar, button_placeholder):
    try:
        # Caminho da pasta de destino
        downloads_path = str(Path.home() / "Downloads")
        launch_path = os.path.join(downloads_path, "LAUNCH")
        
        # Atualizar progresso
        progress_bar.progress(5, text="Criando pasta de destino...")
        time.sleep(0.5)
        
        # Criar pasta LAUNCH se não existir
        os.makedirs(launch_path, exist_ok=True)
        
        # Baixar arquivo de regras do GitHub
        progress_bar.progress(10, text="Baixando arquivo de regras...")
        regras_file = baixar_regras_github()
        if regras_file is None:
            return None, None
        
        try:
            df_import1 = pd.read_excel(regras_file)
        except Exception as e:
            st.error(f"Erro ao ler arquivo de regras: {str(e)}")
            return None, None
        
        # Verificar se as colunas necessárias existem no arquivo de regras
        if not all(col in df_import1.columns for col in ['conta', 'conta contabil']):
            st.error("Arquivo de regras não contém as colunas necessárias ('conta', 'conta contabil')")
            return None, None
        
        progress_bar.progress(15, text="Processando arquivos importados...")
        time.sleep(0.5)
        
        # Processar arquivos importados
        dfs_import = []
        total_files = len(arquivos_importados)
        
        for i, uploaded_file in enumerate(arquivos_importados):
            try:
                progress_percent = 15 + int((i / total_files) * 30)
                progress_bar.progress(progress_percent, text=f"Processando arquivo {i+1} de {total_files}...")
                
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Verificar se as colunas necessárias existem
                required_cols = ['Data', 'conta', 'valor', 'valor2']
                if not all(col in df.columns for col in required_cols):
                    st.warning(f"Arquivo {uploaded_file.name} não contém todas as colunas necessárias {required_cols}")
                    continue
                
                dfs_import.append(df[required_cols])
            except Exception as e:
                st.warning(f"Erro ao ler arquivo {uploaded_file.name}: {str(e)}")
                continue
        
        if not dfs_import:
            st.error("Nenhum arquivo válido encontrado nos arquivos importados")
            return None, None
        
        progress_bar.progress(50, text="Concatenando dados...")
        time.sleep(0.5)
        
        df_import = pd.concat(dfs_import, ignore_index=True)
        
        progress_bar.progress(70, text="Mesclando dados...")
        time.sleep(0.5)
        
        # Fazer o merge das planilhas
        df_final = pd.merge(
            df_import,
            df_import1[['conta', 'conta contabil']],
            on='conta',
            how='left'
        )
        
        # Criar dataframe com contas sem depara (NAN)
        contas_sem_depara = df_final[df_final['conta contabil'].isna()].copy()
        contas_sem_depara = contas_sem_depara[['conta', 'Data', 'valor', 'valor2']]
        contas_sem_depara = contas_sem_depara.drop_duplicates(subset=['conta'])
        
        progress_bar.progress(80, text="Processando colunas...")
        time.sleep(0.5)
        
        # Selecionar e renomear colunas
        df_final = df_final[['Data', 'conta contabil', 'valor', 'valor2']]
        df_final.columns = ['Data', 'conta contabil', 'valor', 'valor2']
        
        # Remover os pontos da coluna 'conta contabil'
        df_final['conta contabil'] = df_final['conta contabil'].astype(str).str.replace('.', '', regex=False)
        
        # Remover linhas com conta contabil vazia
        df_final = df_final.dropna(subset=['conta contabil'])
        
        progress_bar.progress(90, text="Salvando arquivos...")
        time.sleep(0.5)
        
        # Salvar a planilha consolidada em arquivos de 1000 linhas cada
        total_linhas = len(df_final)
        num_arquivos = (total_linhas // 1000) + (1 if total_linhas % 1000 != 0 else 0)
        
        for i in range(num_arquivos):
            inicio = i * 1000
            fim = (i + 1) * 1000
            parte = df_final.iloc[inicio:fim]
            
            output_path = os.path.join(launch_path, f"planilha_consolidada_parte_{i+1}.xlsx")
            parte.to_excel(output_path, index=False)
        
        progress_bar.progress(100, text="Processamento concluído!")
        time.sleep(0.5)
        
        success_message = f"""
        <div class="success-message">
            <div class="wave">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#64ffda" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
            </div>
            <h3 style="margin-top: 16px; margin-bottom: 8px; color: #64ffda;">PROCESSAMENTO CONCLUÍDO COM SUCESSO!</h3>
            <p style="margin: 8px 0; color: #a8b2d1;">Total de linhas processadas: <strong style="color: #64ffda;">{total_linhas}</strong></p>
            <p style="margin: 8px 0; color: #a8b2d1;">Arquivos gerados: <strong style="color: #64ffda;">{num_arquivos}</strong></p>
            <p style="margin: 8px 0; color: #a8b2d1;">Salvo em: <strong style="color: #64ffda;">{launch_path}</strong></p>
        </div>
        """
        st.markdown(success_message, unsafe_allow_html=True)
        
        # Restaurar o botão original após a conclusão
        with button_placeholder:
            if st.button('🚀 PROCESSAR NOVAMENTE', key='importar_again', help="Clique para importar e consolidar as planilhas"):
                st.session_state.processing = True
        
        return df_final, contas_sem_depara
        
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
        progress_bar.empty()
        # Restaurar o botão original em caso de erro
        with button_placeholder:
            if st.button('🚀 PROCESSAR NOVAMENTE', key='importar_again', help="Clique para importar e consolidar as planilhas"):
                st.session_state.processing = True
        return None, None

# Interface do aplicativo
def main():
    # Aplicar o CSS e JavaScript
    st.markdown(custom_css, unsafe_allow_html=True)
    html(particles_js, height=0, width=0)
    
    # Título do aplicativo com efeito de digitação
    st.markdown("""
    <div class="title-container">
        <h1 class="title">📊 IMPORTADOR DE LANÇAMENTOS DOMINIO</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Descrição premium
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem; color: #a8b2d1; font-size: 1.1rem; line-height: 1.6; letter-spacing: 0.5px;">
        <p style="margin-bottom: 8px;">Esta ferramenta premium consolida automaticamente planilhas de diferentes formatos</p>
        <p style="margin-top: 0;">em um único arquivo padronizado para análise com tecnologia avançada.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal com efeito de card premium
    with st.container():
        st.markdown("""
        <div class="card">
            <h3 style="color: #64ffda; text-align: center; margin-bottom: 1.5rem; font-weight: 600;">INSTRUÇÕES DE USO</h3>
            <ol style="color: #a8b2d1; padding-left: 1.5rem; line-height: 1.8;">
                <li style="margin-bottom: 0.8rem;">Clique no botão <strong style="color: #64ffda;">"Importar Razões"</strong> para selecionar os arquivos Excel ou CSV</li>
                <li style="margin-bottom: 0.8rem;">Clique no botão <strong style="color: #64ffda;">"Processar"</strong> para iniciar a consolidação automatizada</li>
                <li style="margin-bottom: 0.8rem;">Acompanhe o progresso pela barra de carregamento animada</li>
                <li>Os arquivos consolidados serão salvos automaticamente na pasta <strong style="color: #64ffda;">LAUNCH</strong> dentro de Downloads</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Espaçamento
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    
    # Botão para importar arquivos com estilo premium
    uploaded_files = st.file_uploader(
        "📤 Importar Razões", 
        type=['xlsx', 'xls', 'csv'], 
        accept_multiple_files=True,
        help="Selecione os arquivos Excel ou CSV que deseja processar"
    )
    
    # Botão centralizado com efeitos especiais premium
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        button_placeholder = st.empty()
        
        if 'processing' not in st.session_state:
            st.session_state.processing = False
            st.session_state.contas_sem_depara = None
        
        if not st.session_state.processing:
            if uploaded_files and button_placeholder.button('🚀 INICIAR PROCESSAMENTO', key='processar', help="Clique para processar os arquivos importados"):
                st.session_state.processing = True
                st.rerun()
            elif not uploaded_files:
                button_placeholder.button('🚀 INICIAR PROCESSAMENTO', key='processar_disabled', disabled=True, help="Importe arquivos primeiro")
        else:
            # Criar uma barra de progresso premium
            progress_bar = st.progress(0, text="Preparando para processar...")
            
            # Chamar a função de processamento com a barra de progresso
            df_final, contas_sem_depara = processar_planilhas(uploaded_files, progress_bar, button_placeholder)
            
            # Armazenar contas sem depara na sessão
            if contas_sem_depara is not None:
                st.session_state.contas_sem_depara = contas_sem_depara
            
            # Remover a barra de progresso após um breve delay
            time.sleep(1)
            progress_bar.empty()
            st.session_state.processing = False
    
    # Seção para extrair contas sem depara (sem mostrar a tabela)
    if st.session_state.get('contas_sem_depara') is not None and not st.session_state.contas_sem_depara.empty:
        st.markdown("---")
        
        num_contas_sem_depara = len(st.session_state.contas_sem_depara)
        
        # Mensagem informativa sobre contas sem depara premium
        st.markdown(f"""
        <div class="contas-sem-depara-info">
            <strong style="color: #FF9800; font-size: 1.1rem;">⚠️ ATENÇÃO: {num_contas_sem_depara} CONTAS SEM CORRESPONDÊNCIA</strong><br>
            <p style="margin: 8px 0 0; color: #a8b2d1;">Foram identificadas contas que não possuem mapeamento no sistema. 
            Você pode baixar a lista completa para análise clicando no botão abaixo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão premium para baixar contas sem depara
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

if __name__ == "__main__":
    main()
