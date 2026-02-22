import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
from typing import Dict, List, Any, Optional, Tuple, Callable
import hashlib
import uuid
from streamlit_option_menu import option_menu
import re

# ==========================================
# IMPORTS PARA ANÁLISE AVANÇADA (Humanidades Digitais)
# ==========================================
# Imports condicionais para evitar quebra se bibliotecas não estiverem instaladas
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Backend não-interativo para Streamlit
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

except ImportError:
    SEABORN_AVAILABLE = False

try:
    from pyvis.network import Network
    import streamlit.components.v1 as components
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False

try:
    from collections import Counter
    import string
    
    # Tentativa de usar NLTK (conforme solicitado no plano avançado)
    try:
        import nltk
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        from nltk.corpus import stopwords
        STOP_WORDS_PT = set(stopwords.words('portuguese'))
        NLP_AVAILABLE = True
    except (ImportError, Exception):
        # Fallback para lista embutida caso NLTK falhe
        STOP_WORDS_PT = {
            'a', 'à', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'às',
            'até', 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois',
            'do', 'dos', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'era', 'eram',
            'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes', 'eu', 'foi',
            'fomos', 'for', 'fora', 'foram', 'forem', 'formos', 'fosse', 'fossem', 'fui', 'há',
            'isso', 'isto', 'já', 'lhe', 'lhes', 'lo', 'mais', 'mas', 'me', 'mesmo', 'meu',
            'meus', 'minha', 'minhas', 'muito', 'na', 'não', 'nas', 'nem', 'no', 'nos', 'nós',
            'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'o', 'os', 'ou', 'para', 'pela',
            'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 'que', 'quem', 'são', 'se', 'seja',
            'sejam', 'sejamos', 'sem', 'ser', 'será', 'serão', 'seria', 'seriam', 'seríamos',
            'seu', 'seus', 'só', 'somos', 'sou', 'sua', 'suas', 'também', 'te', 'tem', 'tém',
            'temos', 'tenha', 'tenham', 'tenhamos', 'tenho', 'ter', 'teu', 'teus', 'ti', 'tido',
            'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram',
            'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tu', 'tua', 'tuas',
            'um', 'uma', 'umas', 'uns', 'você', 'vocês', 'vos', 'vossa', 'vossas', 'vosso',
            'vossos', 'ainda', 'assim', 'bem', 'bom', 'cada', 'coisa', 'coisas', 'dele', 'desse',
            'desses', 'dessa', 'dessas', 'deste', 'destes', 'desta', 'destas', 'disto', 'daquele',
            'daqueles', 'daquela', 'daquelas', 'daquilo', 'donde', 'então', 'etc', 'fazer', 'feito',
            'grande', 'grandes', 'há', 'isto', 'lá', 'la', 'lo', 'lugar', 'maior', 'maiores',
            'melhor', 'melhores', 'menor', 'menores', 'menos', 'mesma', 'mesmas', 'mesmos', 'muita',
            'muitas', 'muitos', 'nada', 'nela', 'nelas', 'nele', 'neles', 'nenhum', 'nenhuma',
            'nesse', 'nesses', 'nessa', 'nessas', 'neste', 'nestes', 'nesta', 'nestas', 'ninguém',
            'nisso', 'nisto', 'novo', 'novos', 'onde', 'ora', 'outra', 'outras', 'outro', 'outros',
            'parte', 'partes', 'pois', 'pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras',
            'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios', 'qual', 'quais',
            'qualquer', 'quase', 'quatro', 'segundo', 'segunda', 'sempre', 'ser', 'seus', 'tal',
            'tais', 'tanto', 'tantos', 'tanta', 'tantas', 'ter', 'toda', 'todas', 'todo', 'todos',
            'três', 'tudo', 'última', 'últimas', 'último', 'últimos', 'vai', 'vão', 'vários',
            'várias', 'ver', 'vez', 'vezes', 'vindo', 'vir', 'sobre', 'sob', 'sendo', 'sido',
            'tendo', 'tendo', 'partir', 'através', 'apenas', 'alguns', 'algumas', 'algum', 'alguma',
            'algo', 'aqui', 'ali', 'aí', 'lá', 'cá', 'lhe', 'lhes', 'me', 'mim', 'nos', 'vos',
            'si', 'consigo', 'comigo', 'contigo', 'conosco', 'convosco'
        }
        NLP_AVAILABLE = True

    # Tentar importar SPACY para análise gramatical mais robusta (Substantivos/Adjetivos)
    try:
        import spacy
        try:
            # Tenta carregar modelo pequeno para português
            nlp_spacy = spacy.load("pt_core_news_sm")
            SPACY_AVAILABLE = True
        except OSError:
            # Tenta baixar se não encontrar e carrega novamente
            from spacy.cli import download
            download("pt_core_news_sm")
            nlp_spacy = spacy.load("pt_core_news_sm")
            SPACY_AVAILABLE = True
    except Exception:
        SPACY_AVAILABLE = False
        nlp_spacy = None
        
except Exception:
    NLP_AVAILABLE = False
    STOP_WORDS_PT = set()
    SPACY_AVAILABLE = False

# ==========================================
# CONSTANTES GLOBAIS
# ==========================================
ORDEM_SIBILA = ["0", "1", "2", "3", "4", "5", "6", "7", "8-9", "10", "11", "12"]

# ==========================================
# 1. CONFIGURAÇÃO E ESTILO
# ==========================================

st.set_page_config(
    page_title="SISTEMA NELIC - SIBILA",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Vocabulário Controlado e Metodologia (agora em um módulo de dados)
# (Dados movidos para dentro da classe DataModule para encapsulamento)
# Tipos textuais que NÃO exigem resumo analítico
# Tipos textuais que NÃO exigem resumo analítico
TIPOS_SEM_RESUMO = {"POEMA", "POEMA(S)", "FICÇÃO", "CAPA", "IMAGEM", "HQ/CHARGE", "HQ", "CHARGE", "ARTES PLÁSTICAS"}

# Mapeamento de Autores Canônicos (Normalização de Nomes)
CANONICAL_AUTHORS = {
    # BACH
    "BACH": "BACH, Johann Sebastian",
    "BACH, J. S.": "BACH, Johann Sebastian",
    "BACH, Johann S.": "BACH, Johann Sebastian",
    
    # NOVAS REGRAS
    "ADORNO, Theodor": "ADORNO, Theodor W.",
    "ALIGHIERI, DANTE": "ALIGHIERI, Dante",
    "ALLEN, Donald": "ALLEN, Donald M.",
    "ALVIM, Chico": "ALVIM, Francisco",
    "ARAÚJO, Lais Corrêa de": "ARAÚJO, Laís Corrêa de",
    "ARISTÓTELES, Aristóteles": "ARISTÓTELES",
    "BALL": "BALL, Hugo",
    "BUENO": "BUENO, Wilson",
    "BYRON": "BYRON, Lord",
    "CABRAL, João": "CABRAL, João (de Melo Neto)",
    "CABRAL, João (Melo Neto)": "CABRAL, João (de Melo Neto)",
    "CAMÕES, Luís de": "CAMÕES, Luís Vaz de",
    "CAYMMI, Dori": "CAYMMI, Dorival",
    "CHOPIN, Fryderyk": "CHOPIN, Frédéric",
    "CLARK, Lígia": "CLARK, Lygia",
    "CORBUSIER, LE": "CORBUSIER, Le",
    "CRISTOBO, Anibal": "CRISTOBO, Aníbal",
    "CUMMINGS, E. E.": "CUMMINGS, e. e.",
    "CUMMINGS, e.e.": "CUMMINGS, e. e.",
    "DAO, BEI": "DAO, Bei",
    "DICK, André": "DICK, André Henrique",
    "DOLHNIKOFF, Luís": "DOLHNIKOFF, Luis",
    
    # NOVAS REGRAS (LOTE 2)
    "DRUMMOND, Carlos": "DRUMMOND, Carlos (de Andrade)",
    "DRUMMOND, Drummond": "DRUMMOND, Carlos (de Andrade)",
    "ANDRADE, Carlos Drummond de": "DRUMMOND, Carlos (de Andrade)",
    "DUFRÊNE": "DUFRÊNE, François",
    "EISENSTEIN, Sergei": "EISENSTEIN, Sergei M.",
    "ELIOT, T.S.": "ELIOT, T. S.",
    "FERRARI, Léon": "FERRARI, León",
    "FERREIRA": "FERREIRA, Evandro Affonso",
    "FONTANA": "FONTANA, Lucio",
    "FROTA": "FROTA, Eduardo",
    "GIL": "GIL, Gilberto",
    "GOETHE": "GOETHE, Johann Wolfgang von",
    "GOLDSMITH, Kenny": "GOLDSMITH, Kenneth",

    # NOVAS REGRAS (LOTE 3)
    "GUIMARÃES, Júlio C.": "GUIMARÃES, Júlio Castañon",
    "HOLLANDA, Heloisa Buarque de": "HOLLANDA, Heloísa Buarque de",
    "JOBIM, Tom": "JOBIM, Antônio Carlos",
    "JOHNSON": "JOHNSON, Robert",
    "JOYCE": "JOYCE, James",
    "KHLIÉBNIKOV, Vielímir": "KHLIÉBNIKOV, Velimir",
    "KHLÉBNIKOV, Velimir": "KHLIÉBNIKOV, Velimir",
    "KHLÉBNIKOV, Velímir": "KHLIÉBNIKOV, Velimir",
    "KOZER, Jos": "KOZER, José",
    "KOZER, Jose": "KOZER, José",
    "LAUTRÉAMONT": "LAUTRÉAMONT, Conde de",
    "LEITE, Sebastião Uchôa": "LEITE, Sebastião Uchoa",
    "LIMA, Manoel Ricardo": "LIMA, Manoel Ricardo de",
    "MAIAKÓVSKI": "MAIAKÓVSKI, Vladímir",
    "MAIAKÓVSKI, Vladimir": "MAIAKÓVSKI, Vladímir",
    "MANDELSTAM, Óssip": "MANDELSTAM, Osip",
    "MORAES, Vinícius de": "MORAES, Vinicius de",
    "MORAIS, Vinícius de": "MORAES, Vinicius de",
    "MOURA, Antonio": "MOURA, Antônio",
    "MÃE, Valter Hugo": "MÃE, valter hugo",
    "NEZVAL, Vitezlav": "NEZVAL, Vítězslav",
    "PASTERNAK": "PASTERNAK, Boris",
    "PETRARCA": "PETRARCA, Francesco",
    "PLAZA, Júlio": "PLAZA, Julio",
    
    # NOVAS REGRAS (LOTE 4)
    "PUSHKIN": "PUSHKIN, Alexander",
    "RODRÍGUEZ, Américo": "RODRIGUES, Américo",
    "ROQUETTE-PINTO, Cláudia": "ROQUETTE-PINTO, Claudia",
    "ROSA, Guimarães": "ROSA, João Guimarães",
    "ROSA, Mario Alex": "ROSA, Mário Alex",
    "ROTHENBERG, Gerome": "ROTHENBERG, Jerome",
    "SABINSON, Eric": "SABINSON, Eric Mitchell",
    "SALOMÃO, Wally": "SALOMÃO, Waly",
    "SALVINO, Rômullo Valle": "SALVINO, Romulo Valle",
    "SALVINO, Romullo Valle": "SALVINO, Romulo Valle",
    "SALVINO, Rômulo Valle": "SALVINO, Romulo Valle",
    "SOSA, Víctor": "SOSA, Victor",
    "SOUSÂNDRADE, Joaquim de": "SOUSÂNDRADE",
    "SOUSÂNDRADE, Joaquim de Sousa Andrade": "SOUSÂNDRADE",
    "VICUÑA, Cecília": "VICUÑA, Cecilia",
    "WARCHAVCHIK, Gregorio": "WARCHAVCHIK, Gregori",
    "WEBERN, Anton von": "WEBERN, Anton",
    "WOOLF, Virgínia": "WOOLF, Virginia",
    "XAVIER": "XAVIER, Valêncio",
    "ÁVILA, Afonso": "ÁVILA, Affonso",
    
    # NOVAS REGRAS (LOTE 5 - Pente Fino)
    "COSTA, Lúcio": "COSTA, Lucio",
    "SALVINO, Rômulo Valle": "SALVINO, Romulo Valle",
    "SALVINO, Romullo Valle": "SALVINO, Romulo Valle",
}

# Caminhos de arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'catalogo_sibila.json')
DIARIO_PATH = os.path.join(BASE_DIR, 'diario_sibila.json')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
LOGO_PATH = os.path.join(BASE_DIR, 'NELIC.png')  # Arquivo de Logo

# Estilos CSS
CSS_STYLES = """
<style>
.main { 
    background: radial-gradient(circle at top left, #f5f7fb 0%, #f1f3f5 40%, #eceff1 100%);
    padding-top: 1rem;
}
.block-container {
    padding-top: 2.2rem;
    max-width: 1300px;
}
.stDeployButton {display: none !important;}
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
.viewerBadge_container__1QSob {display: none !important;}
.styles_viewerBadge__1yB5_ {display: none !important;}
h1 {
    color: #1f2933;
    font-weight: 800 !important;
    text-transform: uppercase;
    border-bottom: 3px solid #2f5f98;
    padding-bottom: 10px;
    margin-bottom: 20px;
    font-size: 2rem !important;
    letter-spacing: 1px;
}
h2, h3, h4 { 
    color: #243b53;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 1.5rem;
    letter-spacing: 0.06em;
}
/* ===== SIDEBAR - FUNDO BRANCO LIMPO ===== */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Texto da sidebar em azul escuro */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: #366092 !important;
}

/* LOGO: Sem inversão para fundo branco */
[data-testid="stSidebar"] img {
    filter: none;
    opacity: 1;
}

/* Input de senha - estilo para fundo branco */
[data-testid="stSidebar"] input {
    background-color: #f8f9fa !important;
    color: #366092 !important;
    border: 1px solid #d0d7de !important;
}

[data-testid="stSidebar"] input::placeholder {
    color: #8a9ab0 !important;
}

/* Alinhamento do tooltip (?) ao lado do label */
[data-testid="stSidebar"] label {
    display: flex !important;
    align-items: center !important;
    gap: 0.25rem !important;
}

[data-testid="stSidebar"] .stTooltipIcon {
    margin-left: 0 !important;
    vertical-align: middle !important;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 999px;
    font-weight: 600;
    text-transform: uppercase;
    width: 100%;
    transition: all 0.25s ease;
    border: 1px solid #2f5f98;
    background-color: #2f5f98;
    color: white;
    letter-spacing: 0.06em;
    font-size: 0.78rem;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.18);
    background-color: #23466f;
    border-color: #23466f;
}
.stTextArea textarea {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 0.95rem;
    line-height: 1.6;
    border-radius: 6px;
    padding: 0.75rem;
}
.stTextInput input {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 0.95rem;
    line-height: 1.5;
}
.nelic-card {
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.8rem;
    background: #ffffff;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow: 0 8 20px rgba(15, 23, 42, 0.04);
}
.nelic-card-header {
    font-weight: 700;
    color: #1f2933;
    margin-bottom: 0.35rem;
    font-size: 0.92rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.nelic-card-subtitle {
    color: #62748a;
    font-size: 0.8rem;
    margin-bottom: 0.35rem;
}
.nelic-tag {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    border-radius: 999px;
    background-color: #e3edff;
    color: #243b53;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.nelic-tag-muted {
    background-color: #e5e7eb;
    color: #4b5563;
}
.nelic-muted {
    color: #6b7b93;
    font-size: 0.8rem;
}
div[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1f2933;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7b93;
}
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 8 18px rgba(15, 23, 42, 0.06);
    background-color: white;
}
button[data-baseweb="tab"] {
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.info-box {
    background-color: #e3f2fd;
    border-left: 4px solid #2f5f98;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
}
.warning-box {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
}
.success-box {
    background-color: #e8f5e9;
    border-left: 4px solid #4caf50;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
}
/* Estilos Metodologia Sóbria */
.metod-section {
    background: #f9fafb;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    border: 1px solid #e5e7eb;
}
.metod-section h4 {
    color: #374151;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #d1d5db;
}
.metod-section p, .metod-section li {
    color: #4b5563;
    font-size: 0.95rem;
    line-height: 1.7;
}
.metod-section ul {
    margin: 0.75rem 0;
    padding-left: 1.5rem;
}
.metod-section li {
    margin-bottom: 0.5rem;
}
.metod-section strong {
    color: #1f2937;
    font-weight: 600;
}
</style>
"""

st.markdown(CSS_STYLES, unsafe_allow_html=True)

# ==========================================
# 2. CLASSES E MÓDULOS
# ==========================================

class DataModule:
    """Encapsula dados estáticos e funções de normalização."""
    LISTA_PALAVRAS_CHAVE = sorted(list(set([x.title() for x in [
        "Absurdo", "Adolescência", "África", "Agricultura", "Alegoria", "Alemanha", "Alimentação", "Amazônia",
        "Ambivalência", "América", "América Latina", "Amor", "Análise Do Discurso", "Anarquismo", "Antiguidade",
        "Antologia", "Antropologia", "Argentina", "Arqueologia", "Arquitetura", "Arte",
        "Arte Gráfica", "Artes Plásticas", "Artesanato", "Astrologia", "Áustria", "Autonomia", "Autoria",
        "Autoritarismo", "Barroco", "Best Seller", "Bíblia", "Biblioteca", "Biografia", "Biologia", "Bossa Nova",
        "Brasil", "Bruxaria", "Burguesia", "Câmbio", "Cânone Literário", "Capitalismo", "Caricatura", "Carnaval",
        "Cartas", "Casamento", "Catolicismo", "Censura", "Chanchada", "Chile", "China", "Cidade", "Ciência",
        "Cinema", "Cinema Novo", "Classe", "Classe Média", "Colonialismo", "Comédia", "Cômico", "Competência",
        "Comportamento", "Compromisso", "Comunicação", "Comunismo", "Colonização", "Concretismo", "Concurso",
        "Consumo", "Contemporâneo", "Conto", "Contra Cultura", "Crenças Populares", "Criação", "Crise",
        "Crítica", "Crônica", "Cuba", "Cultura", "Cultura Alternativa", "Cultura Popular", "Dadaísmo", "Dança",
        "Década De 20", "Década De 30", "Década De 40", "Década De 50", "Década De 60", "Década De 70",
        "Década De 80", "Década De 90", "Democracia", "Demografia", "Descolonização", "Desconhecimento",
        "Desconstrução", "Design", "Despotismo", "Dialética", "Direito", "Direitos Autorais", "Discos",
        "Discriminação", "Discurso", "Ditadura", "Documentário", "Drama", "Dramaturgia", "Drogas", "Ecletismo",
        "Ecologia", "Economia", "Editor", "Educação", "Efeméride", "Elite", "Enciclopedismo", "Energia",
        "Engajamento Político", "Ensaio", "Ensino", "Entretenimento", "Epistemologia", "Erotismo",
        "Escola De Frankfurt", "Escravidão", "Escritor", "Escritura", "Escultura", "Exoterismo", "Espaço",
        "Espanha", "Esporte", "Estado", "Estado Novo", "Estados Unidos", "Estética", "Estrutura",
        "Estruturalismo", "Ética", "Etnografia", "Etno-história", "Etnologia", "Europa", "Eventos",
        "Existencialismo", "Experimentalismo", "Expressionismo", "Fantástico", "Fascismo", "Feminismo",
        "Fenomenologia", "Ficção", "Ficção Científica", "Filologia", "Filosofia", "Física", "Folclore",
        "Folhetim", "Formalismo", "Fotografia", "França", "Funcionalismo", "Futebol", "Futurismo", "Genealogia",
        "Gênero", "Geografia", "Geração De 45", "Geração Marginal", "Globalização", "Golpe Militar", "Grafite",
        "Gramática", "Guerra", "Guerra Fria", "Hermenêutica", "Herói", "Heterogeneidade", "Hispano-América",
        "História", "História Do Brasil", "História Em Quadrinhos", "Historiografia", "Homossexualidade",
        "Humanismo", "Humor", "Idade Média", "Idealização", "Identidade", "Ideograma", "Ideologia", "Idioma",
        "Igreja", "Iluminismo", "Imagem", "Imaginação", "Imigração", "Imperialismo", "Imprensa",
        "Imprensa Alternativa", "Impressionismo", "Inconfidência Mineira", "Inconsciente", "Independência",
        "Índia", "Indianismo", "Índio", "Indústria Cultural", "Industrialização", "Infância", "Informática",
        "Informes", "Inglaterra", "Instituições", "Intelectual", "Interdisciplinar", "Intelectualidade",
        "Invenção", "Ironia", "Itália", "Japão", "Jazz", "Jornalismo", "Judaísmo", "Justiça", "Kitsch", "Leitor",
        "Liberalismo", "Liberdade", "Língua", "Língua Inglesa", "Língua Portuguesa", "Linguagem", "Linguística",
        "Lírico", "Lirismo", "Literatura", "Literatura Comparada", "Literatura De Cordel",
        "Literatura Infanto-juvenil", "Literatura Policial", "Livro Didático", "Livros", "Lógica", "Loucura",
        "Luta De Classes", "Magia", "Mais-valia", "Manifesto", "Marginalidade", "Marxismo", "Matemática",
        "Mato Grosso", "Medicina", "Memória", "Mercado", "Mercado Editorial", "Mercado Fonográfico",
        "Metafísica", "Metáfora", "Metalinguagem", "Metodologia De Pesquisa", "Métrica", "México", "Mídia",
        "Mimesis", "Minas Gerais", "Minoria Sociais", "Misticismo", "Mito", "Mitologia", "Moda", "Modernidade",
        "Modernismo", "Monarquia", "Monopólio", "Moral", "Morte", "Movimento", "Movimento Ideológico", "MPB",
        "Mulher", "Museu", "Música", "Música Erudita", "Música Popular", "Nação", "Nacionalismo", "Narrador",
        "Narrativa", "Naturalismo", "Natureza", "Nazismo", "Negros", "Neoconcretismo", "Neurologia", "Nordeste",
        "Nova República", "Novela", "Obra", "Obra De Arte", "Ocidente", "Oligarquia", "Ontologia", "Ópera",
        "Oralidade", "Oriente", "Origem", "Originalidade", "Paraná", "Parnasianismo", "Paródia",
        "Partido Comunista", "Pastiche", "Patrimônio Cultural", "Pedagogia", "Periferia", "Periodismo",
        "Peronismo", "Personagem", "Pintura", "Plágio", "Pluralismo", "Poder", "Poema Épico", "Poema Processo",
        "Poema Visual", "Poesia Marginal", "Poesia", "Poética", "Polêmica", "Polícia", "Polifonia", "Política",
        "Polônia", "Pop Art", "Populismo", "Pornografia", "Portugal", "Pós-estruturalismo", "Positivismo",
        "Pós-modernidade", "Pós Modernismo", "Pré História", "Prêmio", "Premio Nobel", "Privatizações",
        "Proletariado", "Prostituição", "Proto-sátira", "Psicanálise", "Psicologia", "Psicoterapia",
        "Psiquiatria", "Publicidade", "Química", "Racismo", "Rádio", "Razão", "Reação", "Ready-made", "Realismo",
        "Realismo Fantástico", "Realismo Mágico", "Rebeldia", "Reforma Agrária", "Regime Político",
        "Regionalismo", "Relações Internacionais", "Relações Raciais", "Relações Sociais", "Relato", "Religião",
        "Renascimento", "Reportagem", "Representação", "Repressão", "República", "República Velha", "Retórica",
        "Revolução", "Revolução De 1930", "Revolução Francesa", "Revolução Industrial", "Rio De Janeiro",
        "Rio Grande Do Sul", "Rito", "Rock And Roll", "Romance", "Romantismo", "Ruptura", "Rússia", "Samba",
        "São Paulo", "Sátira", "Saúde", "SBPC", "Século XIX", "Século XVI", "Século XVII", "Século XVIII",
        "Século XX", "Século XXI", "Semana De Arte Moderna", "Semântica", "Semiologia", "Semiótica", "Servilismo",
        "Sexualidade", "Silêncio", "Simbolismo", "Simbologia", "Sindicalismo", "Sínteses", "Socialismo",
        "Sociedade", "Sociedade Industrial", "Sociologia", "Solidão", "Stalinismo", "Subdesenvolvimento",
        "Sujeito", "Surrealismo", "Tatuagem", "Teatro", "Técnica", "Tecnocracia", "Tecnologia", "Telespectador",
        "Televisão", "Tempo", "Teologia", "Teoria", "Teoria Da Linguagem", "Teoria Literária", "Teoria Social",
        "Terrorismo", "Texto", "Tortura", "Trabalho", "Tradição", "Tradução", "Tragédia", "Traição",
        "Transgressão", "Tropicalismo", "Umbanda", "Underground", "Unidade", "Universalidade", "Universidade",
        "Urbanismo", "URSS", "Uruguai", "Utopia", "Vanguarda", "Verdade", "Vestibular", "Viagem", "Violência"
    ]])))

    LISTA_ICONOGRAFIA = [
        "Cartografia", "Fac-símile", "Foto", "Fotograma", "Gráfico/Tabela",
        "HQ/Charge", "Ilustração", "Publicidade", "Reprodução"
    ]

    # Referência ao dicionário global para acesso dentro da classe se necessário
    CANONICAL_AUTHORS = CANONICAL_AUTHORS

    TIPOS_TEXTUAIS = {
        "APRESENTAÇÃO": ["Sem especificação", "Literatura"],
        "ARTES PLÁSTICAS": ["Sem especificação"],
        "CAPA": ["Sem especificação"],
        "CARTAS DO LEITOR": ["Sem especificação"],
        "CHARGE": ["Sem especificação"],
        "CORRESPONDÊNCIA(S)": ["Sem especificação"],
        "DEBATE": ["Sem especificação"],
        "DEPOIMENTO": ["Sem especificação", "Literatura"],
        "EDITORIAL": ["Sem especificação", "Literatura"],
        "ENSAIO": [
            "Sem especificação", "Antropologia", "Arquitetura", "Bibliologia", "Ciência",
            "Comunicação", "Cultura", "Economia", "Educação", "Esporte", "Filosofia",
            "Fotográfico", "História", "Linguística", "Literatura", "Política",
            "Psicanálise", "Psicologia", "Sociologia", "Teologia"
        ],
        "ENTREVISTA": ["Sem especificação", "Literatura"],
        "FICÇÃO": ["Sem especificação"],
        "HQ": ["Sem especificação"],
        "HQ/CHARGE": ["Sem especificação"],
        "INFORME": ["Sem especificação", "Literatura"],
        "POEMA(S)": ["Sem especificação"],
        "REPORTAGEM": ["Sem especificação", "Literatura"],
        "RESENHA": [
            "Sem especificação", "Antropologia", "Arquitetura", "Bibliologia", "Ciência",
            "Comunicação", "Cultura", "Economia", "Educação", "Filosofia", "História",
            "Linguística", "Literatura", "Política", "Psicanálise", "Psicologia", "Sociologia"
        ],
        "VARIEDADES": ["Sem especificação"]
    }

    @staticmethod
    def normalizar_texto(val: str | list) -> str | list:
        """Normaliza texto genérico (palavras-chave etc.) para Title Case."""
        if isinstance(val, list):
            return [i.strip().title() for i in val if str(i).strip()]
        if isinstance(val, str):
            return val.strip().title()
        return val

    @staticmethod
    def format_nome_abnt(nome: str | None) -> str:
        """
        Normaliza nomes pessoais segundo ABNT.
        Ex.: 'Bonvicino, Régis' -> 'BONVICINO, Régis'
        """
        if nome is None:
            return ""
        if not isinstance(nome, str):
            nome = str(nome)
        
        # 0. Verificação de Autores Canônicos (Normalização prévia)
        # Verifica se o nome exato (ou variante simples) está na lista
        if nome.strip() in DataModule.CANONICAL_AUTHORS:
             return DataModule.CANONICAL_AUTHORS[nome.strip()]
        
        # Verifica também se variantes comuns estão na lista (ex: "Bach" -> "BACH, Johann Sebastian")
        # Mas cuidado para não pegar substrings indevidas. Aqui verifica match exato da string limpa.
        
        s = " ".join(nome.strip().split())
        
        # Check again with standardized spacing
        if s in DataModule.CANONICAL_AUTHORS:
             return DataModule.CANONICAL_AUTHORS[s]

        if not s:
            return ""
        if "," in s:
            ult, resto = s.split(",", 1)
            return f"{ult.strip().upper()}, {resto.strip()}" if resto.strip() else ult.strip().upper()
        partes = s.split()
        if len(partes) >= 2:
            sobrenome = partes[-1].upper()
            prenomes = " ".join(partes[:-1])
            return f"{sobrenome}, {prenomes}"
        return s.upper()

    @staticmethod
    def parse_multiline(texto: str | None) -> list[str]:
        if texto is None:
            return []
        if not isinstance(texto, str):
            texto = str(texto)
        # Split only on newlines to preserve commas in ABNT format names
        linhas = texto.split('\n')
        return [l.strip() for l in linhas if l.strip()]

    @staticmethod
    def normalizar_lista_autores(texto: str | list) -> list[str]:
        nomes = DataModule.parse_multiline(texto)
        return [DataModule.format_nome_abnt(n) for n in nomes]

    @staticmethod
    def get_normalized_series(df: pd.DataFrame, col: str) -> pd.Series:
        """
        Explode coluna, remove vazios. Para campos de autor, aplica formatação ABNT
        sem rebaixar para Title Case (preserva SOBRENOME em CAIXA ALTA).
        """
        if col not in df.columns:
            return pd.Series(dtype='object')
        s = (
            df.explode(col)[col]
            .dropna()
            .astype(str)
            .str.strip()
            .replace('', pd.NA)
            .dropna()
        )
        if col in {'autores_colaboradores', 'autores_citados', 'tradutores', 'entidade_coletiva', 'nome_pessoal_como_assunto'}:
            s = s.apply(DataModule.format_nome_abnt)
        return s

# ==========================================
# FUNÇÃO DE ROTAÇÃO DE BACKUPS
# ==========================================

def limpar_backups_antigos(diretorio, manter=3):
    """
    Remove backups antigos, mantendo apenas os N mais recentes.

    Args:
        diretorio: Caminho do diretório de backups
        manter: Número de backups mais recentes a manter (padrão: 3)
    """
    try:
        if not os.path.exists(diretorio):
            return

        # Listar todos os arquivos de backup
        backups = []
        for arquivo in os.listdir(diretorio):
            caminho_completo = os.path.join(diretorio, arquivo)
            if os.path.isfile(caminho_completo):
                # Obter tempo de criação do arquivo
                tempo_criacao = os.path.getctime(caminho_completo)
                backups.append((tempo_criacao, caminho_completo, arquivo))

        # Ordenar por data de criação (mais recente primeiro)
        backups.sort(reverse=True, key=lambda x: x[0])

        # Se houver mais de N backups, apagar os antigos
        if len(backups) > manter:
            for _, caminho, nome in backups[manter:]:
                try:
                    os.remove(caminho)
                except Exception as e:
                    print(f"Erro ao remover backup {nome}: {e}")

    except Exception as e:
        print(f"Erro na limpeza de backups: {e}")

class PersistenceModule:
    """Encapsula funções de carregamento e salvamento de dados."""
    @staticmethod
    @st.cache_data(ttl=60)
    def load_data():
        if not os.path.exists(FILE_PATH):
            return []
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            return []

    @staticmethod
    def save_data(data):
        try:
            if os.path.exists(FILE_PATH):
                if not os.path.exists(BACKUP_DIR):
                    os.makedirs(BACKUP_DIR)
                bkp = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(FILE_PATH, 'r', encoding='utf-8') as f:
                    with open(os.path.join(BACKUP_DIR, bkp), 'w', encoding='utf-8') as b:
                        json.dump(json.load(f), b, ensure_ascii=False, indent=2)
                # Limpar backups antigos, mantendo apenas os 3 mais recentes
                limpar_backups_antigos(BACKUP_DIR, manter=3)
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            PersistenceModule.load_data.clear()
            return True
        except Exception as e:
            st.error(f"Erro ao salvar dados: {str(e)}")
            return False

    @staticmethod
    def load_diario():
        if not os.path.exists(DIARIO_PATH):
            return []
        try:
            with open(DIARIO_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Erro ao carregar diário: {str(e)}")
            return []

    @staticmethod
    def save_diario(entries):
        try:
            with open(DIARIO_PATH, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar diário: {str(e)}")
            return False

class PDFModule:
    """Encapsula funções de geração de PDF."""
    @staticmethod
    def to_latin1(texto):
        if texto is None:
            return ""
        if not isinstance(texto, str):
            texto = str(texto)
        # Mapa de substituição de caracteres problemáticos
        replacements = {
            '\u201c': '"',  # Aspas duplas esquerda
            '\u201d': '"',  # Aspas duplas direita
            '\u2018': "'",  # Aspas simples esquerda
            '\u2019': "'",  # Aspas simples direita
            '\u2013': '-',  # Traço médio
            '\u2014': '-',  # Travessão
            '\u2022': '*'   # Bullet point
        }
        for char, repl in replacements.items():
            texto = texto.replace(char, repl)
        
        return texto.encode('latin-1', 'replace').decode('latin-1')

    @staticmethod
    def add_nelic_logo_to_pdf(pdf):
        if os.path.exists(LOGO_PATH):
            try:
                # Logo fixo na direita (x=175, y=8, w=25)
                pdf.image(LOGO_PATH, x=175, y=8, w=25, h=0)
            except Exception:
                pass

    @staticmethod
    def _add_standard_header(pdf, title):
        """
        Cabeçalho Padrão (Global):
        - Logo: Canto superior direito (via add_nelic_logo_to_pdf)
        - Título: Alinhado à ESQUERDA, negrito, largura controlada.
        - Data: Alinhada à ESQUERDA, abaixo do título.
        - Linha Divisória: Obrigatória.
        """
        PDFModule.add_nelic_logo_to_pdf(pdf)
        
        # Título
        pdf.set_xy(10, 10) # Texto começa na esquerda, alinhado ao topo visual do logo
        pdf.set_font("Arial", 'B', 14)
        # Limpeza: Remover prefixos se existirem, embora o ideal seja passar o título limpo
        clean_title = title.replace("ESTATÍSTICAS - ", "").upper()
        
        # Largura controlada (160) para não cobrir o logo (x=175)
        pdf.multi_cell(160, 8, PDFModule.to_latin1(clean_title), align='L')
        
        # Data
        pdf.set_font("Arial", 'I', 10)
        pdf.set_x(10)
        pdf.cell(160, 6, PDFModule.to_latin1(f"Emissão: {datetime.now().strftime('%d/%m/%Y')}"), ln=True, align='L')
        
        # Linha Divisória
        # Garante que a linha fique abaixo do texto E do logo (assumindo logo h~25mm -> y_end ~33mm)
        y_line = max(pdf.get_y() + 2, 35)
        pdf.line(10, y_line, 200, y_line)
        pdf.set_y(y_line + 5)

    @staticmethod
    def gerar_pdf_analitico(df, total, crit):
        """Relatório analítico genérico (lista de registros) com % na base."""
        try:
            pdf = FPDF()
            pdf.add_page()
            PDFModule._add_standard_header(pdf, "RELATÓRIO ANALÍTICO - PROJETO SIBILA")
            
            pdf.set_y(pdf.get_y() + 5)
            pdf.set_y(40)
            pdf.set_fill_color(240, 240, 240)
            pdf.rect(10, 45, 190, 25, 'F')
            pdf.set_y(48)
            pdf.set_x(15)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, PDFModule.to_latin1(f"Critério: {crit}"), ln=True)
            pdf.set_x(15)
            pdf.set_font("Arial", '', 11)
            qtd = len(df)
            pct = (qtd / total * 100) if total > 0 else 0
            pdf.cell(0, 6, PDFModule.to_latin1(f"Registros encontrados: {qtd} de {total} (total da base)"), ln=True)
            pdf.set_x(15)
            pdf.cell(0, 6, PDFModule.to_latin1(f"Percentual da base total: {pct:.2f}%"), ln=True)
            pdf.ln(15)
            for _, r in df.iterrows():
                if pdf.get_y() > 250:
                    pdf.add_page()
                try:
                    tit = PDFModule.to_latin1(r.get('titulo_artigo', ''))
                    tip = PDFModule.to_latin1(r.get('vocabulario_controlado', ''))
                    rev = PDFModule.to_latin1(r.get('n', ''))
                    # Limpeza de páginas para evitar "p. p."
                    raw_pag = str(r.get('paginas', '')).replace('pp.', '').replace('p.', '').strip()
                    pags = PDFModule.to_latin1(raw_pag)
                    pdf.set_font("Arial", 'B', 11)
                    pdf.multi_cell(0, 6, f"[{tip}] REVISTA {rev} / p. {pags}")
                    if tit:
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, tit)
                    aut = r.get('autores_colaboradores', [])
                    if aut:
                        if isinstance(aut, list):
                            s_aut = ', '.join([DataModule.format_nome_abnt(a) for a in aut if a])
                        else:
                            s_aut = DataModule.format_nome_abnt(aut)
                        s_aut = PDFModule.to_latin1(s_aut)
                        # Bloco de autores: Rótulo em Negrito, conteúdo Normal
                        pdf.set_font("Arial", 'B', 10)
                        pdf.write(5, PDFModule.to_latin1("Autores: "))
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, s_aut)
                    nota_ed = r.get('nota_edicao', '')
                    if nota_ed:
                        ne = PDFModule.to_latin1(nota_ed)
                        pdf.set_font("Arial", 'I', 9)
                        pdf.multi_cell(0, 5, f"Nota de edição: {ne}")
                    icons = r.get('iconografias', [])
                    if isinstance(icons, list) and icons:
                        icon_txt = []
                        for ic in icons:
                            t = ic.get('tipo', '')
                            d = ic.get('descricao', '')
                            if t or d:
                                icon_txt.append(f"{t}: {d}")
                        if icon_txt:
                            s_icon = PDFModule.to_latin1(" | ".join(icon_txt))
                            pdf.set_font("Arial", 'I', 9)
                            pdf.set_text_color(100, 100, 100)
                            pdf.multi_cell(0, 5, f"[Iconografia]: {s_icon}")
                            pdf.set_text_color(0, 0, 0)
                    res = r.get('resumo', '')
                    if res:
                        resumo_txt = PDFModule.to_latin1(res)
                        # REMOVIDA LIMITAÇÃO: imprime resumo completo sem corte
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, resumo_txt)
                    pdf.ln(5)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(5)
                except Exception:
                    continue
            return pdf.output(dest='S').encode('latin-1', 'replace')
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {str(e)}")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, PDFModule.to_latin1("Erro ao gerar relatório"), ln=True)
            return pdf.output(dest='S').encode('latin-1', 'replace')

    @staticmethod
    def gerar_pdf_busca_analitica(df_reg, total_base, crit, df_citados=None, df_colab=None):
        """
        Relatório da aba EXPLORAR DADOS, incluindo:
        - Critérios de busca
        - Nº de registros e % na base
        - Resumo de 'Autores citados' e 'Autores colaboradores' (tabelas da seleção)
        - Lista de registros
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            PDFModule._add_standard_header(pdf, "RELATÓRIO DE BUSCA - PROJETO SIBILA")

            pdf.set_y(pdf.get_y() + 5)
            pdf.set_fill_color(240, 240, 240)
            pdf.rect(10, 45, 190, 30, 'F')
            pdf.set_y(48)
            pdf.set_x(15)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, PDFModule.to_latin1(f"Critério(s): {crit}"), ln=True)
            qtd = len(df_reg)
            pct = (qtd / total_base * 100) if total_base > 0 else 0
            pdf.set_x(15)
            pdf.set_font("Arial", '', 11)
            pdf.cell(0, 6, PDFModule.to_latin1(f"Registros encontrados: {qtd} de {total_base} (total da base)"), ln=True)
            pdf.set_x(15)
            pdf.cell(0, 6, PDFModule.to_latin1(f"Percentual da base total: {pct:.2f}%"), ln=True)
            pdf.ln(10)
            if df_citados is not None and not df_citados.empty:
                pdf.set_font("Arial", 'B', 11)
                pdf.multi_cell(0, 6, PDFModule.to_latin1("Autores citados na seleção"))
                pdf.set_font("Arial", '', 10)
                for _, row in df_citados.head(10).iterrows():
                    if pdf.get_y() > 260:
                        pdf.add_page()
                        pdf.set_font("Arial", 'B', 11)
                        pdf.multi_cell(0, 6, PDFModule.to_latin1("Autores citados na seleção (cont.)"))
                        pdf.set_font("Arial", '', 10)
                    linha = f"- {row['Termo']}: {row['Qtd']} ocorrência(s) ({row['%']})"
                    pdf.multi_cell(0, 5, PDFModule.to_latin1(linha))
                pdf.ln(6)
            if df_colab is not None and not df_colab.empty:
                pdf.set_font("Arial", 'B', 11)
                pdf.multi_cell(0, 6, PDFModule.to_latin1("Autores colaboradores na seleção"))
                pdf.set_font("Arial", '', 10)
                for _, row in df_colab.head(10).iterrows():
                    if pdf.get_y() > 260:
                        pdf.add_page()
                        pdf.set_font("Arial", 'B', 11)
                        pdf.multi_cell(0, 6, PDFModule.to_latin1("Autores colaboradores na seleção (cont.)"))
                        pdf.set_font("Arial", '', 10)
                    linha = f"- {row['Termo']}: {row['Qtd']} ocorrência(s) ({row['%']})"
                    pdf.multi_cell(0, 5, PDFModule.to_latin1(linha))
                pdf.ln(8)
            pdf.set_font("Arial", 'B', 11)
            pdf.multi_cell(0, 6, PDFModule.to_latin1("Registros da seleção"))
            pdf.ln(3)
            for _, r in df_reg.iterrows():
                if pdf.get_y() > 250:
                    pdf.add_page()
                try:
                    tit = PDFModule.to_latin1(r.get('titulo_artigo', ''))
                    tip = PDFModule.to_latin1(r.get('vocabulario_controlado', ''))
                    rev = PDFModule.to_latin1(r.get('n', ''))
                    # Limpeza de páginas para evitar "p. p."
                    raw_pag = str(r.get('paginas', '')).replace('pp.', '').replace('p.', '').strip()
                    pags = PDFModule.to_latin1(raw_pag)
                    pdf.set_font("Arial", 'B', 11)
                    pdf.multi_cell(0, 6, f"[{tip}] REVISTA {rev} / p. {pags}")
                    if tit:
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, tit)
                    aut = r.get('autores_colaboradores', [])
                    if aut:
                        if isinstance(aut, list):
                            s_aut = ', '.join([DataModule.format_nome_abnt(a) for a in aut if a])
                        else:
                            s_aut = DataModule.format_nome_abnt(aut)
                        s_aut = PDFModule.to_latin1(s_aut)
                        # Bloco de autores: Rótulo em Negrito, conteúdo Normal
                        pdf.set_font("Arial", 'B', 10)
                        pdf.write(5, PDFModule.to_latin1("Autores: "))
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, s_aut)
                    nota_ed = r.get('nota_edicao', '')
                    if nota_ed:
                        ne = PDFModule.to_latin1(nota_ed)
                        pdf.set_font("Arial", 'I', 9)
                        pdf.multi_cell(0, 5, f"Nota de edição: {ne}")
                    res = r.get('resumo', '')
                    if res:
                        resumo_txt = PDFModule.to_latin1(res)
                        # REMOVIDA LIMITAÇÃO: imprime resumo completo sem corte
                        pdf.set_font("Arial", '', 10)
                        pdf.multi_cell(0, 5, resumo_txt)
                    pdf.ln(5)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(5)
                except Exception:
                    continue
            return pdf.output(dest='S').encode('latin-1', 'replace')
        except Exception as e:
            st.error(f"Erro ao gerar PDF da busca: {str(e)}")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, PDFModule.to_latin1("Erro ao gerar relatório de busca"), ln=True)
            return pdf.output(dest='S').encode('latin-1', 'replace')

    @staticmethod
    def gerar_pdf_ficha(registro):
        try:
            pdf = FPDF()
            pdf.add_page()
            PDFModule._add_standard_header(pdf, "FICHA NELIC – PROJETO SIBILA")
            
            pdf.set_y(pdf.get_y() + 5)
            pdf.set_y(40)
            def safe(text):
                return PDFModule.to_latin1(text)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("1. IDENTIFICAÇÃO"), ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, safe(f"Nº revista: {registro.get('n','')}"))
            pdf.multi_cell(0, 5, safe(f"Registro: {registro.get('registro','')}"))
            
            # Limpeza de páginas para evitar "p. p."
            raw_pag = str(registro.get('paginas', '')).replace('pp.', '').replace('p.', '').strip()
            pdf.multi_cell(0, 5, safe(f"Páginas: p. {raw_pag}"))
            
            pdf.multi_cell(0, 5, safe(f"Tipo textual: {registro.get('vocabulario_controlado','')}"))
            pdf.multi_cell(
                0, 5,
                safe(f"Idiomas: {registro.get('idioma_01','')} / {registro.get('idioma_02','')}")
            )
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("2. RESPONSABILIDADE AUTORAL"), ln=True)
            pdf.set_font("Arial", '', 10)
            colab = registro.get('autores_colaboradores', [])
            entidade = registro.get('entidade_coletiva', [])
            trad = registro.get('tradutores', [])
            nome_ass = registro.get('nome_pessoal_como_assunto', [])
            if colab:
                lst = colab if isinstance(colab, list) else [colab]
                s = ", ".join(DataModule.format_nome_abnt(x) for x in lst)
                pdf.multi_cell(0, 5, safe(f"Colaboradores: {s}"))
            if entidade:
                lst = entidade if isinstance(entidade, list) else [entidade]
                s = ", ".join(DataModule.format_nome_abnt(x) for x in lst)
                pdf.multi_cell(0, 5, safe(f"Entidade Coletiva: {s}"))
            if trad:
                lst = trad if isinstance(trad, list) else [trad]
                s = ", ".join(DataModule.format_nome_abnt(x) for x in lst)
                pdf.multi_cell(0, 5, safe(f"Tradutores: {s}"))
            if nome_ass:
                lst = nome_ass if isinstance(nome_ass, list) else [nome_ass]
                s = ", ".join(DataModule.format_nome_abnt(x) for x in lst)
                pdf.multi_cell(0, 5, safe(f"Nome pessoal como assunto: {s}"))
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("3. CONTEÚDO"), ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, safe(f"Título: {registro.get('titulo_artigo','')}"))
            sub = registro.get('subtitulo_artigo', '')
            if sub:
                pdf.multi_cell(0, 5, safe(f"Subtítulo: {sub}"))
            nota_ed = registro.get('nota_edicao', '')
            if nota_ed:
                pdf.multi_cell(0, 5, safe(f"Nota de edição: {nota_ed}"))
            res = registro.get('resumo', '')
            if res:
                pdf.ln(1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 4, safe(res))
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("4. ASSUNTOS"), ln=True)
            pdf.set_font("Arial", '', 10)
            kw = registro.get('palavras_chave', [])
            aut_cit = registro.get('autores_citados', [])
            if kw:
                s = ", ".join(kw) if isinstance(kw, list) else kw
                pdf.multi_cell(0, 5, safe(f"Palavras-chave: {s}"))
            if aut_cit:
                lst = aut_cit if isinstance(aut_cit, list) else [aut_cit]
                s = ", ".join(DataModule.format_nome_abnt(x) for x in lst)
                pdf.multi_cell(0, 5, safe(f"Autores citados: {s}"))
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("5. ICONOGRAFIA"), ln=True)
            pdf.set_font("Arial", '', 10)
            icons = registro.get('iconografias', [])
            if icons:
                for ic in icons:
                    linha = f"- {ic.get('tipo','')}: {ic.get('descricao','')}"
                    pdf.multi_cell(0, 5, safe(linha))
            else:
                pdf.multi_cell(0, 5, safe("Sem iconografia registrada."))
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 6, safe("6. NOTAS DE PESQUISA"), ln=True)
            pdf.set_font("Arial", '', 10)
            notas = registro.get('notas_pesquisa', [])
            if notas:
                for n in sorted(notas, key=lambda x: x.get('data', ''), reverse=True):
                    data_str = n.get('data', '')[:10]
                    t = n.get('titulo', '')
                    txt = n.get('texto', '')
                    tags = n.get('tags', [])
                    pdf.set_font("Arial", 'B', 9)
                    pdf.multi_cell(0, 4, safe(f"[{data_str}] {t}"))
                    if tags:
                        pdf.set_font("Arial", 'I', 8)
                        pdf.multi_cell(0, 4, safe("Tags: " + ", ".join(tags)))
                    pdf.set_font("Arial", '', 9)
                    pdf.multi_cell(0, 4, safe(txt))
                    pdf.ln(1)
            else:
                pdf.multi_cell(0, 5, safe("Sem notas vinculadas a este registro até o momento."))
            return pdf.output(dest='S').encode('latin-1', 'replace')
        except Exception as e:
            st.error(f"Erro ao gerar ficha em PDF: {str(e)}")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, PDFModule.to_latin1("Erro ao gerar ficha"), ln=True)
            return pdf.output(dest='S').encode('latin-1', 'replace')

    @staticmethod
    def gerar_pdf_tabela_estatistica(df_stats, titulo):
        """
        Gera PDF apenas com tabela de estatísticas (campo, num. absoluto, percentual),
        seguindo o modelo dos relatórios de tipos textuais e palavras-chave do sistema original.
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            # Título limpo (sem "ESTATÍSTICAS - " se vier do argumento, mas a função _add_standard_header já trata)
            PDFModule._add_standard_header(pdf, titulo)
            
            cols = list(df_stats.columns)
            n_cols = len(cols)
            available_width = 190
            col_width = available_width / n_cols if n_cols > 0 else available_width
            
            # Cabeçalho da Tabela: Azul Escuro (#2f5f98) com texto Branco e Negrito
            pdf.set_fill_color(47, 95, 152) 
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 10)
            for col in cols:
                pdf.cell(col_width, 8, PDFModule.to_latin1(str(col)), border=1, align='C', fill=True)
            pdf.ln()
            
            # Corpo da Tabela
            pdf.set_text_color(0, 0, 0) # Reset para preto
            pdf.set_font("Arial", '', 9)
            
            for i, (_, row) in enumerate(df_stats.iterrows()):
                # Zebra striping: linhas alternadas
                if i % 2 == 0:
                    pdf.set_fill_color(255, 255, 255) # Branco
                else:
                    pdf.set_fill_color(240, 240, 240) # Cinza claro
                
                # Quebra de página
                if pdf.get_y() > 265:
                    pdf.add_page()
                    # Re-imprimir cabeçalho
                    pdf.set_fill_color(47, 95, 152)
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", 'B', 10)
                    for col in cols:
                        pdf.cell(col_width, 8, PDFModule.to_latin1(str(col)), border=1, align='C', fill=True)
                    pdf.ln()
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", '', 9)
                    # Restaurar cor de fundo da linha atual
                    if i % 2 == 0:
                        pdf.set_fill_color(255, 255, 255)
                    else:
                        pdf.set_fill_color(240, 240, 240)

                for col in cols:
                    val = row[col]
                    # Formatação numérica: 2 casas decimais para floats
                    if isinstance(val, float):
                        txt = f"{val:.2f}"
                    else:
                        txt = str(val)
                    
                    txt = PDFModule.to_latin1(txt)
                    # Números sempre centralizados
                    pdf.cell(col_width, 6, txt, border=1, align='C', fill=True)
                pdf.ln()
            return pdf.output(dest='S').encode('latin-1', 'replace')
        except Exception as e:
            st.error(f"Erro ao gerar PDF de estatísticas: {str(e)}")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, PDFModule.to_latin1("Erro ao gerar relatório de estatísticas"), ln=True)
            return pdf.output(dest='S').encode('latin-1', 'replace')

    @staticmethod
    def gerar_pdf_duas_tabelas(df1, titulo1, df2, titulo2, titulo_geral):
        """
        Gera PDF contendo duas tabelas sequenciais.
        Útil para 'Autores como assunto vs colaboradores'.
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            PDFModule._add_standard_header(pdf, titulo_geral)
            
            # Função auxiliar para desenhar tabela
            def desenhar_tabela(df, titulo_tabela):
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, PDFModule.to_latin1(titulo_tabela), ln=True)
                pdf.ln(2)
                
                cols = list(df.columns)
                n_cols = len(cols)
                available_width = 190
                col_width = available_width / n_cols if n_cols > 0 else available_width
                
                # Cabeçalho
                pdf.set_fill_color(47, 95, 152) 
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 10)
                for col in cols:
                    pdf.cell(col_width, 8, PDFModule.to_latin1(str(col)), border=1, align='C', fill=True)
                pdf.ln()
                
                # Corpo
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", '', 9)
                for i, (_, row) in enumerate(df.iterrows()):
                    # Zebra
                    if i % 2 == 0:
                        pdf.set_fill_color(255, 255, 255)
                    else:
                        pdf.set_fill_color(240, 240, 240)
                        
                    # Quebra de página
                    if pdf.get_y() > 265:
                        pdf.add_page()
                        # Re-imprimir cabeçalho
                        pdf.set_fill_color(47, 95, 152)
                        pdf.set_text_color(255, 255, 255)
                        pdf.set_font("Arial", 'B', 10)
                        for col in cols:
                            pdf.cell(col_width, 8, PDFModule.to_latin1(str(col)), border=1, align='C', fill=True)
                        pdf.ln()
                        pdf.set_text_color(0, 0, 0)
                        pdf.set_font("Arial", '', 9)
                        # Restaurar zebra
                        if i % 2 == 0:
                            pdf.set_fill_color(255, 255, 255)
                        else:
                            pdf.set_fill_color(240, 240, 240)

                    for col in cols:
                        val = row[col]
                        # Formatação numérica
                        if isinstance(val, float):
                            txt = f"{val:.2f}"
                        else:
                            txt = str(val)
                        txt = PDFModule.to_latin1(txt)
                        pdf.cell(col_width, 6, txt, border=1, align='C', fill=True)
                    pdf.ln()
            
            # Desenha Tabela 1
            desenhar_tabela(df1, titulo1)
            
            pdf.ln(10)
            
            # Verifica espaço para Tabela 2 (estimativa grosseira de cabeçalho + algumas linhas)
            if pdf.get_y() > 200:
                pdf.add_page()
                
            # Desenha Tabela 2
            desenhar_tabela(df2, titulo2)
            
            return pdf.output(dest='S').encode('latin-1', 'replace')
        except Exception as e:
            st.error(f"Erro ao gerar PDF de duas tabelas: {str(e)}")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, PDFModule.to_latin1("Erro ao gerar relatório"), ln=True)
            return pdf.output(dest='S').encode('latin-1', 'replace')

class UtilsModule:
    """Encapsula funções utilitárias."""
    @staticmethod
    def sanitizar_dataframe(df):
        colunas_lista = [
            'iconografias',
            'autores_colaboradores',
            'tradutores',
            'autores_citados',
            'palavras_chave',
            'nome_pessoal_como_assunto',
            'notas_pesquisa'
        ]
        if df.empty:
            return df
        for col in colunas_lista:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])
        return df

    @staticmethod
    def calculate_stats_with_percentage(series):
        if series.empty:
            return pd.DataFrame(columns=['Termo', 'Qtd', '%'])
        counts = series.value_counts().reset_index()
        counts.columns = ['Termo', 'Qtd']
        total = counts['Qtd'].sum()
        counts['%'] = (counts['Qtd'] / total * 100).map('{:.2f}%'.format)
        return counts

    @staticmethod
    def get_registro_by_id(dados, reg_id):
        for r in dados:
            if r.get('_id') == reg_id:
                return r
        return None

    @staticmethod
    def is_bilingue(registro):
        """
        Identifica publicação bilíngue procurando 'bilíngue/bilingue'
        tanto em nota de edição quanto no resumo (colchetes, aspas etc.).
        """
        nota = str(registro.get('nota_edicao', '') or '')
        resu = str(registro.get('resumo', '') or '')
        texto = (nota + " " + resu).lower()
        return ('bilíngue' in texto) or ('bilingue' in texto)

    @staticmethod
    def format_list_field(reg, field):
        raw = reg.get(field)
        itens = []
        if isinstance(raw, list):
            for v in raw:
                if v is None:
                    continue
                if isinstance(v, float) and pd.isna(v):
                    continue
                s = str(v).strip()
                if s:
                    itens.append(s)
        elif isinstance(raw, str):
            s = raw.strip()
            if s:
                itens.append(s)
        elif raw is not None and not (isinstance(raw, float) and pd.isna(raw)):
            s = str(raw).strip()
            if s:
                itens.append(s)
        if field in {'autores_colaboradores', 'autores_citados', 'tradutores', 'nome_pessoal_como_assunto'}:
            itens = [DataModule.format_nome_abnt(i) for i in itens]
        return ', '.join(itens) if itens else '—'

    @staticmethod
    def construir_tipo_textual(tipo_principal: str, subtipo: str | None) -> str:
        """Monta o rótulo completo, ignorando o placeholder 'Sem especificação'."""
        if subtipo and subtipo.strip() and subtipo != "Sem especificação":
            return f"{tipo_principal} - {subtipo.strip()}"
        return tipo_principal

    @staticmethod
    def parse_tipo_textual(valor: str) -> tuple[str, str | None]:
        """Separa o rótulo salvo em principal e subtipo para preencher o formulário.
        Aceita tanto ' - ' quanto ' | ' como separadores."""
        if not valor:
            return "", None
        # Aceitar tanto " - " quanto " | " como separadores
        if " | " in valor:
            partes = valor.split(" | ", 1)
            return partes[0].strip(), partes[1].strip()
        if " - " in valor:
            partes = valor.split(" - ", 1)
            return partes[0].strip(), partes[1].strip()
        return valor.strip(), "Sem especificação"

    @staticmethod
    def converter_excel(df):
        try:
            o = BytesIO()
            with pd.ExcelWriter(o, engine='xlsxwriter') as w:
                df_export = df.copy()
                for col in df_export.columns:
                    df_export[col] = df_export[col].apply(
                        lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x
                    )
                df_export.to_excel(w, index=False, sheet_name='Dados')
            return o.getvalue()
        except Exception as e:
            st.error(f"Erro ao gerar Excel: {str(e)}")
            o = BytesIO()
            pd.DataFrame({'Erro': ['Erro ao gerar planilha']}).to_excel(o, index=False)
            return o.getvalue()

# ==========================================
# 3. COMPONENTES REUTILIZÁVEIS
# ==========================================

class CatalogacaoForm:
    def __init__(self, dados, df):
        self.dados = dados
        self.df = df

    def render(self, rec=None, mode="NOVO REGISTRO"):
        # Inicializa session_state
        if 'loaded_json' not in st.session_state:
            st.session_state.loaded_json = None
        if 'clear_json_input' not in st.session_state:
            st.session_state.clear_json_input = False
        if 'form_clear_counter' not in st.session_state:
            st.session_state.form_clear_counter = 0

        # Carregamento Rápido via JSON/Excel - APENAS em NOVO REGISTRO
        if mode == "NOVO REGISTRO":
            with st.expander("📥 CARREGAMENTO RÁPIDO (JSON ou EXCEL)", expanded=False):
                tipo_import = st.radio("Formato:", ["JSON", "EXCEL"], horizontal=True, key="tipo_import")

                if tipo_import == "JSON":
                    c_txt, c_btn = st.columns([4, 1])
                    with c_txt:
                        json_value = "" if st.session_state.clear_json_input else None
                        j_txt = st.text_area("Cole o JSON:", height=100, key="json_input", value=json_value if json_value is not None else "")
                    with c_btn:
                        st.write(""); st.write("")
                        b_load = st.button("PROCESSAR JSON")

                    if st.session_state.clear_json_input:
                        st.session_state.clear_json_input = False

                    # Lógica de Carregamento JSON
                    if b_load and j_txt:
                        try:
                            l = json.loads(j_txt)
                            st.session_state.force_form_update = True
                            loaded_rec = l[0] if isinstance(l, list) else l
                            st.session_state.loaded_json = loaded_rec
                            st.success("✅ JSON carregado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao processar JSON: {str(e)}")
                            st.session_state.loaded_json = None
                else:
                    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'])
                    if uploaded_file and st.button("PROCESSAR EXCEL"):
                        try:
                            df_excel = pd.read_excel(uploaded_file)
                            if len(df_excel) > 0:
                                loaded_rec = df_excel.iloc[0].to_dict()
                                st.session_state.loaded_json = loaded_rec
                                st.success(f"✅ Excel carregado! {len(df_excel)} registro(s) encontrado(s). Carregando o primeiro.")
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao processar Excel: {str(e)}")

        # Prioridade: loaded_json > rec passado como parâmetro
        if st.session_state.loaded_json is not None:
            rec = st.session_state.loaded_json
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.info("📋 Dados carregados via importação.")
            with col_btn:
                if st.button("🗑️ Limpar dados", use_container_width=True):
                    st.session_state.loaded_json = None
                    st.session_state.selected_record = None
                    st.session_state.clear_json_input = True
                    st.session_state.current_editing_record_id = None  # ⚠️ CORREÇÃO: Resetar rastreamento
                    # Incrementar contador para forçar recriação do formulário
                    st.session_state.form_clear_counter += 1
                    # Limpar todos os campos do formulário E campos de busca
                    for key in list(st.session_state.keys()):
                        if key.startswith('form_') or key.startswith('busca_') or key.startswith('confirm_delete_') or key.startswith('icon_'):
                            del st.session_state[key]
                    st.rerun()
        elif rec and mode == "EDITAR EXISTENTE":
            # Se rec foi passado como parâmetro (da busca), mostrar info
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.info(f"📋 Editando: **{rec.get('titulo_artigo', '[sem título]')}**")
            with col_btn:
                if st.button("🧹 Limpar formulário", use_container_width=True):
                    st.session_state.selected_record = None
                    st.session_state.loaded_json = None
                    st.session_state.current_editing_record_id = None  # ⚠️ CORREÇÃO: Resetar rastreamento
                    # Incrementar contador para forçar recriação do formulário
                    st.session_state.form_clear_counter += 1
                    # Limpar todos os campos do formulário e campos de busca
                    for key in list(st.session_state.keys()):
                        if key.startswith('form_') or key.startswith('busca_') or key.startswith('icon_'):
                            del st.session_state[key]
                    st.rerun()

        # Lógica de Editar Existente (chamada externamente)
        # --- SELEÇÃO DE TIPO TEXTUAL (FORA DO FORMULÁRIO) ---
        st.markdown("---")
        st.markdown("#### TIPO TEXTUAL (Vocabulário Controlado)")

        tipo_atual = (rec or {}).get('vocabulario_controlado', '')
        tipo_principal_atual, subtipo_atual = UtilsModule.parse_tipo_textual(tipo_atual) if tipo_atual else (None, None)

        col_tipo1, col_tipo2 = st.columns(2)
        with col_tipo1:
            tipos_principais = sorted(DataModule.TIPOS_TEXTUAIS.keys())

            # Encontrar o índice correto
            idx_tipo = 0  # default
            if tipo_principal_atual and tipo_principal_atual in tipos_principais:
                idx_tipo = tipos_principais.index(tipo_principal_atual)

            # Gerar key único baseado no valor atual para forçar atualização do selectbox
            key_tipo = f"sel_tipo_principal_{tipo_atual}_{rec.get('_id', 'novo') if rec else 'novo'}"
            tipo_principal_selecionado = st.selectbox(
                "TIPO PRINCIPAL*",
                tipos_principais,
                index=idx_tipo,
                key=key_tipo,
                help="Selecione o tipo textual principal."
            )
        with col_tipo2:
            subtipos_disponiveis = DataModule.TIPOS_TEXTUAIS.get(tipo_principal_selecionado, ["Sem especificação"])
            idx_subtipo = subtipos_disponiveis.index(subtipo_atual) if subtipo_atual in subtipos_disponiveis else 0
            # Gerar key único baseado no valor atual para forçar atualização
            key_subtipo = f"sel_subtipo_{tipo_atual}_{rec.get('_id', 'novo') if rec else 'novo'}"
            subtipo_selecionado = st.selectbox(
                "SUBTIPO (Campo disciplinar)",
                subtipos_disponiveis,
                index=idx_subtipo,
                key=key_subtipo,
                help="Especifique o campo disciplinar."
            )

        tipo_textual_final = UtilsModule.construir_tipo_textual(tipo_principal_selecionado, subtipo_selecionado)
        st.info(f"Será registrado como: **{tipo_textual_final}**")

        # -----------------------------------------------------
        st.markdown("---")
        # --- INÍCIO DO FORMULÁRIO ---
        # ⚠️ CORREÇÃO DO BUG DE PERSISTÊNCIA:
        # Só atualizar session_state quando o registro REALMENTE mudar
        # Isso evita sobrescrever as edições do usuário a cada rerun

        # Identificar o registro atual
        rec_id_atual = rec.get('_id', 'novo') if rec else 'novo'

        # Verificar se é um registro diferente do anterior
        if 'current_editing_record_id' not in st.session_state:
            st.session_state.current_editing_record_id = None

        registro_mudou = (st.session_state.current_editing_record_id != rec_id_atual)

        # SÓ atualizar os campos quando:
        # 1. O registro mudou (carregou um diferente) OU
        # 2. Foi solicitado force_form_update (ao clicar em "Carregar Registro")
        should_update_form = registro_mudou or st.session_state.get('force_form_update', False)

        if should_update_form:
            # Atualizar o ID do registro atual
            st.session_state.current_editing_record_id = rec_id_atual

            # Resetar flag de force_form_update
            if 'force_form_update' in st.session_state:
                st.session_state.force_form_update = False

            # Função auxiliar para converter listas em texto
            def lt(x): return "\n".join(x) if isinstance(x, list) else str(x)

            if rec:
                # Carregar dados do registro
                st.session_state.form_n_rev = str(rec.get('n', ''))
                st.session_state.form_registro = str(rec.get('registro', ''))
                st.session_state.form_paginas = str(rec.get('paginas', ''))
                st.session_state.form_ordem = int(rec.get('ordem_exibicao', 0))
                st.session_state.form_i1 = rec.get('idioma_01', 'POR')
                st.session_state.form_i2 = rec.get('idioma_02', '')

                # Carregar Iconografias para lista dinâmica
                icon_data = rec.get('iconografias', [])
                rows = []
                for item in icon_data:
                    row_id = str(uuid.uuid4())
                    rows.append(row_id)
                    st.session_state[f"icon_tipo_{row_id}"] = item.get('tipo', DataModule.LISTA_ICONOGRAFIA[0])
                    st.session_state[f"icon_desc_{row_id}"] = item.get('descricao', '')
                st.session_state.iconografias_rows = rows
                st.session_state.form_titulo = rec.get('titulo_artigo', '')
                st.session_state.form_sub = rec.get('subtitulo_artigo', '')
                st.session_state.form_nota = rec.get('nota_edicao', '')
                st.session_state.form_autores = lt(rec.get('autores_colaboradores', []))
                st.session_state.form_entidade = lt(rec.get('entidade_coletiva', []))
                st.session_state.form_tradutores = lt(rec.get('tradutores', []))
                st.session_state.form_citados = lt(rec.get('autores_citados', []))
                st.session_state.form_kw = lt(rec.get('palavras_chave', []))
                st.session_state.form_pessoal = lt(rec.get('nome_pessoal_como_assunto', []))
                st.session_state.form_resumo = rec.get('resumo', '')
            else:
                # Formulário vazio (novo registro sem dados)
                st.session_state.form_n_rev = ''
                st.session_state.form_registro = ''
                st.session_state.form_paginas = ''
                st.session_state.form_ordem = 0
                st.session_state.form_i1 = 'POR'
                st.session_state.form_i2 = ''
                st.session_state.form_titulo = ''
                st.session_state.form_sub = ''
                st.session_state.form_nota = ''
                st.session_state.form_autores = ''
                st.session_state.form_entidade = ''
                st.session_state.form_tradutores = ''
                st.session_state.form_citados = ''
                st.session_state.form_kw = ''
                st.session_state.form_pessoal = ''
                st.session_state.form_resumo = ''

        # Usar chave dinâmica para forçar recriação do formulário quando registro mudar OU quando limpar
        rec_id = rec.get('_id', 'novo') if rec else 'novo'
        # form_key = f"form_{rec_id}_v{st.session_state.form_clear_counter}"
        
        # REMOVIDO st.form PARA PERMITIR BOTÕES DINÂMICOS
        # with st.form(form_key):
        if True: # Manter indentação visual ou remover indentação abaixo (vou remover indentação)
            c_form1, c_form2, c_form3, c_form4 = st.columns(4)
            n_rev = c_form1.text_input("Nº REVISTA*", key="form_n_rev")
            reg_txt = c_form2.text_input("REGISTRO*", key="form_registro")
            pag = c_form3.text_input("PÁGINAS", key="form_paginas")
            # Verificação de Duplicidade
            if n_rev and reg_txt:
                duplicado = False
                for r in self.dados:
                    if mode == "EDITAR EXISTENTE" and (rec or {}).get('_id') == r.get('_id'): continue
                    if str(r.get('n')) == str(n_rev) and str(r.get('registro')) == str(reg_txt):
                        duplicado = True
                        break
                if duplicado:
                    st.warning(f"⚠️ ATENÇÃO: Já existe o registro '{reg_txt}' na Revista {n_rev}!", icon="🚨")
            ordem = c_form4.number_input("ORDEM", key="form_ordem", min_value=0, step=1, format="%d")

            c5, c6, c7 = st.columns(3)
            langs = ["POR", "ING", "ESP", "FRA", "ITA", "ALE", "RUS", "CAT", "GRE", "JAP"]
            # Idiomas usam session_state para valores padrão
            i1 = c5.selectbox("IDIOMA 1", langs, key="form_i1")
            i2 = c6.selectbox("IDIOMA 2", [""] + langs, key="form_i2")
            st.markdown("---")

            regra_help = "Se sem título: insira o primeiro verso entre aspas..."
            tit = st.text_input("TÍTULO*", help=regra_help, key="form_titulo")
            sub = st.text_input("SUBTÍTULO", key="form_sub")
            nota_ed = st.text_input("NOTA DE EDIÇÃO", key="form_nota")

            st.markdown("---")
            st.markdown("#### RESPONSABILIDADE AUTORAL")
            c8, c9, c10 = st.columns(3)
            aut = c8.text_area("COLABORADORES", key="form_autores")
            entidade = c9.text_area("ENTIDADE COLETIVA", key="form_entidade", help="Responsabilidade institucional quando não há autor individual")
            trad = c10.text_area("TRADUTORES", key="form_tradutores")

            st.markdown("---")
            st.markdown("#### ASSUNTOS")
            c10, c11 = st.columns(2)
            cit = c10.text_area("AUTORES CITADOS", key="form_citados")
            kw = c11.text_area("PALAVRAS-CHAVE", key="form_kw")
            nome_pessoal = st.text_area("NOME PESSOAL COMO ASSUNTO", key="form_pessoal")

            st.markdown("---")
            st.markdown("#### RESUMO ANALÍTICO")
            tipo_base = tipo_principal_selecionado.upper().replace(" ", "")
            requer_resumo = tipo_base not in TIPOS_SEM_RESUMO
            label_resumo = "RESUMO" + (" (OBRIGATÓRIO)" if requer_resumo else " (OPCIONAL)")
            resumo = st.text_area(label_resumo, height=200, key="form_resumo")

            st.markdown("---")
            st.markdown("#### ICONOGRAFIA")

            # --- ICONOGRAFIA (REFATORADO) ---
            if 'iconografias_rows' not in st.session_state:
                st.session_state.iconografias_rows = []

            # Botão de Adicionar
            col_add_icon, _ = st.columns([3, 4])
            if col_add_icon.button("➕ ADICIONAR ICONOGRAFIA"):
                new_row_id = str(uuid.uuid4())
                st.session_state.iconografias_rows.append(new_row_id)
                # Valores padrão
                st.session_state[f"icon_tipo_{new_row_id}"] = DataModule.LISTA_ICONOGRAFIA[0]
                st.session_state[f"icon_desc_{new_row_id}"] = ""
                st.rerun()

            # Renderizar linhas
            rows_to_remove = []
            for idx, row_id in enumerate(st.session_state.iconografias_rows):
                st.markdown(f"**Iconografia {idx+1}**")
                c_tipo, c_desc, c_del = st.columns([2, 5, 0.5])
                
                with c_tipo:
                    st.selectbox(
                        "Tipo",
                        DataModule.LISTA_ICONOGRAFIA,
                        key=f"icon_tipo_{row_id}",
                        label_visibility="collapsed"
                    )
                with c_desc:
                    st.text_input(
                        "Descrição",
                        key=f"icon_desc_{row_id}",
                        placeholder="Descrição da iconografia...",
                        label_visibility="collapsed"
                    )
                with c_del:
                    if st.button("🗑️", key=f"del_icon_{row_id}", help="Remover iconografia"):
                        rows_to_remove.append(row_id)

            # Processar remoções
            if rows_to_remove:
                for rid in rows_to_remove:
                    if rid in st.session_state.iconografias_rows:
                        st.session_state.iconografias_rows.remove(rid)
                    # Limpar chaves do session_state
                    if f"icon_tipo_{rid}" in st.session_state: del st.session_state[f"icon_tipo_{rid}"]
                    if f"icon_desc_{rid}" in st.session_state: del st.session_state[f"icon_desc_{rid}"]
                st.rerun()

            # Informação visual
            if not st.session_state.iconografias_rows:
                st.info("ℹ️ Nenhuma iconografia cadastrada.")
                st.caption(f"💡 Dica: Aumente o número acima para adicionar mais iconografias, diminua para remover.")

            st.markdown("---")
            # BOTÃO SALVAR (AGORA FORA DO FORM)
            submit_btn = st.button("💾 SALVAR", type="primary")

        # LÓGICA DE SALVAMENTO (FORA DO FORM, MAS GATILHADA PELO BOTÃO)
        if submit_btn:
            if not n_rev or not reg_txt:
                st.error("❌ Campos obrigatórios: Nº REVISTA e REGISTRO!")
                st.stop()
            if requer_resumo and not resumo.strip():
                st.error(f"❌ O tipo textual '{tipo_textual_final}' exige RESUMO ANALÍTICO!")
                st.stop()

            # Construir lista de iconografias a partir do session_state
            icon_list = []
            if 'iconografias_rows' in st.session_state:
                for row_id in st.session_state.iconografias_rows:
                    t = st.session_state.get(f"icon_tipo_{row_id}")
                    d = st.session_state.get(f"icon_desc_{row_id}", "").strip()
                    if t and d:
                        icon_list.append({"tipo": t, "descricao": d})

            new = {
                "n": n_rev,
                "registro": reg_txt,
                "ordem_exibicao": ordem,
                "idioma_01": i1,
                "idioma_02": i2 if i2 else "",
                "vocabulario_controlado": tipo_textual_final,
                "titulo_artigo": tit,
                "subtitulo_artigo": sub,
                "paginas": pag,
                "resumo": resumo,
                "nota_edicao": nota_ed,
                "autores_colaboradores": DataModule.normalizar_lista_autores(aut),
                "entidade_coletiva": DataModule.normalizar_lista_autores(entidade),
                "tradutores": DataModule.normalizar_lista_autores(trad),
                "autores_citados": DataModule.normalizar_lista_autores(cit),
                "palavras_chave": DataModule.normalizar_texto(kw.replace(',', '\n').split('\n')),
                "nome_pessoal_como_assunto": DataModule.normalizar_lista_autores(nome_pessoal),
                "iconografias": icon_list,
                "_timestamp": datetime.now().isoformat()
            }
            # Preservar notas de pesquisa do registro original, se existir
            if 'notas_pesquisa' in (rec or {}):
                new['notas_pesquisa'] = (rec or {}).get('notas_pesquisa', [])

            # LÓGICA APRIMORADA: Buscar registro existente por Revista + Registro
            # Isso evita duplicatas mesmo quando não há _id no rec
            registro_existente = None
            indice_existente = None

            for i, d in enumerate(self.dados):
                if str(d.get('n')) == str(n_rev) and str(d.get('registro')) == str(reg_txt):
                    # Encontrou registro com mesma Revista + Registro
                    registro_existente = d
                    indice_existente = i
                    break

            if mode == "EDITAR EXISTENTE":
                # Modo EDITAR: Verificar se há registro para substituir
                if registro_existente:
                    # Substituir o registro existente, preservando o _id original
                    new['_id'] = registro_existente.get('_id', str(int(datetime.now().timestamp() * 1000)))
                    # Preservar notas de pesquisa do registro original
                    if 'notas_pesquisa' in registro_existente:
                        new['notas_pesquisa'] = registro_existente.get('notas_pesquisa', [])
                    self.dados[indice_existente] = new
                    st.info(f"ℹ️ Registro existente (ID: {new['_id']}) foi ATUALIZADO.")
                elif '_id' in (rec or {}):
                    # Tem _id mas não encontrou por revista+registro (usuário pode ter mudado esses campos)
                    # Buscar pelo _id original
                    new['_id'] = (rec or {})['_id']
                    for i, d in enumerate(self.dados):
                        if d.get('_id') == new['_id']:
                            self.dados[i] = new
                            st.info(f"ℹ️ Registro (ID: {new['_id']}) foi ATUALIZADO.")
                            break
                else:
                    # Está em modo EDITAR mas não encontrou registro existente - criar novo
                    new['_id'] = str(int(datetime.now().timestamp() * 1000))
                    new.setdefault('notas_pesquisa', [])
                    self.dados.append(new)
                    st.warning("⚠️ Não foi encontrado registro existente para editar. Criado NOVO registro.")
            else:
                # Modo NOVO REGISTRO
                if registro_existente:
                    # ATENÇÃO: Já existe um registro com essa Revista + Registro!
                    st.error(f"❌ ERRO: Já existe um registro com Revista {n_rev} e Registro {reg_txt} (ID: {registro_existente.get('_id')})")
                    st.error("💡 Use o modo 'EDITAR EXISTENTE' para modificar este registro ou altere os campos Revista/Registro.")
                    st.stop()
                else:
                    # Criar novo registro normalmente
                    new['_id'] = str(int(datetime.now().timestamp() * 1000))
                    new.setdefault('notas_pesquisa', [])
                    self.dados.append(new)

            if PersistenceModule.save_data(self.dados):
                st.success("✅ Registro salvo com sucesso!")
                st.balloons()

                # Limpar automaticamente o formulário após salvar
                st.session_state.loaded_json = None
                st.session_state.selected_record = None
                st.session_state.current_editing_record_id = None  # ⚠️ CORREÇÃO: Resetar rastreamento
                # Incrementar contador para forçar recriação do formulário
                st.session_state.form_clear_counter += 1

                # Limpar todos os campos do formulário
                for key in list(st.session_state.keys()):
                    if key.startswith('form_') or key.startswith('busca_') or key.startswith('confirm_delete_') or key.startswith('icon_'):
                        del st.session_state[key]

                # Recarregar a página para mostrar formulário limpo
                st.rerun()


class FichasNotasView:
    def __init__(self, df, dados):
        self.df = df
        self.dados = dados

    def render(self):
        st.title("📇 FICHAS & NOTAS NELIC")
        if self.df.empty:
            st.warning("Base de dados vazia. Cadastre registros na aba CATALOGAÇÃO.")
            return

        st.markdown("### 🔍 Navegação por Revista")
        # Garante ordenação correta das revistas
        revistas_disponiveis = sorted(
            self.df['n'].astype(str).unique(),
            key=lambda x: ORDEM_SIBILA.index(x) if x in ORDEM_SIBILA else 999
        )
        revista_selecionada = st.selectbox(
            "Selecione a revista:",
            ["Todas as revistas"] + revistas_disponiveis,
            help="Filtre os registros por número da revista para facilitar a navegação"
        )

        if revista_selecionada == "Todas as revistas":
            df_filtrado = self.df
        else:
            df_filtrado = self.df[self.df['n'].astype(str) == revista_selecionada]

        st.markdown("---")
        opcoes = [
            f"{r.get('n','?')} | Reg: {r.get('registro','?')} | {r.get('titulo_artigo','[sem título]')}"
            for _, r in df_filtrado.iterrows()
        ]
        if not opcoes:
            st.warning(f"⚠️ Nenhum registro encontrado para a revista {revista_selecionada}")
            return

        escolha = st.selectbox("Selecione o registro específico:", opcoes)
        idx = opcoes.index(escolha)
        reg_sel = df_filtrado.iloc[idx].to_dict()
        reg_id = reg_sel.get('_id')

        c_esq, c_dir = st.columns([2, 1])
        with c_esq:
            st.markdown(
                f"""
                <div class="nelic-card">
                    <div class="nelic-card-header">FICHA NELIC – REGISTRO {reg_sel.get('registro','')}</div>
                    <div class="nelic-card-subtitle">
                        n. {reg_sel.get('n','?')} · Tipo {reg_sel.get('vocabulario_controlado','')} · pp. {reg_sel.get('paginas','')}
                    </div>
                    <div>
                        <strong>Título:</strong> {reg_sel.get('titulo_artigo','[sem título]')}<br>
                        <strong>Subtítulo:</strong> {reg_sel.get('subtitulo_artigo','')}<br>
                        <strong>Autores:</strong> {UtilsModule.format_list_field(reg_sel, 'autores_colaboradores')}<br>
                        <strong>Tradutores:</strong> {UtilsModule.format_list_field(reg_sel, 'tradutores')}<br>
                        <strong>Entidade Coletiva:</strong> {UtilsModule.format_list_field(reg_sel, 'entidade_coletiva')}
                    </div>
                    <div style="margin-top:0.4rem;">
                        <span class="nelic-tag">Idioma 1: {reg_sel.get('idioma_01','')}</span>
                        <span class="nelic-tag nelic-tag-muted">Idioma 2: {reg_sel.get('idioma_02','')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("#### Conteúdo e Assuntos")
            with st.expander("📌 Conteúdo", expanded=True):
                st.markdown(f"**Nota de edição:** {reg_sel.get('nota_edicao','—')}")
                st.markdown("**Resumo:**")
                st.write(reg_sel.get('resumo', '—'))

            with st.expander("🎯 Assuntos e autores citados", expanded=False):
                st.markdown(f"**Palavras-chave:** {UtilsModule.format_list_field(reg_sel, 'palavras_chave')}")
                st.markdown(f"**Autores citados:** {UtilsModule.format_list_field(reg_sel, 'autores_citados')}")
                st.markdown(f"**Nomes pessoais como assunto:** {UtilsModule.format_list_field(reg_sel, 'nome_pessoal_como_assunto')}")

            with st.expander("🖼️ Iconografia", expanded=False):
                icons = reg_sel.get('iconografias', [])
                if icons:
                    for ic in icons:
                        st.markdown(f"- **{ic.get('tipo','')}** · {ic.get('descricao','')}")
                else:
                    st.markdown("Nenhuma iconografia registrada.")

        with c_dir:
            st.markdown("#### Exportar Ficha")
            pdf_ficha = PDFModule.gerar_pdf_ficha(reg_sel)
            st.download_button(
                "📄 BAIXAR FICHA EM PDF",
                pdf_ficha,
                f"ficha_sibila_{reg_sel.get('registro','')}.pdf",
                "application/pdf",
                width='stretch'
            )

            st.markdown("---")
            st.markdown("#### Notas de Pesquisa")
            # Carregamos o diário aqui para garantir atualização
            diario = PersistenceModule.load_diario()
            notas = reg_sel.get('notas_pesquisa', []) or []
            with st.form("form_nota_registro"):
                titulo_nota = st.text_input("Título da nota")
                texto_nota = st.text_area("Texto da nota", height=120)
                tags_nota = st.text_input("Tags (separadas por vírgula)")
                if st.form_submit_button("➕ Adicionar nota a este registro"):
                    if texto_nota.strip():
                        nova_nota = {
                            "id": str(int(datetime.now().timestamp() * 1000)),
                            "data": datetime.now().isoformat(),
                            "titulo": titulo_nota.strip() or "[sem título]",
                            "texto": texto_nota.strip(),
                            "tags": [t.strip() for t in tags_nota.split(',') if t.strip()],
                            "registro_id": reg_id
                        }
                        # Precisamos buscar o registro na lista original 'dados' para salvar
                        reg_real = UtilsModule.get_registro_by_id(self.dados, reg_id)
                        if reg_real is not None:
                            reg_real.setdefault('notas_pesquisa', [])
                            reg_real['notas_pesquisa'].append(nova_nota)
                            if PersistenceModule.save_data(self.dados):
                                st.success("Nota adicionada ao registro.")
                                st.rerun() # Recarrega para mostrar a nota nova
                        else:
                            st.error("Erro ao vincular nota.")
                    else:
                        st.warning("O texto da nota não pode estar vazio.")

            if notas:
                st.markdown("##### Notas já cadastradas")
                for n in sorted(notas, key=lambda x: x.get('data', ''), reverse=True):
                    dt = n.get('data', '')[:16].replace("T", " ")
                    st.markdown(
                        f"""
                        <div class="nelic-card">
                            <div class="nelic-card-header">{n.get('titulo','[sem título]')}</div>
                            <div class="nelic-card-subtitle">Data: {dt}</div>
                            <div class="nelic-muted">{n.get('texto','')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    tags = n.get('tags', [])
                    if tags:
                        st.markdown(" ".join([f"<span class='nelic-tag nelic-tag-muted'>{t}</span>" for t in tags]), unsafe_allow_html=True)
            else:
                st.info("Nenhuma nota vinculada.")

# ==========================================
# 4. FUNÇÕES DE RELATÓRIOS
# ==========================================

def relatorio_mapa_colaboracao(df):
    st.markdown("#### Volume de itens por revista")
    def itens_por_revista(df_local):
        rows = []
        for rev, sub in df_local.groupby('n'):
            rows.append({"n.": str(rev), "Quantidade de itens": len(sub)})
        return pd.DataFrame(rows)
    
    df_rel = itens_por_revista(df)
    # Garante ordenação correta no gráfico
    if 'n.' in df_rel.columns:
        df_rel['n.'] = pd.Categorical(df_rel['n.'], categories=ORDEM_SIBILA, ordered=True)
        df_rel = df_rel.sort_values('n.')
    
    df_rel.index = df_rel.index + 1
    st.dataframe(df_rel, width='stretch')
    fig = px.bar(df_rel, x="n.", y="Quantidade de itens", text="Quantidade de itens")
    fig.update_layout(height=380, title="Volume de itens por número da revista")
    fig.update_xaxes(type='category', tickmode='linear')
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    
    excel_rel = UtilsModule.converter_excel(df_rel.rename(columns={'n.': 'Nº Revista'}))
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_mapa_colaboracao_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_analitico(df, len(df), "Volume de itens por revista")
    col2.download_button(
        "📄 PDF (lista completa)",
        pdf_rel,
        f"rel_mapa_colaboracao_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_bilinguismo(df):
    st.markdown("#### Índice de publicações bilíngues por número da revista")
    df_local = df.copy()
    df_local['bilingue'] = df_local.apply(UtilsModule.is_bilingue, axis=1)
    resumo = (
        df_local.groupby('n')['bilingue']
        .agg(total='count', bil='sum')
        .reset_index()
    )
    resumo['% bilíngue'] = resumo.apply(
        lambda r: (r['bil'] / r['total'] * 100) if r['total'] > 0 else 0, axis=1
    )
    resumo['n'] = resumo['n'].astype(str)
    
    # Garante ordenação correta no gráfico
    if 'n' in resumo.columns:
        resumo['n'] = pd.Categorical(resumo['n'], categories=ORDEM_SIBILA, ordered=True)
        resumo = resumo.sort_values('n')

    resumo.index = resumo.index + 1
    st.dataframe(resumo, width='stretch')
    fig = px.bar(
        resumo,
        x='n',
        y='% bilíngue',
        text=resumo['% bilíngue'].map(lambda x: f"{x:.1f}%")
    )
    fig.update_layout(
        height=380,
        title="% de registros bilíngues (nota ou resumo) por revista",
        xaxis_title="n.",
        yaxis_title="% bilíngue"
    )
    fig.update_xaxes(type='category', tickmode='linear')
    st.plotly_chart(fig, width='stretch')
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    excel_rel = UtilsModule.converter_excel(resumo.rename(columns={'n': 'Nº Revista', 'total': 'Total', 'bil': 'Bilíngues'}))
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_bilinguismo_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_tabela_estatistica(resumo, "Índice de publicações bilíngues")
    col2.download_button(
        "📄 PDF",
        pdf_rel,
        f"rel_bilinguismo_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_iconografia(df):
    st.markdown("#### Iconografia por número da revista")
    df_local = df.copy()
    
    # Nova Lógica: Contar número de itens na lista de iconografias
    df_local['qtd_imagens'] = df_local['iconografias'].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
    
    resumo = (
        df_local.groupby('n')['qtd_imagens']
        .agg(total_imagens='sum')
        .reset_index()
    )
    
    resumo['n'] = resumo['n'].astype(str)

    # Garante ordenação correta no gráfico
    if 'n' in resumo.columns:
        resumo['n'] = pd.Categorical(resumo['n'], categories=ORDEM_SIBILA, ordered=True)
        resumo = resumo.sort_values('n')

    resumo.index = resumo.index + 1
    
    # Renomear coluna para exibição
    resumo_display = resumo.rename(columns={'total_imagens': 'Total de Imagens'})
    
    st.dataframe(resumo_display, width='stretch')
    
    fig = px.bar(
        resumo,
        x='n',
        y='total_imagens',
        text=resumo['total_imagens'].map(lambda x: f"{x}")
    )
    fig.update_layout(
        height=380,
        title="Total de Imagens por Revista",
        xaxis_title="n.",
        yaxis_title="Quantidade de Imagens"
    )
    fig.update_xaxes(type='category', tickmode='linear')
    st.plotly_chart(fig, width='stretch')
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    excel_rel = UtilsModule.converter_excel(resumo.rename(columns={'n': 'Nº Revista', 'total_imagens': 'Total de Imagens'}))
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_iconografia_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_tabela_estatistica(resumo_display, "Iconografia por revista")
    col2.download_button(
        "📄 PDF",
        pdf_rel,
        f"rel_iconografia_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_autores_assunto_colab(df):
    st.markdown("#### Autores como assunto vs colaboradores")
    s_colab = DataModule.get_normalized_series(df, 'autores_colaboradores')
    s_ass = DataModule.get_normalized_series(df, 'nome_pessoal_como_assunto')
    df_colab = UtilsModule.calculate_stats_with_percentage(s_colab)
    df_ass = UtilsModule.calculate_stats_with_percentage(s_ass)
    
    # Ajuste visual do índice para começar em 1
    df_colab.index = df_colab.index + 1
    df_ass.index = df_ass.index + 1
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Colaboradores (top 20)**")
        st.dataframe(df_colab.head(20), width='stretch')
    with c2:
        st.markdown("**Nomes pessoais como assunto (top 20)**")
        st.dataframe(df_ass.head(20), width='stretch')
    intersect = set(df_colab['Termo']).intersection(set(df_ass['Termo']))
    st.markdown("---")
    st.markdown("##### Interseções (quem é autor e tema)")
    if intersect:
        st.write(", ".join(sorted(list(intersect))))
    else:
        st.write("Nenhuma interseção encontrada.")
        
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    
    # Exportar Tabelas Completas (Top 20 apenas para visualização, mas exportação pode ser completa ou top 20. 
    # O usuário pediu "Autores Colaboradores (Top 20)" e "Nomes Pessoais como Assunto (Top 20)" no PDF.
    # Vamos exportar o Top 20 no PDF conforme solicitado.
    
    pdf_duplo = PDFModule.gerar_pdf_duas_tabelas(
        df_colab.head(20), "Autores Colaboradores (Top 20)",
        df_ass.head(20), "Nomes Pessoais como Assunto (Top 20)",
        "Autores como Assunto vs Colaboradores"
    )
    
    col1.download_button(
        "📄 PDF (Top 20 de ambos)",
        pdf_duplo,
        f"rel_autores_assunto_colab_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_tipos_textuais(df):
    st.markdown("#### Análise por tipos textuais")
    df_local = df.copy()
    df_local['tipo_base'] = df_local['vocabulario_controlado'].astype(str).apply(
        lambda x: 'Manifesto' if 'manifesto' in x.lower() else x.split(' - ')[0]
    )
    counts = df_local['tipo_base'].value_counts().reset_index()
    counts.columns = ['Tipo textual', 'Num. Absoluto']
    total = counts['Num. Absoluto'].sum()
    counts['Percentual'] = (counts['Num. Absoluto'] / total * 100).map(lambda x: f"{x:.2f}%")
    counts.index = counts.index + 1
    st.dataframe(counts, width='stretch')
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    excel_rel = UtilsModule.converter_excel(counts)
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_tipos_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_tabela_estatistica(counts, "Tipos textuais")
    col2.download_button(
        "📄 PDF",
        pdf_rel,
        f"rel_tipos_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_manifesto(df):
    st.markdown("#### Textos relacionados a 'Manifesto' (tipo textual, palavra-chave ou título)")
    df_local = df.copy()
    def verificar_manifesto(registro):
        locais = []
        tipo = str(registro.get('vocabulario_controlado', '')).lower()
        if 'manifesto' in tipo:
            locais.append('Tipo textual')
        kw = registro.get('palavras_chave', [])
        if isinstance(kw, list):
            for palavra in kw:
                if palavra and 'manifesto' in str(palavra).lower():
                    locais.append('Palavra-chave')
                    break
        titulo = str(registro.get('titulo_artigo', '')).lower()
        if 'manifesto' in titulo:
            locais.append('Título')
        resumo = str(registro.get('resumo', '')).lower()
        if 'manifesto' in resumo:
            locais.append('Resumo')
        return locais

    df_local['locais_manifesto'] = df_local.apply(verificar_manifesto, axis=1)
    df_man = df_local[df_local['locais_manifesto'].apply(lambda x: len(x) > 0)].copy()
    st.write(f"Registros encontrados: {len(df_man)} de {len(df)} (total da base)")
    if not df_man.empty:
        df_man['onde_encontrado'] = df_man['locais_manifesto'].apply(lambda x: ', '.join(x))
        
        # Preparar dataframe para exibição com índice começando em 1
        df_display = df_man[['n', 'registro', 'vocabulario_controlado', 'titulo_artigo', 'onde_encontrado']].copy()
        df_display.reset_index(drop=True, inplace=True)
        df_display.index = df_display.index + 1
        
        st.dataframe(
            df_display,
            column_config={
                'n': 'Revista',
                'registro': 'Registro',
                'vocabulario_controlado': 'Tipo',
                'titulo_artigo': 'Título',
                'onde_encontrado': 'Encontrado em'
            },
            width='stretch'
        )
        st.markdown("##### Exportar")
        col1, col2 = st.columns(2)
        df_export = df_man[['n', 'registro', 'vocabulario_controlado', 'titulo_artigo', 'palavras_chave', 'onde_encontrado']].copy()
        excel_rel = UtilsModule.converter_excel(df_export.rename(columns={
            'n': 'Nº Revista', 
            'registro': 'Registro',
            'vocabulario_controlado': 'Tipo Textual',
            'titulo_artigo': 'Título',
            'palavras_chave': 'Palavras-chave',
            'onde_encontrado': 'Encontrado em'
        }))
        col1.download_button(
            "📊 EXCEL",
            excel_rel,
            f"rel_manifesto_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )
        
        pdf_rel = PDFModule.gerar_pdf_analitico(df_man, len(df), "Manifesto")
        col2.download_button(
            "📄 PDF",
            pdf_rel,
            f"rel_manifesto_{datetime.now().strftime('%Y%m%d')}.pdf",
            "application/pdf",
            width='stretch'
        )
    else:
        st.info("Nenhum registro relacionado a 'Manifesto' foi encontrado na base.")

def relatorio_sibila(df):
    st.markdown("#### Textos relacionados a 'Sibila' (tipo textual, palavra-chave ou título)")
    df_local = df.copy()
    def verificar_sibila(registro):
        locais = []
        tipo = str(registro.get('vocabulario_controlado', '')).lower()
        if 'sibil' in tipo:
            locais.append('Tipo textual')
        kw = registro.get('palavras_chave', [])
        if isinstance(kw, list):
            for palavra in kw:
                if palavra and 'sibil' in str(palavra).lower():
                    locais.append('Palavra-chave')
                    break
        titulo = str(registro.get('titulo_artigo', '')).lower()
        if 'sibil' in titulo:
            locais.append('Título')
        resumo = str(registro.get('resumo', '')).lower()
        if 'sibil' in resumo:
            locais.append('Resumo')
        return locais

    df_local['locais_sibila'] = df_local.apply(verificar_sibila, axis=1)
    df_sib = df_local[df_local['locais_sibila'].apply(lambda x: len(x) > 0)].copy()
    st.write(f"Registros encontrados: {len(df_sib)} de {len(df)} (total da base)")
    if not df_sib.empty:
        df_sib['onde_encontrado'] = df_sib['locais_sibila'].apply(lambda x: ', '.join(x))
        
        # Preparar dataframe para exibição com índice começando em 1
        df_display = df_sib[['n', 'registro', 'vocabulario_controlado', 'titulo_artigo', 'onde_encontrado']].copy()
        df_display.reset_index(drop=True, inplace=True)
        df_display.index = df_display.index + 1
        
        st.dataframe(
            df_display,
            column_config={
                'n': 'Revista',
                'registro': 'Registro',
                'vocabulario_controlado': 'Tipo',
                'titulo_artigo': 'Título',
                'onde_encontrado': 'Encontrado em'
            },
            width='stretch'
        )
        st.markdown("##### Exportar")
        col1, col2 = st.columns(2)
        df_export = df_sib[['n', 'registro', 'vocabulario_controlado', 'titulo_artigo', 'palavras_chave', 'onde_encontrado']].copy()
        excel_rel = UtilsModule.converter_excel(df_export.rename(columns={
            'n': 'Nº Revista', 
            'registro': 'Registro',
            'vocabulario_controlado': 'Tipo Textual',
            'titulo_artigo': 'Título',
            'palavras_chave': 'Palavras-chave',
            'onde_encontrado': 'Encontrado em'
        }))
        col1.download_button(
            "📊 EXCEL",
            excel_rel,
            f"rel_sibila_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch'
        )
        
        pdf_rel = PDFModule.gerar_pdf_analitico(df_sib, len(df), "Sibila")
        col2.download_button(
            "📄 PDF",
            pdf_rel,
            f"rel_sibila_{datetime.now().strftime('%Y%m%d')}.pdf",
            "application/pdf",
            width='stretch'
        )
    else:
        st.info("Nenhum registro relacionado a 'Sibila' foi encontrado na base.")

def relatorio_palavras_chave(df):
    st.markdown("#### Estatísticas de palavras-chave (vocabulário controlado)")
    s = DataModule.get_normalized_series(df, 'palavras_chave')
    counts = UtilsModule.calculate_stats_with_percentage(s)
    df_stats = counts.rename(
        columns={'Termo': 'Palavra-chave', 'Qtd': 'Num. Absoluto', '%': 'Percentual'}
    )
    df_stats.index = df_stats.index + 1
    st.dataframe(df_stats, width='stretch')
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    excel_rel = UtilsModule.converter_excel(df_stats)
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_palavras_chave_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_tabela_estatistica(df_stats, "Palavras-chave")
    col2.download_button(
        "📄 PDF",
        pdf_rel,
        f"rel_palavras_chave_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

def relatorio_densidade_paginas(df):
    st.markdown("#### Densidade de Imagens por Páginas")
    
    def obter_ultima_pagina_revista(df_revista):
        # Encontra o maior número de página citado em toda a edição
        max_pag = 0
        for pag in df_revista['paginas']:
            try:
                # Extrai todos os números e pega o último (ex: "10-25" -> 25)
                nums = [int(n) for n in re.findall(r'\d+', str(pag))]
                if nums:
                    local_max = max(nums)
                    if local_max > max_pag:
                        max_pag = local_max
            except:
                continue
        return max_pag if max_pag > 0 else 1 # Evita divisão por zero

    def contar_imagens(row):
        # Conta o número de itens na lista de iconografias
        icons = row.get('iconografias', [])
        if isinstance(icons, list):
            return len(icons)
        return 0

    rows = []
    # Agrupa por número da revista
    for rev, sub in df.groupby('n'):
        # Denominator: Última página física da revista
        total_paginas_revista = obter_ultima_pagina_revista(sub)
        
        # Numerator: Soma da quantidade de itens de iconografia
        soma_imagens = 0
        for _, row in sub.iterrows():
            soma_imagens += contar_imagens(row)
            
        # Densidade: Imagens por página (ou % de ocupação conforme solicitado, mas a lógica agora é Imagens / Páginas)
        # O usuário pediu: "Numerador (Ocupação): Soma itens iconografia", "Denominador: Última página"
        # O título original era "% da revista ocupada por ilustrações".
        # Se tivermos 50 imagens em 100 páginas, a densidade é 0.5 imagens/página.
        # Se multiplicarmos por 100, seria "50%".
        # Vou manter a lógica de porcentagem/densidade mas com os novos valores.
        
        pct = (soma_imagens / total_paginas_revista * 100)
        
        rows.append({
            "n.": str(rev),
            "Total de Imagens": soma_imagens,
            "Total Páginas Revista": total_paginas_revista,
            "Densidade (Img/Pág %)": pct
        })
        
    df_rel = pd.DataFrame(rows)
    # Garante ordenação correta no gráfico
    if 'n.' in df_rel.columns:
        df_rel['n.'] = pd.Categorical(df_rel['n.'], categories=ORDEM_SIBILA, ordered=True)
        df_rel = df_rel.sort_values('n.')

    df_rel.index = df_rel.index + 1
    
    st.dataframe(df_rel, width='stretch')
    
    # Gráfico
    fig = px.bar(
        df_rel, 
        x="n.", 
        y="Densidade (Img/Pág %)", 
        text=df_rel["Densidade (Img/Pág %)"].map(lambda x: f"{x:.1f}")
    )
    fig.update_layout(
        height=380, 
        title="Densidade de Imagens (Volume de Imagens / Total de Páginas)",
        xaxis_title="n.",
        yaxis_title="Densidade"
    )
    fig.update_xaxes(type='category', tickmode='linear')
    st.plotly_chart(fig, width='stretch')
    
    # Exportar
    st.markdown("##### Exportar")
    col1, col2 = st.columns(2)
    
    excel_rel = UtilsModule.converter_excel(df_rel.rename(columns={'n.': 'Nº Revista'}))
    col1.download_button(
        "📊 EXCEL",
        excel_rel,
        f"rel_densidade_imagens_{datetime.now().strftime('%Y%m%d')}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width='stretch'
    )
    
    pdf_rel = PDFModule.gerar_pdf_tabela_estatistica(df_rel, "Densidade de Imagens por Páginas")
    col2.download_button(
        "📄 PDF",
        pdf_rel,
        f"rel_densidade_imagens_{datetime.now().strftime('%Y%m%d')}.pdf",
        "application/pdf",
        width='stretch'
    )

# ==========================================
# 5. MAIN APP LOGIC
# ==========================================

def main():
    # ===== LOGO NELIC =====
    with st.sidebar:
        try:
            st.image("Nelic-imagem.png", use_container_width=True)
        except:
            st.error("Imagem não encontrada no caminho especificado.")
            st.markdown("## NELIC")  # Fallback
        st.write("")  # Espaçamento

    # ==================================================
    # SISTEMA DE AUTENTICAÇÃO
    # ==================================================

    # Campo de senha na sidebar
    with st.sidebar:
        senha_digitada = st.text_input(
            "🔐 Área Restrita (Catalogadores)",
            type="password",
            placeholder="Digite a senha..."
        )

    # Verificar autenticação
    usuario_autenticado = False
    senha_correta = None

    # Tenta pegar a senha dos secrets
    try:
        if "SENHA_ADMIN" in st.secrets:
            senha_correta = st.secrets["SENHA_ADMIN"]
    except:
        pass

    # Se não encontrou nos secrets, exibe aviso
    if senha_correta is None:
        if senha_digitada:
            st.sidebar.error("⚠️ Configure SENHA_ADMIN em .streamlit/secrets.toml")
    # Verifica se a senha está correta
    elif senha_digitada == senha_correta:
        usuario_autenticado = True
        st.sidebar.success("✅ Modo Editor: ATIVADO")

        # Detecta se está rodando no Streamlit Cloud
        is_cloud = os.environ.get('STREAMLIT_SHARING_MODE') or os.environ.get('STREAMLIT_SERVER_HEADLESS')

        if is_cloud:
            st.sidebar.warning("⚠️ **Atenção**: Dados inseridos online não são salvos permanentemente. Para catalogação segura, use o sistema local no seu computador.")
    elif senha_digitada:
        st.sidebar.error("❌ Senha incorreta")

    st.sidebar.markdown("---")

    # ==================================================
    # MENU ADAPTATIVO (baseado na autenticação)
    # ==================================================

    # Menu completo para usuários autenticados
    if usuario_autenticado:
        opcoes_menu = [
            "NELIC",
            "CATALOGAÇÃO",
            "FICHAS & NOTAS",
            "EXPLORAR DADOS",
            "RELATÓRIOS",
            "ANÁLISE COMPARATIVA",
            "ANÁLISE AVANÇADA",  # Nova aba para Humanidades Digitais
            "DIÁRIO DE PESQUISA",
            "METODOLOGIA",
            "MAIS DADOS",
            "EXPORTAR",
            "QUALIDADE DOS DADOS"
        ]
        icones_menu = [
            "house-fill",
            "pencil-square",
            "file-text",
            "search",
            "graph-up",
            "diagram-3",
            "lightbulb",  # Ícone para Análise Avançada
            "journal-text",
            "book",
            "database",
            "download",
            "shield-check"
        ]
    else:
        # Menu público (apenas visualização)
        opcoes_menu = [
            "NELIC",
            "FICHAS & NOTAS",
            "EXPLORAR DADOS",
            "RELATÓRIOS",
            "ANÁLISE COMPARATIVA",
            "ANÁLISE AVANÇADA",  # Nova aba para Humanidades Digitais
            "METODOLOGIA",
            "MAIS DADOS",
            "QUALIDADE DOS DADOS"
        ]
        icones_menu = [
            "house-fill",
            "file-text",
            "search",
            "graph-up",
            "diagram-3",
            "lightbulb",  # Ícone para Análise Avançada
            "book",
            "database",
            "shield-check"
        ]

    # ===== MENU DE NAVEGAÇÃO LIMPO =====
    with st.sidebar:
        menu = option_menu(
            menu_title=None,  # Remove o título "NAVEGAÇÃO"
            options=opcoes_menu,
            icons=icones_menu,
            default_index=0,
            key="main_sidebar_menu", # ADICIONADO KEY PARA PERSISTÊNCIA NA SIDEBAR

            orientation="vertical",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#ffffff"  # Fundo Branco
                },
                "icon": {
                    "color": "#366092",  # Ícones Azul
                    "font-size": "14px"
                },
                "nav-link": {
                    "color": "#366092",  # Texto Azul
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px 12px",
                    "border-radius": "6px",
                    "font-weight": "bold",  # Negrito
                    "--hover-color": "#f0f2f6"
                },
                "nav-link-selected": {
                    "background-color": "#366092",  # Fundo Azul quando selecionado
                    "color": "white"  # Texto Branco quando selecionado
                }
            }
        )

    st.sidebar.markdown("---")

    # Status do sistema
    if usuario_autenticado:
        st.sidebar.markdown("🔓 **Modo Catalogador**")
    else:
        st.sidebar.markdown("👁️ **Modo Visitante**")
        st.sidebar.info("💡 Digite a senha acima para catalogar")

    dados = PersistenceModule.load_data()
    df = pd.DataFrame(dados)
    df = UtilsModule.sanitizar_dataframe(df)

    # --- CORREÇÃO ESTRUTURAL: ORDENAÇÃO DE REVISTAS ---
    # Converte a coluna 'n' para categórica com ordem definida
    if 'n' in df.columns:
        df['n'] = df['n'].astype(str)
        df['n'] = pd.Categorical(df['n'], categories=ORDEM_SIBILA, ordered=True)

    # --- NELIC ---
    if menu == "NELIC":
        st.title("NÚCLEO DE ESTUDOS LITERÁRIOS & CULTURAIS")
        st.markdown("---")

        # Introdução
        st.markdown("""
        O **Núcleo de Estudos Literários e Culturais (NELIC)**, sediado no Departamento de Língua e
        Literatura Vernáculas da UFSC, consolidou-se desde meados dos anos 1990 como um dos principais
        laboratórios de pesquisa sobre **periodismo literário e cultural**, **formação de cânones** e
        **arquivo no Brasil**, articulando crítica literária, teoria cultural, estudos de poesia e
        reflexão sobre o contemporâneo.

        Seu eixo estruturante é o estudo de revistas, jornais e suplementos culturais (sobretudo da
        segunda metade do século XX) e a construção de um amplo arquivo e base de dados, a partir dos
        quais se interrogam a modernidade, a memória, o anacronismo e a própria ideia de literatura.
        """)

        st.markdown("---")

        # Origem e perfil institucional
        st.markdown("## 1. Origem e Perfil Institucional")
        st.markdown("""
        O NELIC nasce em **1996**, no CCE/UFSC, vinculado ao Departamento de Língua e Literatura
        Vernáculas (DLLV), a partir do projeto integrado **"Poéticas Contemporâneas"**, coordenado
        por **Maria Lucia de Barros Camargo**.

        Desde sua criação, se define como **laboratório de formação de pesquisadores** (graduação e
        pós-graduação) em crítica textual e crítica cultural, dedicando-se ao mapeamento da crítica
        literária e cultural brasileira a partir dos anos 1970, por meio da indexação e estudo de
        periódicos literários e/ou culturais em circulação no país.

        O trabalho é descrito como uma leitura do periódico como **"tecido semântico"**, cuja
        inteligibilidade depende de leitura retrospectiva e de cruzamentos de dados, bem como uma
        proposta de **"ciclo de leitura da crítica literária e cultural"**, que vai do texto crítico
        à crítica da crítica, produzindo uma metacrítica do campo.
        """)

        st.markdown("---")

        # Acervo e Base de Dados
        st.markdown("## 2. Acervo e Base de Dados")

        col_acervo1, col_acervo2 = st.columns([3, 2])

        with col_acervo1:
            st.markdown("""
            O NELIC mantém um amplo **acervo físico de periódicos literários e culturais** –
            revistas, jornais e suplementos, nacionais e estrangeiros – aberto à consulta e pesquisa local.

            Esse acervo é complementado pela **Base de Dados "Periodismo Literário e Cultural"**, que:

            - 📊 Reúne mais de **46 mil artigos indexados**
            - 📰 Cobre cerca de **70 revistas, jornais e suplementos**
            - 🔍 Permite busca por palavras-chave, autores colaboradores, autores citados, resumos
            """)

        with col_acervo2:
            st.info("""
            **Periódicos Mapeados:**

            • Revista Civilização Brasileira
            • Folhetim e Mais! (Folha de S.Paulo)
            • Revista do Livro
            • Cult
            • Argumento
            • Opinião
            • Versus
            • Revista USP
            • Almanaque
            • Revista Brasileira de Poesia
            • José
            • 34 Letras
            • Entre outros
            """)

        st.markdown("---")

        # Boletim de Pesquisa NELIC
        st.markdown("## 3. Boletim de Pesquisa NELIC")
        st.markdown("""
        O **Boletim de Pesquisa NELIC** é o periódico científico semestral do núcleo, voltado à
        publicação de textos acadêmicos nas áreas de literatura e cultura contemporâneas, com ênfase
        em produção brasileira e latino-americana.

        **Dados Institucionais:**
        - 📅 Início da publicação: **1997**
        - 🔢 ISSN (online): **1984-784X**
        - 🌐 Indexado em: DOAJ, Latindex, OpenAlex, ROAD, CariNiana
        """)

        st.markdown("---")

        # Pesquisadores Principais
        st.markdown("## 4. Pesquisadores Principais")

        # Maria Lucia de Barros Camargo
        with st.expander("**Maria Lucia de Barros Camargo** - Fundadora e Pesquisadora Sênior"):
            st.markdown("""
            **Bolsista de Produtividade em Pesquisa do CNPq - Nível 1B**
            
            Endereço para acessar o Lattes: http://lattes.cnpq.br/7854330137879524

            **Trajetória:**
            - Doutora em Letras (Teoria Literária e Literatura Comparada) pela USP (1990)
            - Tese sobre a poesia de **Ana Cristina Cesar**
            - Professora titular de Teoria Literária (aposentada em 2019)
            - Criadora do NELIC e do projeto "Poéticas Contemporâneas" (1996)
            - Vice-presidente da ABRALIC (1996-1998)
            - Pró-Reitora de Pós-Graduação da UFSC (2008-2012)
            - Coordenadora do PPG em Literatura (2013-2018)

            **Áreas de Pesquisa:**
            - Periodismo cultural
            - Revistas literárias
            - Poesia contemporânea
            - Anos 70
            - Crítica cultural

            **Obra Principal:**
            *Atrás dos olhos pardos: uma leitura da poesia de Ana Cristina Cesar* (Editora Argos, 2003)
            """)

        # Carlos Eduardo Schmidt Capela
        with st.expander("**Carlos Eduardo Schmidt Capela** - Coordenador Atual"):
            st.markdown("""
            **Bolsista de Produtividade em Pesquisa do CNPq - Nível 1D**
            
            Endereço para acessar o Lattes: http://lattes.cnpq.br/6619827107636765

            **Coordenação:**
            - Coordenador docente do NELIC
            - Editor do Boletim de Pesquisa NELIC

            **Projetos de Pesquisa:**
            - *Heranças de andanças de Ahasverus pela América Latina* (2023–atual)
            - *Ahasverus (heranças : errâncias : hiâncias)* (2019–2023)
            - *A gesta entre nós, tal gesto: disposições e dispositivos* (2013–2019)

            **Linha de Pesquisa:**
            Literaturas comparadas, estudos de arquivos ficcionais e figurações da errância e da estrangeiridade
            """)

        # Raúl Antelo
        with st.expander("**Raúl Antelo** - Pesquisador Sênior"):
            st.markdown("""
            Endereço para acessar o Lattes: http://lattes.cnpq.br/4828668706498888

            **Trajetória:**
            - Crítico e teórico argentino-brasileiro (n. 1950)
            - Professor titular de Literatura Brasileira na UFSC (aposentado)
            - Pesquisador do CNPq
            - Guggenheim Fellow
            - Ex-presidente da ABRALIC
            - Doutorado *honoris causa* pela Universidad Nacional de Cuyo

            **Projeto Atual:**
            *Por uma conceituação da bioestética: arquivo e diagramas do vivente na América Latina* (2018–atual)

            **Obras Principais:**
            - *Literatura em revista*
            - *João do Rio: o dândi e a especulação*
            - *Maria com Marcel. Duchamp nos trópicos*
            - *Archifilologías latinoamericanas*
            - *Crítica acéfala*
            - *A máquina afilológica*
            - *A ruinologia*
            """)

        st.markdown("---")

        # Outros pesquisadores e linhas de pesquisa
        st.markdown("## 5. Outros Pesquisadores e Linhas de Pesquisa no NELIC")

        st.markdown("""
        Atuando em projetos que articulam **crítica e criação na modernidade**, **poéticas da América Latina**,
        **autografias e escritas de si**, **literatura**, **cinema**, **cultura**, e **contracultura**.
        """)

        # Pesquisadores por categoria
        with st.expander("👥 **Pesquisadores do NELIC** (expandir para ver lista completa)"):
            st.markdown("""
            **Docentes:**
            Carlos Eduardo Schmidt Capela, Maria Lucia de Barros Camargo, Raúl Antelo, Jorge Hoffmann Wolff,
            Artur de Vargas Giorgi, André Fiorussi, Jair Tadeu da Fonseca, Laíse Ribas Bastos,
            Luz Maria Luisa Rodriguez, Manoel Ricardo de Lima, Júlia Vasconcelos Studart, Renata Telles,
            Valentina da Silva Nunes, Jeferson Candido, Fernando Floriani Petry.

            **Doutorado:**
            Joaquín Emanuel Correa, Adner De Almeida Sena, Alessandra Guterres Deifeld, Allende Renck Pereira,
            André Vichara Barcellos, Arthur Katrein Mora, Carlos Speck Pereira, Dennis Lauro Radünz,
            Denise Rogenski Raizel, Diogo Araujo Da Silva, Gabriela Cristina Carvalho Gonçalves Dos Santos,
            Isabel Cristina Costa Louzada, João Paulo Zarelli Rocha, Julio Aied Passos, Karoline Zampiva Corrêa,
            Lisbeth Juliana Monroy Ortiz, Lucas De Mello Schlemper, Lucas Garcia Nunes, Luciéle Bernardi De Souza,
            María Mercedes Rodriguez, Patrícia Galelli, Raquel de Figueredo Eltermann, Renato Bradbury De Oliveira,
            Sérgio Leite Barboza, Sinval Soares Paulino, William Fernandes Rabelo Da Silva, Wilson Sousa Oliveira.

            **Mestrado:**
            Carolina Maria Cardoso Pilati, Clara Padial Lucas, Clareana Moreira De Castro Eugênio,
            Emmanuele Amaral Santos, Matheus Reiser Muller, Renato Rodrigues, Zulmar Dustin Ribeiro Anchieta.

            **Graduação:**
            Nycolas Gomes Correia, Vivianne Oliveira Rodrigues.
            """)

        st.info("""
        **Nota:** O NELIC funciona como rede de pesquisadores associados e ex‑orientandos.
        Nesse sentido, listamos Laíse Ribas Bastos, Jeferson Candido, Simone Dias, Fernando Floriani Petry,
        Renata Telles, Valentina Nunes, Júlia Studart, Manoel Ricardo de Lima, que hoje atuam em outras
        instituições e continuam vinculados a projetos ou publicações do núcleo.
        """)

        st.markdown("---")

        # Formação de Pesquisadores: Teses e Dissertações
        st.markdown("## 6. Formação de Pesquisadores: Teses e Dissertações")
        st.markdown("""
        O **NELIC** mantém listas extensas de **teses e dissertações** defendidas sob sua égide,
        sobretudo no **Programa de Pós-Graduação em Literatura (PPGLit/UFSC)**, abrangendo temas
        centrais do núcleo com forte inserção nacional e latino‑americana.

        O núcleo integra o PPGLit/UFSC, atuando na formação de mestres e doutores com foco em:

        - Literatura Brasileira Contemporânea
        - Teoria Literária e Crítica Cultural
        - Práticas de Arquivo e Memória Literária
        - Metodologia NELIC de catalogação e análise de periódicos
        - Periodismo Literário e Cultural

        Além disso, desde sua fundação, o núcleo incorpora estudantes de **graduação** (bolsistas de
        Iniciação Científica PIBIC/CNPq e voluntários) em suas atividades de catalogação, digitalização e
        pesquisa, promovendo a formação completa do pesquisador acadêmico.
        """)

        st.markdown("---")

        # Contato
        st.markdown("## 📧 Contato e Informações")

        col_contato1, col_contato2 = st.columns(2)

        with col_contato1:
            st.markdown("""
            **Website:**
            [nelic.ufsc.br](http://nelic.ufsc.br)

            **Boletim de Pesquisa NELIC:**
            [periodicos.ufsc.br/index.php/nelic](https://periodicos.ufsc.br/index.php/nelic)

            **Base de Dados:**
            Acesso via site do NELIC
            """)

        with col_contato2:
            st.markdown("""
            **Endereço:**
            Universidade Federal de Santa Catarina
            Centro de Comunicação e Expressão
            Departamento de Língua e Literatura Vernáculas
            Campus Universitário - Trindade
            88040-900 - Florianópolis - SC
            """)

        st.markdown("---")

        st.info("""
        💡 **Mais Informações:** O NELIC está aberto à colaboração com pesquisadores, projetos
        interinstitucionais e consultas ao acervo físico mediante agendamento. Entre em contato
        para mais detalhes sobre o acesso à Base de Dados, possibilidades de pesquisa conjunta ou
        orientações acadêmicas na área de periodismo literário e cultural.
        """)

    # --- CATALOGAÇÃO ---
    elif menu == "CATALOGAÇÃO":
        st.title("EDITOR DE REGISTROS")
        form = CatalogacaoForm(dados, df)

        # Seleção de Modo com Botão de Limpeza
        col_mode1, col_mode2, col_mode3 = st.columns([2, 3, 5])
        with col_mode1:
            st.markdown("**Modo:**")
        with col_mode2:
            mode = st.radio("Selecione:", ["NOVO REGISTRO", "EDITAR EXISTENTE"], key="mode_radio", horizontal=True, label_visibility="collapsed")
        with col_mode3:
            # Botão LIMPAR TUDO - só aparece e funciona em NOVO REGISTRO
            if 'mode_radio' in st.session_state and st.session_state.mode_radio == "NOVO REGISTRO":
                if st.button("🗑️ LIMPAR TUDO", help="Limpa todos os campos do formulário"):
                    # Limpar TUDO no session_state relacionado ao formulário
                    st.session_state.selected_record = None
                    st.session_state.loaded_json = None
                    st.session_state.clear_json_input = True
                    st.session_state.current_editing_record_id = None  # ⚠️ CORREÇÃO: Resetar rastreamento

                    # Incrementar contador para forçar recriação do formulário
                    if 'form_clear_counter' not in st.session_state:
                        st.session_state.form_clear_counter = 0
                    st.session_state.form_clear_counter += 1

                    # Limpar TODOS os campos do formulário e busca
                    keys_to_delete = [key for key in st.session_state.keys()
                                      if key.startswith('form_') or key.startswith('busca_') or
                                      key.startswith('confirm_delete_') or key.startswith('sel_tipo_') or
                                      key.startswith('sel_subtipo_') or key.startswith('icon_')]
                    for key in keys_to_delete:
                        del st.session_state[key]
                    
                    # Limpar lista de linhas de iconografia
                    if 'iconografias_rows' in st.session_state:
                        st.session_state.iconografias_rows = []

                    st.success("✅ Formulário limpo!")
                    time.sleep(0.3)
                    st.rerun()

        # Inicializar session_state para registro selecionado
        if 'selected_record' not in st.session_state:
            st.session_state.selected_record = None

        # Limpar registro selecionado e formulário ao mudar de modo
        if 'previous_mode' not in st.session_state:
            st.session_state.previous_mode = mode
        if st.session_state.previous_mode != mode:
            st.session_state.selected_record = None
            st.session_state.loaded_json = None
            st.session_state.previous_mode = mode
            st.session_state.current_editing_record_id = None  # ⚠️ CORREÇÃO: Resetar rastreamento
            # Incrementar contador para forçar recriação do formulário
            if 'form_clear_counter' not in st.session_state:
                st.session_state.form_clear_counter = 0
            st.session_state.form_clear_counter += 1
            # Limpar TODOS os campos do formulário ao mudar de modo
            for key in list(st.session_state.keys()):
                if key.startswith('form_') or key.startswith('busca_') or key.startswith('confirm_delete_') or key.startswith('icon_'):
                    del st.session_state[key]
            # IMPORTANTE: Recarregar a página para aplicar a limpeza
            st.rerun()

        rec = {}

        # No modo NOVO REGISTRO, garantir que rec seja vazio se não houver registro carregado
        if mode == "NOVO REGISTRO":
            # Se selected_record for None, garantir que rec seja vazio
            if st.session_state.selected_record is None:
                rec = {}
            else:
                rec = st.session_state.selected_record

        # Lógica de Editar Existente
        elif mode == "EDITAR EXISTENTE" and dados:
            st.markdown("---")
            st.markdown("### 🔍 BUSCAR REGISTRO PARA EDITAR")

            # Campos de busca
            col1, col2, col3 = st.columns(3)
            with col1:
                # Listar todas as revistas únicas
                # Ordenação correta na lista de seleção manual
                revs_existentes = list(set([str(d.get('n', '')) for d in dados if d.get('n')]))
                revistas_disponiveis = sorted(
                    revs_existentes,
                    key=lambda x: ORDEM_SIBILA.index(x) if x in ORDEM_SIBILA else 999
                )
                revista_busca = st.selectbox("Nº REVISTA", [""] + revistas_disponiveis, key="busca_revista")

            with col2:
                # Filtrar registros por revista selecionada e criar lista com títulos
                if revista_busca:
                    registros_filtrados = [d for d in dados if str(d.get('n', '')) == revista_busca]
                else:
                    registros_filtrados = dados

                # Criar dicionário: "registro - título" -> dados completos
                registros_opcoes = {}
                for d in registros_filtrados:
                    if d.get('registro'):
                        titulo = d.get('titulo_artigo', '[sem título]')
                        # Limitar título a 60 caracteres
                        titulo_curto = titulo[:60] + "..." if len(titulo) > 60 else titulo
                        chave = f"{d.get('registro')} - {titulo_curto}"
                        registros_opcoes[chave] = d

                # Ordenar por número de registro (extrair parte numérica para ordenação correta)
                def extrair_numero(chave):
                    try:
                        # Extrair "10 de 23" -> 10
                        parte_reg = chave.split(' - ')[0]  # "10 de 23"
                        numero = parte_reg.split(' ')[0]   # "10"
                        return int(numero)
                    except:
                        return 0
                opcoes_ordenadas = sorted(registros_opcoes.keys(), key=extrair_numero)

                registro_busca = st.selectbox("REGISTRO (título)", [""] + opcoes_ordenadas, key="busca_registro")

            with col3:
                # Botão de busca
                st.write("")
                st.write("")
                buscar = st.button("🔎 CARREGAR REGISTRO", type="primary", use_container_width=True)

            # Encontrar e carregar o registro
            if registro_busca and registro_busca in registros_opcoes:
                # Registro selecionado diretamente do dropdown com título
                novo_rec = registros_opcoes[registro_busca]
                # Verificar se é um registro diferente do atual
                if st.session_state.selected_record is None or st.session_state.selected_record.get('_id') != novo_rec.get('_id'):
                    st.session_state.selected_record = novo_rec
                    st.session_state.force_form_update = True
                    st.rerun()
                rec = novo_rec
                st.success(f"✅ Registro carregado: **{rec.get('titulo_artigo', '[sem título]')}**")
            elif buscar and (revista_busca or registro_busca):
                st.warning("⚠️ Por favor, selecione um registro da lista.")

            # Usar registro do session_state se existir
            if st.session_state.selected_record is not None:
                rec = st.session_state.selected_record

        form.render(rec=rec, mode=mode)

    # --- FICHAS & NOTAS ---
    elif menu == "FICHAS & NOTAS":
        view = FichasNotasView(df, dados)
        view.render()

    # --- EXPLORAR DADOS ---
    elif menu == "EXPLORAR DADOS":
        st.title("🔎 EXPLORAR DADOS")
        if not df.empty:
            # Linha de filtros com botão de reset
            st.markdown("### 🔍 FILTROS DE BUSCA")

            # GERAÇÃO DE TODOS OS TIPOS TEXTUAIS POSSÍVEIS (do TIPOS_TEXTUAIS)
            # Incluindo TODAS as combinações de tipo + subtipo
            tipos_completos = []
            for tipo, subtipos in DataModule.TIPOS_TEXTUAIS.items():
                for subtipo in subtipos:
                    if subtipo == "Sem especificação":
                        # Tipo sem subtipo específico
                        tipos_completos.append(tipo)
                    else:
                        # Tipo com subtipo (formato: "TIPO - Subtipo")
                        tipos_completos.append(f"{tipo} - {subtipo}")
            tipos_clean = sorted(list(set(tipos_completos)))

            # Preparar listas para os filtros
            revs = sorted(
                df['n'].astype(str).unique(),
                key=lambda x: ORDEM_SIBILA.index(x) if x in ORDEM_SIBILA else 999
            )

            # FILTROS
            col_filtros1, col_filtros2 = st.columns(2)

            with col_filtros1:
                termo = st.text_input("🔍 Busca Livre (Título/Resumo):", key="explorar_termo")

            with col_filtros2:
                # Selectbox para revista
                revista_sel = st.selectbox(
                    "📖 Revista",
                    ["Todas"] + revs,
                    key="explorar_revista_select"
                )
                f_rev = [revista_sel] if revista_sel != "Todas" else []

            # Filtro de Tipo Textual - TODOS os tipos e subtipos!
            with st.expander("📝 Tipo Textual (clique para expandir e selecionar)", expanded=False):
                st.caption(f"💡 {len(tipos_clean)} tipos textuais disponíveis (incluindo todos os subtipos)")

                # Campo de busca para filtrar tipos
                busca_tipo = st.text_input(
                    "🔍 Filtrar tipos:",
                    key="busca_tipo_textual",
                    placeholder="Digite para filtrar a lista..."
                )

                # Filtrar tipos conforme a busca
                if busca_tipo:
                    tipos_exibir = [t for t in tipos_clean
                                   if busca_tipo.lower() in t.lower()]
                    st.caption(f"✅ {len(tipos_exibir)} tipos encontrados")
                else:
                    tipos_exibir = tipos_clean

                # Mostrar TODOS os tipos (filtrados ou não)
                f_tipo = []
                cols_tipo = st.columns(3)
                for idx, tipo in enumerate(tipos_exibir):
                    with cols_tipo[idx % 3]:
                        if st.checkbox(tipo, key=f"tipo_check_{tipo}"):
                            f_tipo.append(tipo)

            # Filtro de Palavras-chave - TODAS AS 461!
            with st.expander("🏷️ Palavras-Chave (clique para expandir e selecionar)", expanded=False):
                st.caption(f"💡 {len(DataModule.LISTA_PALAVRAS_CHAVE)} palavras-chave disponíveis")

                # Campo de busca para filtrar palavras
                busca_palavra = st.text_input(
                    "🔍 Filtrar palavras:",
                    key="busca_palavra_chave",
                    placeholder="Digite para filtrar a lista..."
                )

                # Filtrar palavras conforme a busca
                if busca_palavra:
                    palavras_exibir = [p for p in DataModule.LISTA_PALAVRAS_CHAVE
                                      if busca_palavra.lower() in p.lower()]
                    st.caption(f"✅ {len(palavras_exibir)} palavras encontradas")
                else:
                    palavras_exibir = DataModule.LISTA_PALAVRAS_CHAVE

                # Mostrar TODAS as palavras (filtradas ou não)
                f_kw = []
                cols_kw = st.columns(4)
                for idx, palavra in enumerate(palavras_exibir):
                    with cols_kw[idx % 4]:
                        if st.checkbox(palavra, key=f"kw_check_{palavra}"):
                            f_kw.append(palavra)

            # Botão de reset
            if st.button("🔄 Limpar Todos os Filtros", help="Desmarca todos os filtros e recarrega"):
                # Limpar TODOS os checkboxes e filtros
                for key in list(st.session_state.keys()):
                    if key.startswith('tipo_check_') or key.startswith('kw_check_') or key.startswith('explorar_'):
                        del st.session_state[key]
                st.rerun()

            # Aplicar filtros
            res = df.copy()
            criterios = []

            if f_rev:
                res = res[res['n'].astype(str).isin(f_rev)]
                criterios.append(f"Revistas: {', '.join(f_rev)}")

            if f_tipo:
                # Filtro que compara o valor COMPLETO (tipo + subtipo) do vocabulario_controlado
                def filtro_tipo(valor):
                    if pd.isna(valor) or not valor:
                        return False
                    valor_completo = str(valor).strip()
                    # Verificar se o valor completo está nos tipos selecionados
                    return valor_completo in f_tipo

                res = res[res['vocabulario_controlado'].apply(filtro_tipo)]
                criterios.append(f"Tipos: {', '.join(f_tipo)}")

            if f_kw:
                res = res[
                    res['palavras_chave'].apply(
                        lambda x: any(
                            k.lower() in [i.lower() for i in (x if isinstance(x, list) else [])]
                            for k in f_kw
                        )
                    )
                ]
                criterios.append(f"Palavras-chave: {', '.join(f_kw)}")

            if termo:
                res = res[
                    res.astype(str).apply(lambda x: x.str.contains(termo, case=False, na=False)).any(axis=1)
                ]
                criterios.append(f"Termo livre: '{termo}'")

            # Estatísticas dos resultados
            str_criterios = " | ".join(criterios) if criterios else "Toda a base de dados"
            total_base = len(df)
            qtd_res = len(res)
            pct_res = (qtd_res / total_base * 100) if total_base > 0 else 0

            st.markdown("---")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.metric("Registros Encontrados", f"{qtd_res} de {total_base}", f"{pct_res:.1f}% da base")
            with col_info2:
                if criterios:
                    st.info(f"🔍 Filtros ativos: {str_criterios}")
                else:
                    st.info("📊 Mostrando todos os registros")

            # Tabela de resultados com configuração aprimorada
            st.markdown("### 📋 RESULTADOS")

            # Configuração de colunas visíveis
            if 'colunas_visiveis' not in st.session_state:
                st.session_state.colunas_visiveis = ['n', 'registro', 'titulo_artigo', 'autores_colaboradores', 'vocabulario_controlado']

            with st.expander("⚙️ Configurar Colunas Visíveis", expanded=False):
                todas_colunas = list(res.columns)
                colunas_recomendadas = ['n', 'registro', 'titulo_artigo', 'autores_colaboradores', 'vocabulario_controlado', 'palavras_chave', 'paginas']

                col_config1, col_config2 = st.columns([4, 1])
                with col_config1:
                    st.session_state.colunas_visiveis = st.multiselect(
                        "Selecione as colunas a exibir:",
                        todas_colunas,
                        default=st.session_state.colunas_visiveis if st.session_state.colunas_visiveis else colunas_recomendadas,
                        key="multiselect_colunas"
                    )
                with col_config2:
                    if st.button("↻ Reset", help="Mostrar colunas padrão", use_container_width=True):
                        st.session_state.colunas_visiveis = colunas_recomendadas
                        st.rerun()

            # Preparar DataFrame para exibição
            res_prepared = res.copy()

            # Remover coluna _timestamp se existir
            if '_timestamp' in res_prepared.columns:
                res_prepared = res_prepared.drop(columns=['_timestamp'])

            # Formatar iconografias para mostrar dados reais
            if 'iconografias' in res_prepared.columns:
                def formatar_iconografias(icon_list):
                    if not icon_list or not isinstance(icon_list, list):
                        return ""
                    itens = []
                    for icon in icon_list:
                        if isinstance(icon, dict):
                            tipo = icon.get('tipo', '')
                            desc = icon.get('descricao', '')
                            if tipo:
                                itens.append(f"{tipo}: {desc}" if desc else tipo)
                    return " | ".join(itens) if itens else ""

                res_prepared['iconografias'] = res_prepared['iconografias'].apply(formatar_iconografias)

            # Reordenar colunas: mover entidade_coletiva perto de autores
            # e nota_edicao para o final
            colunas_ordenadas = []
            for col in res_prepared.columns:
                if col not in ['entidade_coletiva', 'nota_edicao']:
                    colunas_ordenadas.append(col)
                    # Inserir entidade_coletiva após tradutores
                    if col == 'tradutores' and 'entidade_coletiva' in res_prepared.columns:
                        colunas_ordenadas.append('entidade_coletiva')

            # Adicionar nota_edicao no final
            if 'nota_edicao' in res_prepared.columns:
                colunas_ordenadas.append('nota_edicao')

            res_prepared = res_prepared[colunas_ordenadas]

            # Atualizar colunas visíveis se necessário
            if st.session_state.colunas_visiveis:
                colunas_disponiveis = [col for col in st.session_state.colunas_visiveis if col in res_prepared.columns]
                res_display = res_prepared[colunas_disponiveis]
            else:
                res_display = res_prepared

            # Ajuste visual do índice para começar em 1
            res_display = res_display.copy()
            res_display.reset_index(drop=True, inplace=True)
            res_display.index = res_display.index + 1

            st.dataframe(
                res_display,
                column_config={
                    "n": "n.",
                    "registro": "Registro",
                    "titulo_artigo": "Título",
                    "subtitulo_artigo": "Subtítulo",
                    "autores_colaboradores": "Autores",
                    "entidade_coletiva": "Entidade Coletiva",
                    "tradutores": "Tradutores",
                    "autores_citados": "Autores Citados",
                    "vocabulario_controlado": "Tipo Textual",
                    "palavras_chave": "Palavras-Chave",
                    "nome_pessoal_como_assunto": "Nome Pessoal Como Assunto",
                    "paginas": "Páginas",
                    "resumo": "Resumo",
                    "iconografias": "Iconografias",
                    "nota_edicao": "Nota da Edição",
                    "notas_pesquisa": "Notas de Pesquisa",
                    "idioma_01": "Idioma 01",
                    "idioma_02": "Idioma 02",
                    "ordem_exibicao": "Ordem de Exibição"
                },
                use_container_width=True,
                height=400
            )

            df_citados = None
            df_colab = None
            if not res.empty:
                st.markdown("---")
                st.subheader("📊 ANÁLISE COM BASE NA SELEÇÃO DOS DADOS")
                s_citados = DataModule.get_normalized_series(res, 'autores_citados')
                c_stat1, c_stat2 = st.columns(2)
                with c_stat1:
                    if not s_citados.empty:
                        df_citados = UtilsModule.calculate_stats_with_percentage(s_citados)
                        st.markdown("📌 **AUTORES MAIS CITADOS**")
                        df_citados.index = df_citados.index + 1
                        st.dataframe(df_citados.head(10), width='stretch')
                    else:
                        st.info("Nenhum autor citado nestes registros.")

                with c_stat2:
                    s_colab = DataModule.get_normalized_series(res, 'autores_colaboradores')
                    if not s_colab.empty:
                        df_colab = UtilsModule.calculate_stats_with_percentage(s_colab)
                        st.markdown("✍️ **AUTORES COLABORADORES**")
                        df_colab.index = df_colab.index + 1
                        st.dataframe(df_colab.head(10), width='stretch')
                    else:
                        st.info("Nenhum colaborador listado nestes registros.")

            st.markdown("---")
            st.markdown("### 📥 EXPORTAR RESULTADOS DA BUSCA")

            # Layout melhorado para botões de exportação com espaçamento adequado
            col_export1, col_export2, col_export3 = st.columns([1, 1, 1])

            # Renomear colunas para português antes de exportar
            res_export = res.rename(columns={
                "n": "Nº Revista",
                "registro": "Registro",
                "titulo_artigo": "Título",
                "subtitulo_artigo": "Subtítulo",
                "autores_colaboradores": "Autores Colaboradores",
                "entidade_coletiva": "Entidade Coletiva",
                "tradutores": "Tradutores",
                "autores_citados": "Autores Citados",
                "vocabulario_controlado": "Tipo Textual",
                "palavras_chave": "Palavras-Chave",
                "nome_pessoal_como_assunto": "Nome Pessoal (Assunto)",
                "paginas": "Páginas",
                "resumo": "Resumo",
                "iconografias": "Iconografias",
                "nota_edicao": "Nota da Edição",
                "idioma_01": "Idioma 1",
                "idioma_02": "Idioma 2",
                "notas_pesquisa": "Notas de Pesquisa"
            })
            excel_busca = UtilsModule.converter_excel(res_export)
            pdf_busca = PDFModule.gerar_pdf_busca_analitica(res, len(df), str_criterios, df_citados, df_colab)
            
            with col_export1:
                st.download_button(
                    "📊 BAIXAR EXCEL",
                    excel_busca,
                    f"busca_sibila_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Exportar resultados para Excel"
                )

            with col_export2:
                st.download_button(
                    "📄 BAIXAR PDF",
                    pdf_busca,
                    f"relatorio_sibila_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "application/pdf",
                    use_container_width=True,
                    help="Exportar relatório para PDF"
                )

            with col_export3:
                # Informação sobre o que será exportado
                st.info(f"📊 Exportando {qtd_res} registro(s)")

        else:
            st.warning("⚠️ Base de dados vazia. Cadastre registros na aba CATALOGAÇÃO.")

    # --- RELATÓRIOS ---
    elif menu == "RELATÓRIOS":
        st.title("📑 RELATÓRIOS NELIC")
        if df.empty:
            st.warning("Base vazia.")
        else:
            tipo_rel = st.selectbox(
                "Selecione o relatório:",
                [
                    "Volume de itens por revista",
                    "Índice de publicações bilíngues",
                    "Iconografia por revista",
                    "Autores como assunto vs colaboradores",
                    "Análise por tipos textuais",
                    "Manifesto",
                    "Sibila",
                    "Palavras-chave",
                    "Densidade de Imagens por Páginas"
                ]
            )
            if tipo_rel == "Volume de itens por revista":
                relatorio_mapa_colaboracao(df)
            elif tipo_rel == "Índice de publicações bilíngues":
                relatorio_bilinguismo(df)
            elif tipo_rel == "Iconografia por revista":
                relatorio_iconografia(df)
            elif tipo_rel == "Autores como assunto vs colaboradores":
                relatorio_autores_assunto_colab(df)
            elif tipo_rel == "Análise por tipos textuais":
                relatorio_tipos_textuais(df)
            elif tipo_rel == "Manifesto":
                relatorio_manifesto(df)
            elif tipo_rel == "Sibila":
                relatorio_sibila(df)
            elif tipo_rel == "Palavras-chave":
                relatorio_palavras_chave(df)
            elif tipo_rel == "Densidade de Imagens por Páginas":
                relatorio_densidade_paginas(df)

    # --- ANÁLISE COMPARATIVA ---
    elif menu == "ANÁLISE COMPARATIVA":
        st.title("📊 ANÁLISE COMPARATIVA")
        if df.empty:
            st.warning("Base vazia.")
        else:
            st.markdown("Compare dois conjuntos de registros a partir de filtros NELIC.")

            def aplicar_filtros(df_base, prefix):
                c1, c2, c3, c4 = st.columns(4)
                termo = c1.text_input(f"{prefix} · termo livre (título/resumo)", key=f"termo_{prefix}")
                revs_local = sorted(
                    df_base['n'].astype(str).unique(),
                    key=lambda x: ORDEM_SIBILA.index(x) if x in ORDEM_SIBILA else 999
                )
                f_rev = c2.multiselect(f"{prefix} · revistas", revs_local, key=f"rev_{prefix}")
                tipos_raw_local = df_base['vocabulario_controlado'].astype(str).unique()
                tipos_clean_local = sorted(list(set([t.split(' - ')[0] for t in tipos_raw_local])))
                f_tipo = c3.multiselect(f"{prefix} · tipos textuais", tipos_clean_local, key=f"tipo_{prefix}")
                f_bil = c4.selectbox(
                    f"{prefix} · bilíngue",
                    ["Todos", "Apenas bilíngues", "Apenas não bilíngues"],
                    key=f"bil_{prefix}"
                )
                res_local = df_base.copy()
                if f_rev:
                    res_local = res_local[res_local['n'].astype(str).isin(f_rev)]
                if f_tipo:
                    res_local = res_local[
                        res_local['vocabulario_controlado'].apply(lambda x: str(x).split(' - ')[0] in f_tipo)
                    ]
                res_local = res_local.copy()
                res_local['__bil'] = res_local.apply(UtilsModule.is_bilingue, axis=1)
                if f_bil == "Apenas bilíngues":
                    res_local = res_local[res_local['__bil']]
                elif f_bil == "Apenas não bilíngues":
                    res_local = res_local[~res_local['__bil']]
                if termo:
                    res_local = res_local[
                        res_local.astype(str).apply(lambda x: x.str.contains(termo, case=False)).any(axis=1)
                    ]
                return res_local.drop(columns=['__bil'], errors='ignore')

            st.markdown("#### Conjunto A")
            df_A = aplicar_filtros(df, "A")
            st.markdown(f"Conjunto A: {len(df_A)} registros.")

            st.markdown("#### Conjunto B")
            df_B = aplicar_filtros(df, "B")
            st.markdown(f"Conjunto B: {len(df_B)} registros.")

            if not df_A.empty or not df_B.empty:
                st.markdown("---")
                st.subheader("🔬 Métricas comparadas")
                def metricas(df_sub):
                    s_colab = DataModule.get_normalized_series(df_sub, 'autores_colaboradores')
                    s_cit = DataModule.get_normalized_series(df_sub, 'autores_citados')
                    ic = df_sub['iconografias'].apply(
                        lambda x: isinstance(x, list) and len(x) > 0
                    ).sum()
                    df_tmp = df_sub.copy()
                    df_tmp['__bil'] = df_tmp.apply(UtilsModule.is_bilingue, axis=1)
                    bil = df_tmp['__bil'].sum()
                    total = len(df_tmp)
                    return {
                        "registros": total,
                        "colab_distintos": s_colab.nunique(),
                        "cit_distintos": s_cit.nunique(),
                        "pct_iconografia": (ic / total * 100) if total > 0 else 0,
                        "pct_bilingue": (bil / total * 100) if total > 0 else 0
                    }

                mA = metricas(df_A) if not df_A.empty else None
                mB = metricas(df_B) if not df_B.empty else None
                cA, cB = st.columns(2)
                with cA:
                    st.markdown("##### Conjunto A")
                    if mA:
                        st.metric("Registros", mA["registros"])
                        st.metric("Colaboradores distintos", mA["colab_distintos"])
                        st.metric("Autores citados distintos", mA["cit_distintos"])
                        st.metric("% com iconografia", f"{mA['pct_iconografia']:.1f}%")
                        st.metric("% bilíngue", f"{mA['pct_bilingue']:.1f}%")
                    else:
                        st.info("Sem registros no conjunto A.")

                with cB:
                    st.markdown("##### Conjunto B")
                    if mB:
                        st.metric("Registros", mB["registros"])
                        st.metric("Colaboradores distintos", mB["colab_distintos"])
                        st.metric("Autores citados distintos", mB["cit_distintos"])
                        st.metric("% com iconografia", f"{mB['pct_iconografia']:.1f}%")
                        st.metric("% bilíngue", f"{mB['pct_bilingue']:.1f}%")
                    else:
                        st.info("Sem registros no conjunto B.")

    # --- QUALIDADE DOS DADOS ---
    elif menu == "QUALIDADE DOS DADOS":
        st.title("🧪 QUALIDADE DOS DADOS")
        if df.empty:
            st.warning("Base vazia.")
        else:
            st.markdown(
                "Monitoramento de consistência e lacunas conforme as exigências metodológicas do NELIC."
            )
            df_local = df.copy()
            sem_pag = df_local[
                df_local['paginas'].isna() |
                (df_local['paginas'].astype(str).str.strip() == '')
            ]
            sem_tit = df_local[
                df_local['titulo_artigo'].isna() |
                (df_local['titulo_artigo'].astype(str).str.strip() == '')
            ]
            df_local['tipo_base'] = df_local['vocabulario_controlado'].astype(str).apply(
                lambda x: x.split(' - ')[0]
            )
            precisa_resumo = ~df_local['tipo_base'].isin(TIPOS_SEM_RESUMO)
            sem_resumo = df_local[
                precisa_resumo &
                (
                    df_local['resumo'].isna() |
                    (df_local['resumo'].astype(str).str.strip() == '')
                )
            ]
            # Substituição de st.tabs por option_menu para persistência
            # t1, t2, t3, t4, t5 = st.tabs(
            #     ["Sem páginas", "Sem título", "Sem resumo (quando exigido)", "Duplicidade de registro", "Autores Similares"]
            # )
            

            selected_quality = option_menu(
                menu_title=None,
                options=["Sem páginas", "Sem título", "Sem resumo", "Duplicidade", "Autores Similares"],
                icons=["file-earmark-x", "card-heading", "justify-left", "files", "people"], 
                orientation="horizontal",
                key="quality_menu"
            )
            
            if selected_quality == "Sem páginas":
                st.markdown("#### Registros sem informação de páginas")
                st.write(f"Total: {len(sem_pag)}")
                df_sem_pag = sem_pag[['n', 'registro', 'titulo_artigo', 'paginas']].copy()
                df_sem_pag.reset_index(drop=True, inplace=True)
                df_sem_pag.index = df_sem_pag.index + 1
                st.dataframe(df_sem_pag, width='stretch')
            elif selected_quality == "Sem título":
                st.markdown("#### Registros sem título")
                st.write(f"Total: {len(sem_tit)}")
                df_sem_tit = sem_tit[['n', 'registro', 'paginas']].copy()
                df_sem_tit.reset_index(drop=True, inplace=True)
                df_sem_tit.index = df_sem_tit.index + 1
                st.dataframe(df_sem_tit, width='stretch')
            elif selected_quality == "Sem resumo":
                st.markdown("#### Registros sem resumo em tipos que demandam resumo analítico")
                st.write(f"Total: {len(sem_resumo)}")
                df_sem_resumo = sem_resumo[['n', 'registro', 'vocabulario_controlado', 'titulo_artigo']].copy()
                df_sem_resumo.reset_index(drop=True, inplace=True)
                df_sem_resumo.index = df_sem_resumo.index + 1
                st.dataframe(
                    df_sem_resumo,
                    width='stretch'
                )
            elif selected_quality == "Duplicidade":
                st.markdown("#### Duplicidade potencial de campo REGISTRO")
                df_local['chave_unica'] = df_local['n'].astype(str) + '_' + df_local['registro'].astype(str)
                duplicatas = df_local[df_local.duplicated(subset=['chave_unica'], keep=False)]
                if not duplicatas.empty:
                    st.write(f"Total: {len(duplicatas)} registros com potencial duplicidade")

                    if usuario_autenticado:
                        st.warning("⚠️ Use os botões 🗑️ para excluir registros duplicados. Esta ação é IRREVERSÍVEL!")
                    else:
                        st.info("ℹ️ Para excluir registros duplicados, faça login com a senha de editor.")

                    for chave in duplicatas['chave_unica'].unique():
                        grupo = duplicatas[duplicatas['chave_unica'] == chave]
                        st.markdown(f"**🔴 Duplicata encontrada: Revista {grupo.iloc[0]['n']} - Registro {grupo.iloc[0]['registro']}**")

                        # Mostrar cada registro duplicado com botão de exclusão
                        for idx, row in grupo.iterrows():
                            if usuario_autenticado:
                                col1, col2 = st.columns([5, 1])
                                with col1:
                                    st.write(f"**ID:** {row['_id']} | **Título:** {row['titulo_artigo']} | **Páginas:** {row['paginas']}")
                                with col2:
                                    if st.button(f"🗑️ Excluir", key=f"delete_{row['_id']}"):
                                        # Confirmar exclusão
                                        if f"confirm_delete_{row['_id']}" not in st.session_state:
                                            st.session_state[f"confirm_delete_{row['_id']}"] = True
                                            st.warning(f"⚠️ Clique novamente para CONFIRMAR a exclusão do registro ID: {row['_id']}")
                                            st.rerun()
                                        else:
                                            # Excluir o registro
                                            dados_novos = [d for d in dados if d.get('_id') != row['_id']]
                                            if PersistenceModule.save_data(dados_novos):
                                                st.success(f"✅ Registro ID {row['_id']} excluído com sucesso!")
                                                del st.session_state[f"confirm_delete_{row['_id']}"]
                                                st.rerun()
                                            else:
                                                st.error("❌ Erro ao salvar os dados após exclusão.")
                            else:
                                st.write(f"**ID:** {row['_id']} (login necessário para excluir)")


                else:
                    st.success("✅ Nenhuma duplicidade detectada! Todos os registros possuem combinações únicas de Revista + Registro.")
                df_local = df_local.drop(columns=['chave_unica'])

            elif selected_quality == "Autores Similares":
                st.markdown("#### 🕵️ Potenciais Duplicatas de Autores")
                st.info("Esta aba agrupa autores pelo SOBRENOME para ajudar a identificar variações de grafia (ex: 'SILVA, Jose' e 'SILVA, J.').")

                # 1. Coletar todos os autores normalizados
                all_authors = DataModule.get_normalized_series(df, 'autores_colaboradores')
                # Adicionar autores citados também? O usuário pediu "mesmos autores", geralmente refere-se a colaboradores, mas citados também importa.
                all_cited = DataModule.get_normalized_series(df, 'autores_citados')
                
                # Unir e pegar únicos
                unique_authors = sorted(list(set(all_authors.tolist() + all_cited.tolist())))
                
                # 2. Agrupar por sobrenome (primeira palavra antes da vírgula ou espaço)
                groups = {}
                for auth in unique_authors:
                    if not auth: continue
                    # Assumindo formato ABNT "SOBRENOME, Nome"
                    sobrenome = auth.split(',')[0].strip()
                    if sobrenome not in groups:
                        groups[sobrenome] = []
                    groups[sobrenome].append(auth)
                
                # 3. Filtrar apenas grupos com > 1 variação
                potential_dupes = []
                for surname, names in groups.items():
                    if len(names) > 1:
                        potential_dupes.append({
                            "Sobrenome": surname,
                            "Variações Encontradas": ", ".join(sorted(names)),
                            "Qtd": len(names)
                        })
                
                if potential_dupes:
                    df_dupes = pd.DataFrame(potential_dupes).sort_values("Sobrenome")
                    st.write(f"Total de grupos suspeitos: {len(df_dupes)}")
                    st.dataframe(df_dupes, width='stretch', hide_index=True)
                    
                    st.markdown("""
                    **Como corrigir?**
                    Se identificar autores que são a mesma pessoa (ex: "BACH" e "BACH, J.S."), anote esses casos e me informe para que eu adicione à regra de unificação automática (`CANONICAL_AUTHORS`).
                    """)
                else:
                    st.success("Nenhuma duplicata óbvia baseada em sobrenome encontrada.")

    # ==========================================
    # --- ANÁLISE AVANÇADA (Humanidades Digitais) ---
    # ==========================================
    elif menu == "ANÁLISE AVANÇADA":
        st.title("🔬 ANÁLISE AVANÇADA")
        st.markdown("""
        Ferramentas de análise para **Humanidades Digitais**: análise de redes,
        processamento de linguagem natural e correlações entre dados do catálogo.
        """)

        if df.empty:
            st.warning("⚠️ Base de dados vazia. Adicione registros primeiro.")
        else:
            # Sub-abas dentro da Análise Avançada (Substituído por option_menu para persistência)
            # tab_redes, tab_nlp, tab_correlacao, tab_dna = st.tabs([
            #     "🕸️ Análise de Redes",
            #     "📝 Análise Textual (NLP)",
            #     "📊 Matriz de Correlação",
            #     "🧬 DNA das Edições"
            # ])
            
            selected_adv = option_menu(
                menu_title=None,
                options=["🕸️ Análise de Redes", "📝 Análise Textual (NLP)", "📊 Matriz de Correlação", "🧬 DNA das Edições"],
                icons=["share", "file-text", "bar-chart", "diagram-3"], 
                orientation="horizontal",
                key="menu_analise_avancada"
            )

            # ========================================
            # TAB 1: ANÁLISE DE REDES
            # ========================================
            if selected_adv == "🕸️ Análise de Redes":
                st.markdown("### 🕸️ Análise de Redes: Autores e Citações")
                st.markdown("""
                Visualize as relações entre **autores colaboradores** e **autores citados**.
                Esta análise permite identificar padrões de citação e redes de influência.
                """)

                if not NETWORKX_AVAILABLE:
                    st.error("❌ Biblioteca `networkx` não disponível. Instale com: `pip install networkx`")
                else:
                    try:
                        # Extrair dados para o grafo
                        edges_autor_citacao = []
                        for _, row in df.iterrows():
                            autores = row.get('autores_colaboradores', [])
                            citados = row.get('autores_citados', [])
                            if isinstance(autores, list) and isinstance(citados, list):
                                for autor in autores:
                                    for citado in citados:
                                        if autor and citado:
                                            edges_autor_citacao.append((autor.strip(), citado.strip()))

                        if not edges_autor_citacao:
                            st.info("ℹ️ Não há dados suficientes para gerar o grafo. Verifique se existem registros com autores colaboradores E autores citados.")
                        else:
                            # Criar grafo
                            G = nx.DiGraph()
                            G.add_edges_from(edges_autor_citacao)

                            # Métricas do grafo
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Autores", G.number_of_nodes())
                            with col2:
                                st.metric("Citações", G.number_of_edges())
                            with col3:
                                densidade = nx.density(G)
                                st.metric("Densidade", f"{densidade:.4f}", help="Indica o quão conectada é a rede. Se fosse 1.0, todos os autores citariam todos os outros. Valor baixo indica rede esparsa.")
                            with col4:
                                componentes = nx.number_weakly_connected_components(G)
                                st.metric("Componentes", componentes, help="Número de grupos isolados de autores. Se for 1, todos estão conectados. Se for maior, existem 'ilhas' de citação separadas.")

                            st.markdown("---")

                            # Top autores mais citados
                            st.markdown("#### 📊 Autores Mais Citados")
                            in_degree = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)[:15]
                            if in_degree:
                                df_in = pd.DataFrame(in_degree, columns=['Autor', 'Vezes Citado'])
                                fig_in = px.bar(df_in, x='Vezes Citado', y='Autor', orientation='h',
                                               title='15 Autores Mais Citados')
                                fig_in.update_layout(yaxis={'categoryorder': 'total ascending'})
                                st.plotly_chart(fig_in, use_container_width=True)

                            # Top autores que mais citam
                            st.markdown("#### 📊 Autores que Mais Citam")
                            out_degree = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)[:15]
                            if out_degree:
                                df_out = pd.DataFrame(out_degree, columns=['Autor', 'Citações Feitas'])
                                fig_out = px.bar(df_out, x='Citações Feitas', y='Autor', orientation='h',
                                                title='15 Autores que Mais Citam Outros')
                                fig_out.update_layout(yaxis={'categoryorder': 'total ascending'})
                                st.plotly_chart(fig_out, use_container_width=True)

                            st.markdown("---")

                            # Exportação
                            st.markdown("#### 💾 Exportar Dados da Rede")
                            col_exp1, col_exp2, col_exp3 = st.columns(3)

                            with col_exp1:
                                # Exportar GEXF (para Gephi)
                                try:
                                    import io
                                    gexf_buffer = io.BytesIO()
                                    nx.write_gexf(G, gexf_buffer)
                                    gexf_data = gexf_buffer.getvalue()
                                    st.download_button(
                                        "📥 Baixar GEXF (Gephi)",
                                        data=gexf_data,
                                        file_name="rede_autores_citacoes.gexf",
                                        mime="application/gexf+xml",
                                        key="btn_gexf"
                                    )
                                except Exception as e:
                                    st.warning(f"Erro ao gerar GEXF: {e}")

                            with col_exp2:
                                # CSV de nós
                                nodes_data = []
                                for node in G.nodes():
                                    nodes_data.append({
                                        'ID': node,
                                        'Rótulo': node,
                                        'Grau Entrada': G.in_degree(node),
                                        'Grau Saída': G.out_degree(node)
                                    })
                                df_nodes = pd.DataFrame(nodes_data)
                                excel_nodes = UtilsModule.converter_excel(df_nodes)
                                st.download_button(
                                    "📥 Baixar Nós (Excel)",
                                    data=excel_nodes,
                                    file_name="autores_nos.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_nodes_excel"
                                )

                            with col_exp3:
                                # Excel de arestas
                                edges_data = [{'Origem': e[0], 'Destino': e[1]} for e in G.edges()]
                                df_edges = pd.DataFrame(edges_data)
                                excel_edges = UtilsModule.converter_excel(df_edges)
                                st.download_button(
                                    "📥 Baixar Arestas (Excel)",
                                    data=excel_edges,
                                    file_name="citacoes_arestas.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_edges_excel"
                                )

                    except Exception as e:
                        st.error(f"❌ Erro na análise de redes: {str(e)}")

                    # ==========================================
                    # VIZ INTERATIVA PYVIS
                    # ==========================================
                    st.markdown("#### 🕸️ VISUALIZAÇÃO INTERATIVA") # (PYVIS)
                    st.markdown("Clique no botão abaixo para gerar o grafo. *Para grandes volumes de dados, isso pode levar alguns segundos.*")
                    
                    if not PYVIS_AVAILABLE:
                        st.warning("⚠️ Biblioteca `pyvis` não instalada. Instale com `pip install pyvis` para ver o grafo interativo.")
                    elif 'G' in locals() and G.number_of_nodes() > 0:
                        # Função de scroll (no-op se não for usada)
                        def _scroll_to_pyvis():
                            try:
                                st.markdown(
                                    "<div id='pyvis_anchor'></div>",
                                    unsafe_allow_html=True
                                )
                            except Exception:
                                pass

                        def _reset_pyvis_state():
                            # Limpa estados corrompidos (ex.: bool) para evitar erros de iteração
                            cache_state = st.session_state.get("_pyvis_cache")
                            last_state = st.session_state.get("_pyvis_last")

                            if not isinstance(cache_state, dict):
                                st.session_state["_pyvis_cache"] = {}
                            else:
                                st.session_state["_pyvis_cache"] = {
                                    k: v for k, v in cache_state.items() if isinstance(v, str)
                                }

                            if not isinstance(last_state, dict):
                                st.session_state["_pyvis_last"] = {}
                            else:
                                # Mantém apenas se render_html for string e graph for nx.Graph
                                graph_ok = isinstance(last_state.get("graph"), nx.Graph)
                                html_ok = isinstance(last_state.get("render_html"), str)
                                st.session_state["_pyvis_last"] = last_state if graph_ok and html_ok else {}

                        _reset_pyvis_state()

                        # ========== CONTROLES SIMPLIFICADOS ==========
                        st.markdown("##### 🎯 Selecione um autor para destacar:")
                        try:
                            autor_options = sorted(G.nodes())
                        except Exception:
                            autor_options = [str(n) for n in G.nodes()]

                        autor_pref_label = st.selectbox(
                            "Autor",
                            autor_options,
                            index=None,
                            placeholder="Digite ou selecione um autor...",
                            key="pyvis_autor_select"
                        )
                        autor_pref = autor_pref_label

                        # Mostrar relações do autor IMEDIATAMENTE ao selecionar
                        if autor_pref and autor_pref in G.nodes():
                            st.success(f"**Autor selecionado:** {autor_pref}")

                            # Calcular citações - ordenadas alfabeticamente
                            # REGRA: Excluir o próprio autor (não pode citar/ser citado por si mesmo)
                            # NOTA: O grafo não armazena citações múltiplas, então cada relação aparece 1 vez
                            try:
                                # Quem o autor cita - lista alfabética
                                citas_raw = [v for _, v in G.out_edges(autor_pref) if v != autor_pref]
                                citas_lista = sorted(list(set(citas_raw)))

                                # Quem cita o autor - lista alfabética
                                citado_raw = [u for u, _ in G.in_edges(autor_pref) if u != autor_pref]
                                citado_lista = sorted(list(set(citado_raw)))
                            except:
                                citas_lista = []
                                citado_lista = []

                            col_cita, col_citado = st.columns(2)

                            with col_cita:
                                st.markdown(f"**→ Cita ({len(citas_lista)} autores):**")
                                if citas_lista:
                                    # Mostrar os 15 primeiros (ordem alfabética)
                                    for autor_c in citas_lista[:15]:
                                        st.write(f"• {autor_c}")

                                    # Se houver mais, mostrar expander
                                    if len(citas_lista) > 15:
                                        with st.expander(f"📋 Ver todos os {len(citas_lista)} autores citados"):
                                            st.markdown("**Lista completa (ordem alfabética):**")
                                            for i, autor_c in enumerate(citas_lista, 1):
                                                st.write(f"{i}. {autor_c}")

                                            # Gerar PDF para download
                                            try:
                                                pdf_cita = FPDF()
                                                pdf_cita.add_page()
                                                pdf_cita.set_font("Arial", 'B', 14)
                                                pdf_cita.cell(0, 10, f"Autores citados por {autor_pref}", ln=1)
                                                pdf_cita.set_font("Arial", '', 10)
                                                pdf_cita.cell(0, 8, f"Total: {len(citas_lista)} autores (ordem alfabetica)", ln=1)
                                                pdf_cita.ln(5)
                                                for i, autor_c in enumerate(citas_lista, 1):
                                                    texto = f"{i}. {autor_c}"
                                                    texto_safe = texto.encode('latin-1', 'replace').decode('latin-1')
                                                    pdf_cita.cell(0, 6, texto_safe, ln=1)
                                                pdf_bytes_cita = pdf_cita.output(dest='S').encode('latin-1', 'replace')

                                                st.download_button(
                                                    "📥 Exportar lista (PDF)",
                                                    data=pdf_bytes_cita,
                                                    file_name=f"citados_por_{autor_pref.replace(' ', '_')}.pdf",
                                                    mime="application/pdf",
                                                    key="btn_pdf_cita"
                                                )
                                            except Exception as e:
                                                st.caption(f"Erro ao gerar PDF: {e}")
                                else:
                                    st.write("_Nenhum_")

                            with col_citado:
                                st.markdown(f"**← Citado por ({len(citado_lista)} autores):**")
                                if citado_lista:
                                    # Mostrar os 15 primeiros (ordem alfabética)
                                    for autor_c in citado_lista[:15]:
                                        st.write(f"• {autor_c}")

                                    # Se houver mais, mostrar expander
                                    if len(citado_lista) > 15:
                                        with st.expander(f"📋 Ver todos os {len(citado_lista)} autores que citam"):
                                            st.markdown("**Lista completa (ordem alfabética):**")
                                            for i, autor_c in enumerate(citado_lista, 1):
                                                st.write(f"{i}. {autor_c}")

                                            # Gerar PDF para download
                                            try:
                                                pdf_citado = FPDF()
                                                pdf_citado.add_page()
                                                pdf_citado.set_font("Arial", 'B', 14)
                                                pdf_citado.cell(0, 10, f"Autores que citam {autor_pref}", ln=1)
                                                pdf_citado.set_font("Arial", '', 10)
                                                pdf_citado.cell(0, 8, f"Total: {len(citado_lista)} autores (ordem alfabetica)", ln=1)
                                                pdf_citado.ln(5)
                                                for i, autor_c in enumerate(citado_lista, 1):
                                                    texto = f"{i}. {autor_c}"
                                                    texto_safe = texto.encode('latin-1', 'replace').decode('latin-1')
                                                    pdf_citado.cell(0, 6, texto_safe, ln=1)
                                                pdf_bytes_citado = pdf_citado.output(dest='S').encode('latin-1', 'replace')

                                                st.download_button(
                                                    "📥 Exportar lista (PDF)",
                                                    data=pdf_bytes_citado,
                                                    file_name=f"citam_{autor_pref.replace(' ', '_')}.pdf",
                                                    mime="application/pdf",
                                                    key="btn_pdf_citado"
                                                )
                                            except Exception as e:
                                                st.caption(f"Erro ao gerar PDF: {e}")
                                else:
                                    st.write("_Nenhum_")

                        st.markdown("---")
                        st.markdown("##### 🛠️ Configurações do Grafo")

                        col_cfg1, col_cfg2 = st.columns(2)
                        with col_cfg1:
                            top_n_nodes = st.slider(
                                "Principais autores",
                                10, 200, 50,
                                key="pyvis_top_n"
                            )
                        with col_cfg2:
                            spacing_distance = st.slider(
                                "Distância visual",
                                20, 150, 50,
                                key="pyvis_spacing"
                            )

                        col_cfg3, col_cfg4 = st.columns(2)
                        with col_cfg3:
                            use_community = st.checkbox("Colorir por comunidade", value=True, key="pyvis_community")
                            show_arrows = st.checkbox("Mostrar setas", value=True, key="pyvis_arrows")
                        with col_cfg4:
                            disable_physics = st.checkbox("Layout fixo", value=True, key="pyvis_physics")
                            small_node_mode = st.checkbox("Fontes menores", value=False, key="pyvis_compact")

                        # Botão de gerar grafo
                        if st.button("🔄 GERAR GRAFO", key="btn_gerar_grafo_main", type="primary", use_container_width=True):
                            st.session_state["_pyvis_cache"] = {}
                            st.session_state["_pyvis_last"] = {}
                            st.session_state["_pyvis_params"] = {
                                "autor_pref": autor_pref,
                                "top_n_nodes": top_n_nodes,
                                "spacing_distance": spacing_distance,
                                "use_community": use_community,
                                "show_arrows": show_arrows,
                                "disable_physics": disable_physics,
                                "small_node_mode": small_node_mode
                            }
                            try:
                                with st.spinner("Gerando visualização..."):
                                    if not isinstance(G, nx.Graph):
                                        raise TypeError(f"G esperado como Graph, recebeu {type(G)}")

                                    G_viz = G.copy()
                                    node_degrees = dict(G_viz.degree())
                                    sorted_nodes = sorted(node_degrees.items(), key=lambda item: item[1], reverse=True)

                                    # LOGICA DE FILTRO:
                                    # Se um autor estiver selecionado, focar EXCLUSIVAMENTE nele e seus vizinhos (Ego Network).
                                    # Caso contrário, mostrar os Top N autores mais conectados (Visão Geral).
                                    
                                    if autor_pref and autor_pref in G_viz.nodes():
                                        nodes_to_keep = {autor_pref}
                                        # Adicionar vizinhos do autor selecionado
                                        if G_viz.is_directed():
                                            for _, v in G_viz.out_edges(autor_pref):
                                                nodes_to_keep.add(v)
                                            for u, _ in G_viz.in_edges(autor_pref):
                                                nodes_to_keep.add(u)
                                        else:
                                            for neighbor in G_viz.neighbors(autor_pref):
                                                nodes_to_keep.add(neighbor)
                                    else:
                                        # Visão Geral: Top N nós
                                        nodes_to_keep = set([n[0] for n in sorted_nodes[:top_n_nodes]])

                                    G_viz = G_viz.subgraph(list(nodes_to_keep)).copy()

                                    if G_viz.number_of_nodes() == 0:
                                        st.warning("Nenhum autor encontrado com os filtros atuais.")
                                    else:
                                        stabilization_iterations = 200

                                        current_controls = {
                                            "top_n": top_n_nodes,
                                            "use_community": use_community,
                                            "show_arrows": show_arrows,
                                            "disable_physics": disable_physics,
                                            "stabilization_iterations": stabilization_iterations,
                                            "small_node_mode": small_node_mode,
                                            "spacing_distance": spacing_distance,
                                            "autor_pref": autor_pref,
                                        }
                                        prev_controls = st.session_state.get("_pyvis_controls")
                                        if prev_controls != current_controls:
                                            st.session_state["_pyvis_controls"] = current_controls
                                            st.session_state["_pyvis_last"] = {}

                                        render_html = None

                                        # Exportações do subgrafo filtrado
                                        try:
                                            gexf_buffer = BytesIO()
                                            nx.write_gexf(G_viz, gexf_buffer)
                                            gexf_data_viz = gexf_buffer.getvalue()
                                        except Exception:
                                            gexf_data_viz = b""

                                        nodes_data_viz = []
                                        for node in G_viz.nodes():
                                            nodes_data_viz.append({
                                                'ID': node,
                                                'Rótulo': node,
                                                'Grau Entrada': G_viz.in_degree(node),
                                                'Grau Saída': G_viz.out_degree(node)
                                            })
                                        df_nodes_viz = pd.DataFrame(nodes_data_viz)
                                        excel_nodes_viz = UtilsModule.converter_excel(df_nodes_viz)

                                        edges_data_viz = [{'Origem': e[0], 'Destino': e[1]} for e in G_viz.edges()]
                                        df_edges_viz = pd.DataFrame(edges_data_viz)
                                        excel_edges_viz = UtilsModule.converter_excel(df_edges_viz)

                                        def _safe_text(txt: str) -> str:
                                            try:
                                                return str(txt).encode("latin-1", "replace").decode("latin-1")
                                            except Exception:
                                                return str(txt)

                                        # --- GERAR PDF PADRONIZADO (Estilo Relatório de Busca) ---
                                        try:
                                            pdf = FPDF()
                                            pdf.add_page()
                                            
                                            # Título Dinâmico
                                            if autor_pref and autor_pref in G_viz.nodes():
                                                title_pdf = f"REDE DE AUTORAS(ES): {autor_pref.upper()}"
                                                
                                                # Cabeçalho Padrão
                                                PDFModule._add_standard_header(pdf, title_pdf)
                                                
                                                # Métricas Específicas (Pedido do Usuário)
                                                # Autores relacionados: Total - 1 (o próprio)
                                                qtd_relacionados = max(0, G_viz.number_of_nodes() - 1)
                                                
                                                # Cita e Citado Por (Grafo Dirigido)
                                                try:
                                                    qtd_cita = G_viz.out_degree(autor_pref)
                                                    qtd_citado = G_viz.in_degree(autor_pref)
                                                except:
                                                    qtd_cita = 0
                                                    qtd_citado = 0
                                                
                                                pdf.set_y(pdf.get_y() + 5)
                                                pdf.set_font("Arial", 'B', 10)
                                                
                                                # Linha de métricas
                                                metrics_text = f"Autores relacionados: {qtd_relacionados}  |  Cita: {qtd_cita}  |  Citado por: {qtd_citado}"
                                                pdf.cell(0, 8, PDFModule.to_latin1(metrics_text), ln=1)
                                                pdf.ln(5)

                                                # Função auxiliar para buscar contexto no DF
                                                def get_contexto(source, target, df_ref):
                                                    matches = []
                                                    for _, row in df_ref.iterrows():
                                                        cols = row.get('autores_colaboradores', [])
                                                        cits = row.get('autores_citados', [])
                                                        if isinstance(cols, list) and isinstance(cits, list):
                                                            if source in cols and target in cits:
                                                                n_rev = row.get('n', '?')
                                                                tit = row.get('titulo_artigo', '[sem título]')
                                                                # Formatação solicitada: revista número; Título: ...; (número do registro)
                                                                reg_n = row.get('registro', '?')
                                                                matches.append(f"Revista {n_rev}; Título: {tit}; ({reg_n})")
                                                    return matches

                                                # 1. QUEM O AUTOR CITA (Out-Degree)
                                                cited_by_author = sorted([v for _, v in G_viz.out_edges(autor_pref)])
                                                
                                                if cited_by_author:
                                                    pdf.set_font("Arial", 'B', 12)
                                                    pdf.cell(0, 10, PDFModule.to_latin1("AUTORES QUE CITA"), ln=1)
                                                    pdf.set_font("Arial", '', 10)
                                                    
                                                    for cited in cited_by_author:
                                                        pdf.set_font("Arial", 'B', 10)
                                                        # Apenas o nome do autor aqui
                                                        pdf.cell(0, 6, PDFModule.to_latin1(f"{cited}"), ln=1)
                                                        
                                                        # Contexto
                                                        contextos = get_contexto(autor_pref, cited, df)
                                                        
                                                        if contextos:
                                                            pdf.set_font("Arial", 'I', 9)
                                                            pdf.cell(0, 5, PDFModule.to_latin1("Obras em que cita:"), ln=1)
                                                            
                                                            pdf.set_font("Arial", '', 9)
                                                            pdf.set_text_color(60, 60, 60)
                                                            for ctx in contextos:
                                                                pdf.cell(5) # Indent
                                                                pdf.cell(0, 5, PDFModule.to_latin1(f"- {ctx}"), ln=1)
                                                            pdf.set_text_color(0, 0, 0)
                                                        pdf.ln(3)

                                                pdf.ln(5)

                                                # 2. QUEM CITA O AUTOR (In-Degree)
                                                citing_author = sorted([u for u, _ in G_viz.in_edges(autor_pref)])
                                                
                                                if citing_author:
                                                    pdf.set_font("Arial", 'B', 12)
                                                    pdf.cell(0, 10, PDFModule.to_latin1("CITADO POR"), ln=1)
                                                    pdf.set_font("Arial", '', 10)
                                                    
                                                    for citing in citing_author:
                                                        pdf.set_font("Arial", 'B', 10)
                                                        pdf.cell(0, 6, PDFModule.to_latin1(f"{citing}"), ln=1)
                                                        
                                                        contextos = get_contexto(citing, autor_pref, df)
                                                        
                                                        if contextos:
                                                            pdf.set_font("Arial", 'I', 9)
                                                            # AQUI A MUDANÇA: 'Obras em que foi citado'
                                                            pdf.cell(0, 5, PDFModule.to_latin1("Obras em que foi citada(o):"), ln=1)
                                                            
                                                            pdf.set_font("Arial", '', 9)
                                                            pdf.set_text_color(60, 60, 60)
                                                            for ctx in contextos:
                                                                pdf.cell(5)
                                                                pdf.cell(0, 5, PDFModule.to_latin1(f"- {ctx}"), ln=1)
                                                            pdf.set_text_color(0, 0, 0)
                                                        pdf.ln(3)

                                            else:
                                                # Visão Geral (sem autor selecionado)
                                                title_pdf = "REDE DE AUTORAS(ES) (VISÃO GERAL)"
                                                PDFModule._add_standard_header(pdf, title_pdf)
                                                pdf.set_y(pdf.get_y() + 5)
                                                metrics_text = f"Total de Autores: {G_viz.number_of_nodes()} | Total de Conexões: {G_viz.number_of_edges()}"
                                                pdf.set_font("Arial", '', 11)
                                                pdf.cell(0, 8, PDFModule.to_latin1(metrics_text), ln=1)
                                                pdf.ln(5)
                                                
                                                pdf.set_font("Arial", 'B', 12)
                                                pdf.cell(0, 10, PDFModule.to_latin1("Autores mais conectados (Visão Geral):"), ln=1)
                                                pdf.set_font("Arial", '', 10)
                                                for autor, val in sorted(G_viz.in_degree(), key=lambda x: x[1], reverse=True)[:50]:
                                                    pdf.cell(0, 7, PDFModule.to_latin1(f"{autor}: {val} citações"), ln=1)

                                            pdf_output = pdf.output(dest="S").encode("latin-1", "replace")
                                        except Exception as e:
                                            # st.error(f"Erro PDF: {e}") 
                                            pdf_output = b""

                                        if True:  # Sempre gerar novo grafo
                                            # 2. ESTILIZAÇÃO PROFISSIONAL (Clean & Clear)
                                            sub_degrees = dict(G_viz.degree())
                                            nx.set_node_attributes(
                                                G_viz,
                                                {n: max(6, min(26, 8 + (d * 2))) for n, d in sub_degrees.items()},
                                                'size'
                                            )

                                            if use_community:
                                                try:
                                                    from networkx.algorithms import community
                                                    communities = list(community.greedy_modularity_communities(G_viz))
                                                    colors = [
                                                        '#E6194B', '#3CB44B', '#FFE119', '#4363D8', '#F58231',
                                                        '#911EB4', '#46F0F0', '#F032E6', '#BCF60C', '#FABEBE',
                                                        '#008080', '#E6BEFF', '#9A6324', '#FFFAC8', '#800000',
                                                        '#AAFFC3', '#808000', '#FFD8B1', '#000075', '#808080'
                                                    ]
                                                    color_map = {}
                                                    for i, comm in enumerate(communities):
                                                        c = colors[i % len(colors)]
                                                        for node in comm:
                                                            color_map[node] = c
                                                    nx.set_node_attributes(G_viz, color_map, 'color')
                                                except Exception:
                                                    nx.set_node_attributes(G_viz, '#4e79a7', 'color')
                                            else:
                                                nx.set_node_attributes(G_viz, '#59a14f', 'color')

                                            # 3. CONFIGURAÇÃO PYVIS - Layout com distância configurável
                                            node_font_size = 11 if small_node_mode or G_viz.number_of_nodes() > 300 else 13
                                            base_bg_color = "#ffffff" if small_node_mode else "#f7f9fb"
                                            label_color = "#0f172a"

                                            # k controla a distância ideal entre nós (maior k = mais espaço)
                                            # Escala: 20->0.3, 60->0.9, 150->2.25
                                            k_value = spacing_distance / 66.0
                                            pos = nx.spring_layout(G_viz, k=k_value, iterations=80, seed=42)

                                            # Multiplicador de escala para visualização (maior spacing = mais spread)
                                            scale_factor = 400 + (spacing_distance * 8)
                                            for node_id, (x_pos, y_pos) in pos.items():
                                                G_viz.nodes[node_id]['x'] = float(x_pos * scale_factor)
                                                G_viz.nodes[node_id]['y'] = float(y_pos * scale_factor)

                                            net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="#000000", directed=show_arrows)
                                            net.from_nx(G_viz)

                                            # Garante rótulo visível em cada nó
                                            for n in net.nodes:
                                                n["label"] = str(n.get("label") or n.get("id"))

                                            # --- ESTILIZAÇÃO DE ARESTAS (SOLICITAÇÃO DO USUÁRIO) ---
                                            # Cor distinta e destaque visual
                                            for edge in net.edges:
                                                edge['color'] = {
                                                    'color': '#888888',     # Cinza médio visível
                                                    'highlight': '#d32f2f', # Vermelho forte ao clicar
                                                    'hover': '#d32f2f',
                                                    'inherit': False        # Importante: não herdar cor dos nós
                                                }
                                                edge['width'] = 1.0
                                                edge['arrows'] = {
                                                    'to': {'enabled': True, 'scaleFactor': 0.6}
                                                }
                                                # title (tooltip)
                                                edge['title'] = "Cita"

                                            for n in net.nodes:
                                                node_border = n.get("color", "#4e79a7")
                                                n.update({
                                                    "borderWidth": 1,
                                                    "borderWidthSelected": 3,
                                                    "color": {
                                                        "background": n.get("color", "#4e79a7"),
                                                        "border": node_border,
                                                        "highlight": {
                                                            "background": "#ffdd57",
                                                            "border": "#ff3860"
                                                        }
                                                    },
                                                    # Sombra leve
                                                    "shadow": {"enabled": True, "color": "rgba(0,0,0,0.1)", "size": 5, "x": 2, "y": 2}
                                                })

                                            # OPÇÕES AVANÇADAS DE INTERAÇÃO
                                            options_json = f"""
                                            {{
                                                "interaction": {{
                                                    "hover": true,
                                                    "tooltipDelay": 200,
                                                    "selectable": true,
                                                    "selectConnectedEdges": true,
                                                    "multiselect": true,
                                                    "navigationButtons": true,
                                                    "keyboard": true,
                                                    "highlightNearest": true
                                                }},
                                                "nodes": {{
                                                    "font": {{
                                                        "size": {node_font_size},
                                                        "face": "Arial",
                                                        "color": "{label_color}",
                                                        "strokeWidth": 3,
                                                        "strokeColor": "{base_bg_color}"
                                                    }},
                                                    "shape": "dot"
                                                }},
                                                "edges": {{
                                                    "smooth": {{
                                                        "type": "continuous",
                                                        "forceDirection": "none"
                                                    }},
                                                    "selectionWidth": 2.5
                                                }},
                                                "physics": {{
                                                    "enabled": {str(not disable_physics).lower()},
                                                    "stabilization": {{
                                                        "enabled": true,
                                                        "iterations": {stabilization_iterations},
                                                        "updateInterval": 50
                                                    }},
                                                    "barnesHut": {{
                                                        "gravitationalConstant": -10000,
                                                        "centralGravity": 0.2,
                                                        "springLength": {90 + spacing_distance},
                                                        "springConstant": 0.04,
                                                        "damping": 0.09,
                                                        "avoidOverlap": 0.2
                                                    }}
                                                }}
                                            }}
                                            """
                                            net.set_options(options_json)

                                            try:
                                                if use_community and G_viz.number_of_nodes() > 300:
                                                    from networkx.algorithms import community as nx_comm
                                                    comms = list(nx_comm.greedy_modularity_communities(G_viz))
                                                    for i, comm in enumerate(comms):
                                                        if len(comm) > 25:
                                                            nodes_list = list(comm)
                                                            try:
                                                                net.cluster(nodes=nodes_list)
                                                            except Exception:
                                                                pass
                                            except Exception:
                                                pass

                                            path = os.path.join(os.getcwd(), "pyvis_graph.html")
                                            net.save_graph(path)

                                            try:
                                                with open(path, 'r', encoding='utf-8') as f:
                                                    source_code = f.read()
                                            except Exception:
                                                with open(path, 'r', encoding='utf-8') as f:
                                                    source_code = f.read()

                                            render_html = source_code

                                        if render_html:
                                            autor_focus = autor_pref if autor_pref in G_viz.nodes() else None
                                            viz_state = {
                                                "graph": G_viz,
                                                "render_html": render_html,
                                                "gexf": gexf_data_viz,
                                                "nodes_excel": excel_nodes_viz,
                                                "edges_excel": excel_edges_viz,
                                                "pdf": pdf_output,
                                                "spacing": spacing_distance,
                                                "use_community": use_community,
                                                "show_arrows": show_arrows,
                                                "autor_focus": autor_focus,
                                            }
                                            st.session_state["_pyvis_last"] = viz_state
                                            # Flow continues to main render block below...
                                    
                            except Exception as e:
                                import traceback
                                st.error(f"Erro ao gerar viz PyVis: {e}")
                                st.code("".join(traceback.format_exc()))
                    
                    # Exibir última visualização salva
                    viz_state = st.session_state.get("_pyvis_last") if PYVIS_AVAILABLE else None
                    if viz_state is not None and not isinstance(viz_state, dict):
                        viz_state = None
                    if viz_state is not None and viz_state.get("render_html") and not isinstance(viz_state.get("render_html"), str):
                        viz_state = None
                    if viz_state is not None and not isinstance(viz_state.get("graph"), nx.Graph):
                        viz_state = None

                    if viz_state and viz_state.get("render_html"):
                        render_html = viz_state["render_html"]

                        st.markdown("---")
                        st.markdown("##### 📊 Grafo de Relações")

                        # Injetar botões de controle funcionais em azul no HTML
                        # Injetar botões de controle funcionais com estilo nativo
                        control_buttons_html = """
                        <style>
                            .viz-btn {
                                background-color: #0068c9 !important;
                                color: white !important;
                                border: none;
                                padding: 6px 12px;
                                border-radius: 4px;
                                cursor: pointer;
                                font-weight: 600;
                                font-size: 0.85rem;
                                transition: opacity 0.2s;
                                flex: 1;
                                min-width: 100px;
                                text-align: center;
                            }
                            .viz-btn:hover {
                                opacity: 0.9;
                            }
                        </style>
                        <div style="margin-bottom: 15px; display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;">
                            <button onclick="if(window.network){window.network.moveTo({scale: window.network.getScale() * 1.3});}" class="viz-btn">
                                🔍+ Zoom In
                            </button>
                            <button onclick="if(window.network){window.network.moveTo({scale: window.network.getScale() * 0.7});}" class="viz-btn">
                                🔍- Zoom Out
                            </button>
                            <button onclick="if(window.network){window.network.fit();}" class="viz-btn">
                                🔄 Ajustar Tela
                            </button>
                            <button onclick="if(window.network){window.network.moveTo({position: {x: 0, y: 0}});}" class="viz-btn">
                                🎯 Centralizar
                            </button>
                        </div>
                        """

                        # Injetar os botões no HTML do grafo
                        if "<body>" in render_html:
                            render_html = render_html.replace("<body>", f"<body>{control_buttons_html}")
                        else:
                            render_html = control_buttons_html + render_html

                        # Exibir o grafo
                        components.html(render_html, height=750, scrolling=True)

                        # Legenda explicativa
                        st.markdown("""
                        <div style="margin-top: 5px; margin-bottom: 20px; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f8f9fa;">
                            <h5 style="margin: 0 0 10px 0; font-size: 1rem; color: #333;">📖 Legenda da Rede</h5>
                            <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center;">
                                <div style="display: flex; align-items: center;">
                                    <div style="width: 14px; height: 14px; border-radius: 50%; background-color: #59a14f; border: 2px solid #fff; box-shadow: 0 0 3px rgba(0,0,0,0.2); margin-right: 8px;"></div>
                                    <span style="font-size: 0.9rem; color: #555;"><b>Nós (Pontos):</b> Autores / Colaboradores</span>
                                </div>
                                <div style="display: flex; align-items: center;">
                                    <div style="width: 25px; height: 2px; background-color: #888888; margin-right: 8px; position: relative;">
                                        <div style="width: 0; height: 0; border-top: 4px solid transparent; border-bottom: 4px solid transparent; border-left: 6px solid #888888; position: absolute; right: 0; top: -3px;"></div>
                                    </div>
                                    <span style="font-size: 0.9rem; color: #555;"><b>Arestas (Setas):</b> Citações (Quem cita → Citado)</span>
                                </div>
                                <div style="display: flex; align-items: center;">
                                    <div style="display: flex; margin-right: 8px;">
                                        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #E6194B; margin-right: -4px; border: 1px solid #fff;"></div>
                                        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #FFE119; margin-right: -4px; border: 1px solid #fff;"></div>
                                        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #4363D8; border: 1px solid #fff;"></div>
                                    </div>
                                    <span style="font-size: 0.9rem; color: #555;"><b>Cores:</b> Comunidades (Grupos de citação)</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Botões de download
                        st.markdown("##### 📥 Exportar dados")
                        col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
                        with col_dl1:
                            st.download_button(
                                "PDF",
                                data=viz_state.get("pdf", b""),
                                file_name="rede_autores.pdf",
                                mime="application/pdf",
                                key="btn_pdf_dl",
                                use_container_width=True
                            )
                        with col_dl2:
                            st.download_button(
                                "GEXF",
                                data=viz_state.get("gexf", b""),
                                file_name="rede_autores.gexf",
                                mime="application/gexf+xml",
                                key="btn_gexf_dl",
                                use_container_width=True
                            )
                        with col_dl3:
                            st.download_button(
                                "Nós Excel",
                                data=viz_state.get("nodes_excel", b""),
                                file_name="autores_nos.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="btn_nodes_dl",
                                use_container_width=True
                            )
                        with col_dl4:
                            st.download_button(
                                "Arestas Excel",
                                data=viz_state.get("edges_excel", b""),
                                file_name="citacoes_arestas.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="btn_edges_dl",
                                use_container_width=True
                            )
                    else:
                        st.info("Clique em 'GERAR GRAFO' para visualizar a rede de autores.")

            # ========================================
            # TAB 2: ANÁLISE TEXTUAL (NLP)
            # ========================================
            elif selected_adv == "📝 Análise Textual (NLP)":
                st.markdown("### 📝 Análise Textual dos Resumos")
                st.markdown("""
                Visualize as palavras mais frequentes nos resumos do catálogo.
                As palavras comuns sem valor semântico são automaticamente removidas.
                """)

                if not NLP_AVAILABLE:
                    st.error("❌ Módulo de NLP não disponível.")
                else:
                    try:
                        # Coletar todos os resumos
                        resumos = df['resumo'].dropna().astype(str).tolist()
                        resumos = [r for r in resumos if r.strip() and r.strip() not in ['', 'nan', 'None']]

                        if not resumos:
                            st.info("ℹ️ Não há resumos disponíveis para análise.")
                        else:
                            # st.success(f"✅ Analisando **{len(resumos)}** resumos...") # Removido para limpar a UI se desejar, mas vou manter o feedback de contagem simples se não foi pedido para tirar.
                            # O usuário pediu para retirar a info do spacy.
                            
                            # Juntar texto
                            texto_completo = ' '.join(resumos)
                            
                            # Ordem importa: substituir frases maiores primeiro
                            replacements = [
                                (r'\b[Rr][éèe]gis\s+[Bb]onvicino\b', 'Régis_Bonvicino'), 
                                (r'\b[Rr][éèe]gis\b', 'Régis_Bonvicino'), 
                                (r'\b[Bb]onvicino\b', 'Régis_Bonvicino'),
                                (r'\b[Cc]harles\s+[Bb]ernstein\b', 'Charles_Bernstein'),
                                (r'\b[Cc]harles\b', 'Charles_Bernstein'),
                                (r'\b[Bb]ernstein\b', 'Charles_Bernstein'),
                                (r'\b[Oo]dile\s+[Cc]isneros\b', 'Odile_Cisneros'),
                                (r'\b[Oo]dile\b', 'Odile_Cisneros'),
                                (r'\b[Cc]isneros\b', 'Odile_Cisneros'),
                                (r'\b[Pp]oetas?\b', 'poeta(s)'),     
                                (r'\b[Pp]oemas?\b', 'poema(s)'),
                                (r'\b[Ss]ibila\b', 'Sibila'),             
                                (r'\b[Hh]aarlem\b', 'Haarlem'),
                            ]
                            
                            # Palavras a EXCLUIR explicitamente (Regras do Usuário)
                            EXCLUSOES = {
                                'sobre', 'seção', 'destacando', 'destaca', 'apresenta', 'traz', 
                                'autor', 'autores', 'autora', 'autoras', 'texto', 'textos', 'revista', 'obra', 'obras',
                                'parte', 'partes', 'forma', 'formas', 'ser', 'ter', 'estar', 'haver',
                                'artigo', 'ensaio', 'resumo', 'publicação', 'bilíngue', 'paulo',
                                'produção', 'anos', 'apresentação', 'entrevista', 'papel',
                                'carlos', 'livro', 'escrita', 'edição', 'leitura', 'editorial', 'número', 'meio'
                            }

                            final_tokens = []

                            if SPACY_AVAILABLE:
                                # Processamento com Spacy
                                nlp_spacy.max_length = len(texto_completo) + 100000
                                doc = nlp_spacy(texto_completo)
                                
                                for token in doc:
                                    if token.pos_ not in ['NOUN', 'PROPN', 'ADJ']:
                                        continue
                                    
                                    word = token.text.strip()
                                    word_lower = word.lower()
                                    
                                    if word_lower in STOP_WORDS_PT or word_lower in EXCLUSOES or len(word) < 3:
                                        continue
                                        
                                    if word_lower in ['régis', 'regis', 'bonvicino']:
                                        final_tokens.append('Régis Bonvicino')
                                        continue

                                    if word_lower in ['charles', 'bernstein']:
                                        final_tokens.append('Charles Bernstein')
                                        continue
                                        
                                    if word_lower in ['odile', 'cisneros']:
                                        final_tokens.append('Odile Cisneros')
                                        continue

                                    if word_lower in ['poeta', 'poetas']:
                                        final_tokens.append('poeta(s)')
                                        continue

                                    if word_lower in ['poema', 'poemas']:
                                        final_tokens.append('poema(s)')
                                        continue

                                    if word_lower == 'sibila':
                                        final_tokens.append('Sibila')
                                        continue
                                        
                                    if word_lower == 'poesia':
                                        final_tokens.append('poesia')
                                        continue

                                    if word_lower == 'arte':
                                        final_tokens.append('arte')
                                        continue

                                    if token.pos_ == 'PROPN' or list(word)[0].isupper():
                                        final_tokens.append(word)
                                    else:
                                        final_tokens.append(word.lower())

                            else:
                                # Fallback NLTK
                                texto_proc = texto_completo
                                for pattern, repl in replacements:
                                    import re
                                    texto_proc = re.sub(pattern, repl, texto_proc, flags=re.IGNORECASE)
                                
                                tokens = texto_proc.split()
                                for t in tokens:
                                    t_clean = t.strip(string.punctuation)
                                    if not t_clean: continue
                                    
                                    t_lower = t_clean.lower()
                                    
                                    if t_lower in STOP_WORDS_PT or t_lower in EXCLUSOES or len(t_clean) < 3:
                                        continue
                                        
                                    final_tokens.append(t_clean.replace('_', ' '))

                            # Contar frequências
                            freq = Counter(final_tokens)

                            # Controle de quantidade
                            n_palavras = st.slider("Número de palavras a exibir:", 10, 50, 25)

                            # Top palavras
                            top_palavras = freq.most_common(n_palavras)

                            if top_palavras:
                                df_freq = pd.DataFrame(top_palavras, columns=['Palavra', 'Frequência'])

                                # Gráfico de barras
                                fig_freq = px.bar(
                                    df_freq,
                                    x='Frequência',
                                    y='Palavra',
                                    orientation='h',
                                    title='Palavras mais frequentes nos resumos',
                                    color='Frequência',
                                    color_continuous_scale='Blues'
                                )
                                fig_freq.update_layout(yaxis={'categoryorder': 'total ascending'})
                                st.plotly_chart(fig_freq, use_container_width=True)

                                # Tabela de frequências
                                with st.expander("📋 Ver tabela completa de frequências"):
                                    st.dataframe(df_freq, use_container_width=True)

                                # Estatísticas
                                st.markdown("#### 📊 Estatísticas")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Palavras únicas (Conceitos)", len(freq))
                                with col2:
                                    st.metric("Total Considerado", len(final_tokens))

                                # Download
                                excel_freq = UtilsModule.converter_excel(df_freq)
                                st.download_button(
                                    "📥 Baixar frequências (Excel)",
                                    data=excel_freq,
                                    file_name="frequencia_conceitos_resumos.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_freq_excel"
                                )
                            else:
                                st.warning("Não foi possível extrair palavras significativas dos resumos.")

                    except Exception as e:
                        st.error(f"❌ Erro na análise textual: {str(e)}")
                        # Debug em caso de erro no Spacy
                        import traceback
                        st.code(traceback.format_exc())

            # ========================================
            # TAB 3: MATRIZ DE CORRELAÇÃO
            # ========================================
            elif selected_adv == "📊 Matriz de Correlação":
                st.markdown("### 📊 Matriz de Correlação: Gêneros × Palavras-chave")
                st.markdown("""
                Visualização: tipos textuais (vocabulário controlado) associados às palavras-chave
                """)

                if not SEABORN_AVAILABLE or not MATPLOTLIB_AVAILABLE:
                    st.error("❌ Bibliotecas `seaborn` e/ou `matplotlib` não disponíveis.")
                else:
                    try:
                        # Construir matriz de co-ocorrência
                        generos = []
                        palavras_chave_todas = []

                        for _, row in df.iterrows():
                            genero = row.get('vocabulario_controlado', '')
                            pcs = row.get('palavras_chave', [])
                            if genero and isinstance(pcs, list) and pcs:
                                for pc in pcs:
                                    if pc:
                                        generos.append(str(genero).strip())
                                        palavras_chave_todas.append(str(pc).strip())

                        if not generos or not palavras_chave_todas:
                            st.info("ℹ️ Não há dados suficientes para gerar a matriz. Verifique se existem registros com vocabulário controlado E palavras-chave.")
                        else:
                            # Criar DataFrame de co-ocorrências
                            df_cooc = pd.DataFrame({'genero': generos, 'palavra_chave': palavras_chave_todas})

                            # Contar co-ocorrências
                            matriz = pd.crosstab(df_cooc['genero'], df_cooc['palavra_chave'])

                            # Filtrar para mostrar apenas as mais frequentes
                            n_generos = st.slider("Número de gêneros a exibir:", 5, 20, 10, key="slider_generos")
                            n_palavras_chave = st.slider("Número de palavras-chave a exibir:", 5, 30, 15, key="slider_pc")

                            # Top gêneros e palavras-chave por frequência total
                            top_generos = matriz.sum(axis=1).nlargest(n_generos).index.tolist()
                            top_pcs = matriz.sum(axis=0).nlargest(n_palavras_chave).index.tolist()

                            matriz_filtrada = matriz.loc[top_generos, top_pcs]

                            if matriz_filtrada.empty:
                                st.warning("Matriz vazia após filtragem.")
                            else:
                                # Criar heatmap com matplotlib/seaborn
                                fig, ax = plt.subplots(figsize=(12, 8))
                                sns.heatmap(
                                    matriz_filtrada,
                                    annot=True,
                                    fmt='d',
                                    cmap='Blues',
                                    ax=ax,
                                    cbar_kws={'label': 'Frequência'}
                                )
                                ax.set_xlabel('Palavras-chave', fontsize=12)
                                ax.set_ylabel('Gênero/Tipo Textual', fontsize=12)
                                ax.set_title('Correlação entre Gêneros e Palavras-chave', fontsize=14)
                                plt.xticks(rotation=45, ha='right')
                                plt.yticks(rotation=0)
                                plt.tight_layout()

                                st.pyplot(fig)
                                plt.close()

                                # Estatísticas
                                st.markdown("#### 📊 Estatísticas da Matriz")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Gêneros únicos", len(matriz.index))
                                with col2:
                                    st.metric("Palavras-chave únicas", len(matriz.columns))
                                with col3:
                                    st.metric("Associações totais", len(df_cooc))

                                # Download matriz
                                matriz_final = matriz_filtrada.reset_index().rename(columns={
                                    'genero': 'Tipo Textual',
                                    'palavra_chave': 'Palavras-chave'
                                })
                                excel_matriz = UtilsModule.converter_excel(matriz_final)
                                st.download_button(
                                    "📥 Baixar matriz (Excel)",
                                    data=excel_matriz,
                                    file_name="matriz_generos_palavras_chave.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_matriz_excel"
                                )

                    except Exception as e:
                        st.error(f"❌ Erro ao gerar matriz de correlação: {str(e)}")

            # ========================================
            # TAB 4: DNA DAS EDIÇÕES (RADAR CHART)
            # ========================================
            elif selected_adv == "🧬 DNA das Edições":
                st.markdown("### 🧬 Perfil Estrutural das Edições")
                st.markdown("""
                Compare as características estruturais de diferentes números da Sibila.
                O gráfico abaixo traça uma 'impressão digital' baseada em 4 dimensões:
                
                *   **Internacionalização**: Proporção de textos em língua estrangeira ou com segundo idioma.
                *   **Tradução**: Proporção de textos que envolvem tradução.
                *   **Visualidade**: Densidade de imagens por artigo (normalizada).
                *   **Ensaísmo**: Proporção de textos classificados como 'Ensaio' ou 'Crítica'.
                """)
                
                try:
                    import plotly.graph_objects as go
                    
                    # Preparar dados por edição
                    revistas_unicas = sorted(list(set(df['n'].dropna().astype(str).unique())), 
                                           key=lambda x: ORDEM_SIBILA.index(x) if x in ORDEM_SIBILA else 999)
                    
                    dados_radar = []
                    
                    # Calcular métricas para todas as revistas para normalizar visualidade
                    max_visualidade_dataset = 0
                    temp_metrics = {}

                    for rev in revistas_unicas:
                        df_rev = df[df['n'].astype(str) == rev]
                        if df_rev.empty: continue
                        
                        total_items = len(df_rev)
                        
                        # 1. Internacionalização
                        # Idioma 1 diferente de POR ou PRESENÇA de idioma 2
                        internac_count = df_rev[
                            (df_rev['idioma_01'].str.upper() != 'POR') | 
                            (df_rev['idioma_02'].notna() & (df_rev['idioma_02'] != ''))
                        ].shape[0]
                        score_internac = (internac_count / total_items) * 100
                        
                        # 2. Tradução
                        # Lista de tradutores não vazia
                        traducao_count = df_rev[df_rev['tradutores'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)].shape[0]
                        score_traducao = (traducao_count / total_items) * 100
                        
                        # 3. Visualidade (Densidade)
                        # Total de ícones / Total de artigos
                        total_icones = df_rev['iconografias'].apply(lambda x: len(x) if isinstance(x, list) else 0).sum()
                        density_visual = total_icones / total_items
                        if density_visual > max_visualidade_dataset:
                            max_visualidade_dataset = density_visual
                            
                        # 4. Ensaísmo vs Poesia
                        # Contar 'Ensaio', 'Crítica', 'Resenha' vs Tudo
                        ensaios_count = df_rev[
                            df_rev['vocabulario_controlado'].astype(str).str.upper().str.contains('ENSAIO|CRÍTICA|RESENHA|ENTREVISTA')
                        ].shape[0]
                        score_ensaismo = (ensaios_count / total_items) * 100
                        
                        temp_metrics[rev] = {
                            'Internacionalização': score_internac,
                            'Tradução': score_traducao,
                            'Raw_Visualidade': density_visual,
                            'Ensaísmo': score_ensaismo
                        }
                        
                    # Seletor de revistas
                    opcoes_padrao = revistas_unicas[:3] if len(revistas_unicas) >= 3 else revistas_unicas
                    revistas_selecionadas = st.multiselect(
                        "Selecione as edições para comparar:",
                        revistas_unicas,
                        default=opcoes_padrao
                    )
                    
                    if not revistas_selecionadas:
                        st.warning("Selecione pelo menos uma revista.")
                    else:
                        fig = go.Figure()
                        
                        # Dados para exportação
                        export_data = []
                        
                        # Variável para rastrear o valor máximo e ajustar a escala
                        max_valor_encontrado = 0
                        
                        for rev in revistas_selecionadas:
                            metrics = temp_metrics.get(rev)
                            if not metrics: continue
                            
                            # Normalizar visualidade (0-100 relativo ao máximo do dataset)
                            norm_visualidade = (metrics['Raw_Visualidade'] / max_visualidade_dataset * 100) if max_visualidade_dataset > 0 else 0
                            
                            valores = [
                                metrics['Internacionalização'],
                                metrics['Tradução'],
                                norm_visualidade,
                                metrics['Ensaísmo'],
                                metrics['Internacionalização'] # Fechar o ciclo
                            ]
                            
                            # Atualizar máximo para escala dinâmica
                            local_max = max(valores)
                            if local_max > max_valor_encontrado:
                                max_valor_encontrado = local_max
                            
                            categorias = ['Internacionalização', 'Tradução', 'Visualidade', 'Ensaísmo', 'Internacionalização']
                            
                            fig.add_trace(go.Scatterpolar(
                                r=valores,
                                theta=categorias,
                                fill='toself',
                                name=f'Revista {rev}'
                            ))

                            # Coletar dados para tabela de exportação
                            export_data.append({
                                'Revista': rev,
                                'Internacionalização (%)': round(metrics['Internacionalização'], 2),
                                'Tradução (%)': round(metrics['Tradução'], 2),
                                'Ensaísmo (%)': round(metrics['Ensaísmo'], 2),
                                'Visualidade (Índice Bruto)': round(metrics['Raw_Visualidade'], 4),
                                'Visualidade (Normalizada 0-100)': round(norm_visualidade, 2)
                            })
                            
                        # Definir teto da escala com margem de 10%
                        teto_escala = max_valor_encontrado * 1.1 if max_valor_encontrado > 0 else 100
                        # Se o teto for muito baixo (ex: < 1), forçar um mínimo para não quebrar visualizacao
                        if teto_escala < 1: teto_escala = 1
                            
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, teto_escala]
                                )
                            ),
                            showlegend=True,
                            title={
                                'text': "Perfil Estrutural das Edições",
                                'y':0.95,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'
                            },
                            height=850, # Aumentado conforme solicitado
                            width=1000,
                            margin=dict(l=80, r=80, t=100, b=80)
                        )
                        
                        # Configuração da barra de ferramentas para permitir download SVG/PNG
                        st.plotly_chart(fig, use_container_width=True, config={
                            'toImageButtonOptions': {
                                'format': 'svg', # SVG é vetorial, ideal para "PDF" ou alta qualidade
                                'filename': 'dna_sibila_radar',
                                'height': 850,
                                'width': 1000,
                                'scale': 2 # Alta resolução
                            },
                            'displayModeBar': True,
                            'displaylogo': False
                        })
                        
                        st.caption(f"*Visualidade normalizada relativa à edição mais visual (Max Densidade: {max_visualidade_dataset:.2f} img/artigo)")

                        # Botões de Exportação dos Dados
                        if export_data:
                            st.markdown("### 📥 Exportar Dados do Gráfico")
                            df_export_radar = pd.DataFrame(export_data)
                            
                            col_rad1, col_rad2 = st.columns(2)
                            
                            # Excel (Única opção agora)
                            try:
                                excel_radar = UtilsModule.converter_excel(df_export_radar)
                                col_rad1.download_button(
                                    "📊 Baixar Dados (Excel)",
                                    data=excel_radar,
                                    file_name="dna_sibila_dados.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="btn_radar_excel_export"
                                )
                            except Exception as e:
                                col_rad1.warning(f"Excel indisponível: {e}")

                except Exception as e:
                    st.error(f"❌ Erro ao gerar Radar Chart: {str(e)}")

    # --- DIÁRIO DE PESQUISA ---
    elif menu == "DIÁRIO DE PESQUISA":
        st.title("📝 DIÁRIO DE PESQUISA – PROJETO SIBILA")
        diario = PersistenceModule.load_diario()
        with st.expander("➕ Registrar nova entrada no diário", expanded=True):
            with st.form("form_diario_geral"):
                titulo = st.text_input("Título da entrada")
                texto = st.text_area("Texto da entrada", height=160)
                tags = st.text_input("Tags (separadas por vírgula)")
                reg_ops = []
                reg_ids = []
                for r in dados:
                    label = f"{r.get('n','?')} | Reg: {r.get('registro','?')} | {r.get('titulo_artigo','[sem título]')}"
                    reg_ops.append(label)
                    reg_ids.append(r.get('_id'))
                registros_sel = st.multiselect(
                    "Vincular a registros específicos (opcional)", reg_ops
                )
                if st.form_submit_button("💾 Salvar entrada no diário"):
                    if texto.strip():
                        vinc_ids = [
                            reg_ids[reg_ops.index(lbl)] for lbl in registros_sel
                        ]
                        entrada = {
                            "id": str(int(datetime.now().timestamp() * 1000)),
                            "data": datetime.now().isoformat(),
                            "titulo": titulo.strip() or "[sem título]",
                            "texto": texto.strip(),
                            "tags": [t.strip() for t in tags.split(',') if t.strip()],
                            "registros_relacionados": vinc_ids
                        }
                        diario.append(entrada)
                        if PersistenceModule.save_diario(diario):
                            st.success("Entrada adicionada ao diário.")
                    else:
                        st.warning("O texto da entrada não pode estar vazio.")

        st.markdown("---")
        st.subheader("Entradas registradas")
        if not diario:
            st.info("Nenhuma entrada registrada ainda.")
        else:
            tags_existentes = sorted(
                list(
                    set(
                        t
                        for d in diario
                        for t in d.get('tags', [])
                    )
                )
            )
            c1, c2 = st.columns([1, 2])
            with c1:
                tag_filtro = st.multiselect("Filtrar por tags", tags_existentes)
            with c2:
                ordem = st.selectbox("Ordenar por", ["Mais recentes primeiro", "Mais antigas primeiro"])

            entradas = diario.copy()
            entradas = sorted(
                entradas,
                key=lambda x: x.get('data', ''),
                reverse=(ordem == "Mais recentes primeiro")
            )
            if tag_filtro:
                entradas = [
                    e for e in entradas
                    if any(t in e.get('tags', []) for t in tag_filtro)
                ]

            for e in entradas:
                dt = e.get('data', '')[:16].replace("T", " ")
                st.markdown(
                    f"""
                    <div class="nelic-card">
                        <div class="nelic-card-header">{e.get('titulo','[sem título]')}</div>
                        <div class="nelic-card-subtitle">Data: {dt}</div>
                        <div class="nelic-muted">{e.get('texto','')}</div>
                        <div style="margin-top:0.4rem;">
                    """,
                    unsafe_allow_html=True
                )
                if e.get('tags'):
                    st.markdown(
                        " ".join(
                            [f"<span class='nelic-tag nelic-tag-muted'>{t}</span>" for t in e['tags']]
                        ),
                        unsafe_allow_html=True
                    )
                if e.get('registros_relacionados'):
                    st.markdown("<br><span class='nelic-muted'>Registros vinculados:</span>", unsafe_allow_html=True)
                    labels = []
                    for reg_id in e.get('registros_relacionados', []):
                        r = UtilsModule.get_registro_by_id(dados, reg_id)
                        if r:
                            labels.append(
                                f"{r.get('n','?')} | Reg: {r.get('registro','?')} | {r.get('titulo_artigo','[sem título]')}"
                            )
                    if labels:
                        st.markdown(
                            "<br>".join(labels),
                            unsafe_allow_html=True
                        )
                st.markdown("</div>", unsafe_allow_html=True)

    # --- METODOLOGIA ---
    elif menu == "METODOLOGIA":
        st.title("📚 METODOLOGIA NELIC")

        st.markdown("""
        <div class="info-box">
        <p><strong>Sistema NELIC</strong> é uma ferramenta de catalogação bibliográfica especializada,
        desenvolvida para documentação sistemática de periódicos literários. Este sistema implementa
        a metodologia NELIC de indexação para a catalogação de arquivos, auxiliando em análises e
        reflexões críticas sobre a produção cultural e literária.</p>
        </div>
        """, unsafe_allow_html=True)


        selected_metod = option_menu(
            menu_title=None,
            options=["📝 Catalogação", "🔍 Busca e Exploração", "📊 Análises e Relatórios", "🎓 Metodologia Detalhada", "💡 Dicas de Uso", "🚀 Potencialidades e Usos"],
            icons=["pencil-square", "search", "graph-up", "book", "lightbulb", "rocket"],
            orientation="horizontal",
            key="metodologia_menu"
        )
        
        if selected_metod == "📝 Catalogação":
            st.markdown("### 📝 GUIA DE CATALOGAÇÃO")

            st.markdown("""
            <div class="metod-section">
            <h4>Editor de Registros</h4>
            <p>O editor permite criar novos registros ou editar registros existentes. Cada registro representa
            um texto publicado e deve conter informações bibliográficas completas.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Campos do Formulário de Catalogação")

            st.markdown("""
            <div class="metod-section">
            <h4>1. IDENTIFICAÇÃO BÁSICA</h4>
            <p><em>Campos obrigatórios marcados com asterisco (*)</em></p>
            <ul>
                <li><strong>Nº REVISTA:</strong> Número da edição da revista (0 a 12)</li>
                <li><strong>REGISTRO:</strong> Código único de identificação</li>
                <li><strong>PÁGINAS:</strong> Intervalo de páginas (exemplo: 45-48)</li>
                <li><strong>ORDEM:</strong> Número de ordem de exibição no sistema</li>
                <li><strong>IDIOMAS:</strong> Idioma primário e secundário (se bilíngue)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>2. TIPO TEXTUAL (Sistema Hierárquico)</h4>
            <p>O sistema utiliza classificação em <strong>dois níveis</strong>:</p>

            <p><strong>TIPOS PRINCIPAIS:</strong></p>
            <ul>
                <li>POEMA(S) - não exige resumo</li>
                <li>ENSAIO - exige resumo analítico</li>
                <li>RESENHA - exige resumo analítico</li>
                <li>ENTREVISTA - exige resumo analítico</li>
                <li>FICÇÃO - não exige resumo</li>
                <li>EDITORIAL</li>
                <li>APRESENTAÇÃO</li>
                <li>REPORTAGEM</li>
                <li>CARTAS DO LEITOR</li>
                <li>E outros</li>
            </ul>

            <p><strong>SUBTIPOS (Campo disciplinar):</strong></p>
            <p>Alguns tipos principais permitem especificação disciplinar:</p>
            <ul>
                <li>ENSAIO: Literatura, Filosofia, História, Linguística, etc.</li>
                <li>RESENHA: Literatura, Antropologia, Sociologia, etc.</li>
                <li>ENTREVISTA: Literatura</li>
                <li>INFORME: Literatura</li>
            </ul>
            <p><strong>Exemplo:</strong> ENSAIO - Filosofia</p>
            <p><strong>⚠️ ATENÇÃO:</strong> O sistema valida automaticamente se o tipo textual exige resumo analítico.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>3. TÍTULOS E NOTAS</h4>
            <p><strong>TÍTULO (obrigatório):</strong></p>
            <ul>
                <li>Se o texto possui título: transcreva fielmente</li>
                <li>Se poema sem título: insira primeiro verso entre aspas e reticências
                    <br>Exemplo: "não penses enquanto passa (…)"</li>
                <li>Se prosa sem título: reproduza as 4-5 primeiras palavras</li>
            </ul>

            <p><strong>SUBTÍTULO:</strong> Caso exista</p>

            <p><strong>NOTA DE EDIÇÃO:</strong> Informações editoriais importantes</p>
            <ul>
                <li>[publicação bilíngue]</li>
                <li>[tradução do inglês]</li>
                <li>[texto republicado de...]</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>4. RESPONSABILIDADE AUTORAL</h4>
            <p><strong>FORMATO ABNT (automático):</strong> O sistema converte automaticamente para SOBRENOME, Prenomes</p>

            <p><strong>Exemplos:</strong></p>
            <ul>
                <li>Digite: Régis Bonvicino → Sistema salva: BONVICINO, Régis</li>
                <li>Digite: Claudio Daniel → Sistema salva: DANIEL, Claudio</li>
            </ul>

            <p><strong>COLABORADORES:</strong> Autores do texto (um por linha)</p>
            <p><strong>TRADUTORES:</strong> Se aplicável (um por linha)</p>
            <p><strong>💡 Dica:</strong> Digite um nome por linha ou separe por vírgulas</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>5. ASSUNTOS E INDEXAÇÃO</h4>
            <p><strong>AUTORES CITADOS:</strong> Autores mencionados no texto (um por linha)</p>
            <ul>
                <li>Use para mapear referências bibliográficas</li>
                <li>Importante para análise de redes intelectuais</li>
            </ul>

            <p><strong>PALAVRAS-CHAVE:</strong> Use APENAS termos do Vocabulário Controlado</p>
            <ul>
                <li>Lista pré-estabelecida de 400+ termos</li>
                <li>Garante consistência nas buscas</li>
                <li>Exemplos: Poesia, Modernismo, Vanguarda, Literatura Brasileira</li>
            </ul>

            <p><strong>NOME PESSOAL COMO ASSUNTO:</strong> Pessoas que são tema principal</p>
            <ul>
                <li>Use para biografias, homenagens, estudos críticos</li>
                <li>Exemplo: texto sobre Drummond → ANDRADE, Carlos Drummond de</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>6. RESUMO ANALÍTICO</h4>
            <p><strong>⚠️ OBRIGATÓRIO PARA:</strong></p>
            <ul>
                <li>ENSAIO</li>
                <li>RESENHA</li>
                <li>ENTREVISTA</li>
                <li>REPORTAGEM</li>
                <li>EDITORIAL (com conteúdo analítico)</li>
                <li>APRESENTAÇÃO</li>
                <li>DEBATE</li>
            </ul>

            <p><strong>NÃO EXIGIDO PARA:</strong></p>
            <ul>
                <li>POEMA(S)</li>
                <li>FICÇÃO</li>
                <li>CAPA</li>
                <li>IMAGENS</li>
                <li>HQ/CHARGE</li>
            </ul>

            <p><strong>Como escrever:</strong> Síntese crítica do conteúdo (150-300 palavras)</p>
            <ul>
                <li>Tema central</li>
                <li>Argumentos principais</li>
                <li>Conclusões ou posições defendidas</li>
            </ul>

            <p><strong>Nota:</strong> O sistema valida automaticamente e impede salvar se resumo estiver ausente quando obrigatório.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="metod-section">
            <h4>7. ICONOGRAFIA</h4>
            <p>Documentação sistemática de elementos visuais:</p>

            <p><strong>TIPOS:</strong></p>
            <ul>
                <li>Foto</li>
                <li>Ilustração</li>
                <li>Reprodução (de obra de arte)</li>
                <li>Fac-símile</li>
                <li>Cartografia</li>
                <li>Gráfico/Tabela</li>
                <li>HQ/Charge</li>
                <li>Fotograma</li>
                <li>Publicidade</li>
            </ul>

            <p><strong>DESCRIÇÃO:</strong> Título da obra, créditos, data</p>
            <p><strong>Exemplo:</strong></p>
            <ul>
                <li>Tipo: Foto</li>
                <li>Descrição: "Retrato de João Cabral de Melo Neto. Foto: Arquivo Nacional, 1960"</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        elif selected_metod == "🔍 Busca e Exploração":
            st.markdown("### 🔍 Busca e Exploração")

            st.markdown("""
            <div class="metod-section">
            <p>A busca e a exploração de dados no sistema NELIC de indexação se organizam em torno de uma ideia simples:
            qualquer consulta começa pela definição de um recorte dentro do conjunto de registros catalogados. Esse recorte
            pode ser temporal (período, fascículos, volumes), formal (tipologia dos textos), linguístico (idiomas envolvidos),
            autoral (quem escreve, quem é citado), temático (palavras-chave) ou material (presença de iconografia).</p>

            <p>O sistema NELIC de indexação funciona sempre sobre a mesma base de dados estruturada, em que cada texto possui
            campos definidos (idioma, vocabulário controlado, autores colaboradores, autores citados, palavras-chave, iconografia,
            páginas, entidade coletiva, entre outros). A busca consiste em selecionar combinações desses campos para obter
            subconjuntos coerentes. Alguns exemplos de recortes possíveis:</p>

            <ul>
                <li>textos de um determinado período e de um único tipo textual, como "ensaios entre 2001 e 2002";</li>
                <li>textos em mais de um idioma, de modo a isolar publicações bilíngues;</li>
                <li>textos que tenham uma palavra-chave específica, como "modernismo" ou "tradução";</li>
                <li>textos em que um determinado nome aparece como autor colaborador, como autor citado ou como "nome pessoal como assunto".</li>
            </ul>

            <p>No caso de recortes temporais, como "ensaios entre 2001 e 2002", o sistema não possui um filtro direto por ano.
            O procedimento depende do mapeamento entre ano e número da revista: é necessário saber quais números correspondem
            a 2001 e 2002 e, em seguida, selecionar esses números no filtro de "Revista" da aba EXPLORAR DADOS, combinando
            com o tipo textual "Ensaio".</p>

            <p>A lógica é cumulativa: ao combinar critérios de tipologia, idioma, palavra-chave e autoria, o sistema reduz
            progressivamente o universo de registros até chegar a um conjunto bem delimitado. Um recorte como "ensaios em espanhol
            sobre cultura que citam determinado teórico" pode ser trabalhado, na prática, da seguinte forma: na aba EXPLORAR DADOS,
            selecionar "Ensaio" em "Tipo Textual", escolher "Cultura" (ou o termo temático mais próximo disponível) no campo de
            "Palavras-Chave" e inserir o sobrenome do teórico no campo de "Busca Livre (Título/Resumo)". Essa busca livre percorre
            também colunas textuais internas, de modo que registros em que o teórico apareça como autor citado tendem a ser recuperados.
            Como não há filtro específico por idioma nessa tela, a etapa "em espanhol" exige um passo adicional: depois de obter o
            conjunto de ensaios com aquele tema e aquele teórico, basta exportar os resultados para Excel e filtrar, na planilha,
            a coluna de idioma pela sigla correspondente (por exemplo, "ESP" para espanhol).</p>

            <p>O resultado típico de uma busca é uma lista tabular de registros, em que cada linha corresponde a um texto e cada
            coluna a um campo relevante (título, autores, tipo textual, idiomas, páginas, palavras-chave, presença de iconografia).
            A partir dessa lista, já é possível observar padrões simples, como a concentração de um mesmo autor em determinado período,
            a recorrência de certas palavras-chave em tipos textuais específicos ou a distribuição da iconografia ao longo de uma coleção.</p>

            <p>Essa etapa de busca e exploração funciona como momento de delimitação do corpus para análises posteriores. A qualidade
            desse trabalho depende diretamente da consistência da catalogação: quanto mais rigorosamente os campos forem preenchidos,
            mais precisos se tornam os recortes possíveis.</p>
            </div>
            """, unsafe_allow_html=True)


        elif selected_metod == "📊 Análises e Relatórios":
            st.markdown("### 📊 Análise e Relatórios")

            st.markdown("""
            <div class="metod-section">
            <p>A etapa de análise trabalha com os mesmos registros catalogados, mas desloca o foco da descrição individual de
            cada texto para a observação de distribuições, frequências e proporções. Em vez de perguntar "quais textos satisfazem
            determinado critério?", passa-se a perguntar "como os dados se distribuem dentro de um critério ou combinação de critérios?".</p>

            <p>O sistema NELIC de indexação calcula, a partir dos campos preenchidos, tabelas de frequência e percentuais. Alguns
            exemplos de saídas possíveis:</p>

            <ul>
                <li>distribuição dos tipos textuais no conjunto: quantos ensaios, resenhas, poemas, entrevistas, ficções, editoriais etc.,
                    em números absolutos e em porcentagem;</li>
                <li>lista de autores colaboradores com o número de textos publicados e sua participação relativa no total;</li>
                <li>lista de autores citados, ordenada por número de ocorrências, o que permite mapear redes de referência e campos teóricos predominantes;</li>
                <li>distribuição de palavras-chave mais recorrentes, indicando temas estruturantes do corpus;</li>
                <li>proporção de textos com iconografia em relação ao total, bem como variações dessa proporção em diferentes recortes
                    (por período, por tipo textual, por idioma, quando esses dados forem combinados com filtros e exportações).</li>
            </ul>

            <p>Quando a análise é feita sobre um recorte previamente delimitado na busca (por exemplo, "todos os ensaios de um certo período"),
            as tabelas e proporções dizem respeito apenas a esse subconjunto. Isso permite, por exemplo, comparar os autores mais citados em
            ensaios com os autores mais citados em resenhas, ou a distribuição de idiomas em textos críticos em relação à distribuição em
            textos criativos.</p>

            <p>Os resultados podem ser organizados em tabelas simples com as colunas "valor" (por exemplo, o nome do autor ou da palavra-chave),
            "frequência absoluta" e "percentual no conjunto analisado". A mesma informação pode ser representada em gráficos de barras que
            facilitam a identificação de concentrações, ausências e deslocamentos.</p>

            <p>Além da visualização dentro do sistema, as análises podem ser exportadas em formatos adequados ao trabalho de pesquisa. Em
            planilhas, o pesquisador pode reorganizar, filtrar e combinar as tabelas com outros dados. Em relatórios em PDF, os resultados
            podem ser incorporados diretamente a projetos, artigos e capítulos, documentando com clareza os critérios utilizados e os números obtidos.</p>
            </div>
            """, unsafe_allow_html=True)


        elif selected_metod == "🎓 Metodologia Detalhada":
            st.markdown("### 🎓 Metodologia Detalhada")

            st.markdown("""
            <div class="metod-section">
            <p>A metodologia do sistema de catalogação parte da definição de um conjunto de campos que precisam ser preenchidos de
            maneira uniforme. Cada campo corresponde a um aspecto do texto e pode ser posteriormente utilizado como critério de busca
            ou de análise. O preenchimento cuidadoso desses campos é a base de toda a exploração posterior.</p>

            <p><strong>Alguns campos centrais:</strong></p>

            <h4>Identificação básica</h4>
            <p>Inclui número ou código do fascículo, ordem de exibição do texto dentro da coleção, intervalo de páginas e registro único.
            Esses dados permitem localizar o texto fisicamente e reconstruir a organização interna de cada número.</p>

            <h4>Idiomas</h4>
            <p>Registra o idioma principal do texto e, quando pertinente, um segundo idioma em caso de traduções ou publicações bilíngues.
            O uso de siglas padronizadas (POR, ESP, ING, ITA etc.) evita ambiguidades e facilita contagens posteriores de distribuição linguística.</p>

            <h4>Entidade coletiva e autoria</h4>
            <p>Quando um texto não é atribuído a um indivíduo, o campo "entidade coletiva" indica a responsabilidade institucional (por exemplo,
            a própria revista ou um grupo editorial). Nos demais casos, os "autores colaboradores" são listados com nome normalizado em formato
            padrão (sobrenome em maiúsculas, seguido do prenome). Em entrevistas, tanto entrevistador(es) quanto entrevistado(a) são incluídos,
            de modo que a busca por qualquer um deles recupere o registro.</p>

            <h4>Tradutor</h4>
            <p>Sempre que houver tradução, o tradutor é identificado pelo nome completo. Nos casos em que a tradução é mencionada sem crédito,
            registra-se essa condição (por exemplo, "sem crédito") para não deixar o campo vazio e, ao mesmo tempo, não atribuir autoria inexistente.</p>

            <h4>Título, subtítulo e resumo</h4>
            <p>O título é transcrito conforme aparece no texto, com regras específicas para poemas ou textos em prosa sem título, em que se
            utilizam versos ou primeiras palavras como forma de identificação. O subtítulo, quando existe, complementa o título e pode reunir
            dados adicionais, como informações sobre obras resenhadas. O resumo oferece uma descrição concisa do conteúdo em textos de caráter
            analítico (ensaios, resenhas, entrevistas, reportagens, apresentações) e é dispensado em textos ficcionais ou poéticos. Notas
            complementares, informações de publicação original ou peculiaridades de autoria são acrescentadas entre colchetes.</p>

            <h4>Vocabulário controlado (tipologia)</h4>
            <p>Cada texto recebe uma categoria de tipo textual, escolhida a partir de uma lista limitada e previamente definida. Entre as
            possibilidades estão apresentação, poema, resenha, reportagem, cartas do leitor, correspondência, depoimento, entrevista, ficção,
            editorial, informe, HQ/charge, ensaio, entre outras. Em alguns casos, acrescenta-se um segundo termo para indicar a área disciplinar
            (por exemplo, ensaio – filosofia; resenha – literatura). Essa solução permite cruzar forma textual e campo de conhecimento.</p>

            <h4>Palavras-chave</h4>
            <p>Em textos analíticos, o catalogador seleciona até seis palavras-chave a partir de um vocabulário controlado mais amplo, que
            inclui conceitos, temas, correntes e noções recorrentes. Isso evita variações arbitrárias de grafia e garante comparabilidade entre
            textos. Poemas, ficções, capas, HQs e charges, em geral, não recebem palavras-chave temáticas para preservar a especificidade de
            seu registro.</p>

            <h4>Nome pessoal como assunto</h4>
            <p>Esse campo é preenchido quando o texto trata diretamente de uma pessoa (autores, artistas, críticos, teóricos), independentemente
            de quem assine o texto. O mesmo nome deve aparecer também entre os autores citados, de modo a permitir pesquisas tanto por "assunto
            pessoa" quanto por "citação".</p>

            <h4>Autores citados</h4>
            <p>Reúne os nomes mencionados ao longo do texto. Não se trata de uma lista bibliográfica completa, mas de um registro dos nomes que
            aparecem como referência ou interlocução. Esse campo é crucial para análises de redes de citação, identificação de cânones críticos
            e mapeamento de referências teóricas.</p>

            <h4>Iconografia</h4>
            <p>Registra a presença de imagens associadas ao texto, classificadas em categorias (cartografia, fac-símile, fotografia, fotograma,
            gráfico/tabela, HQ/charge, ilustração, publicidade, reprodução). Para cada item, descrevem-se título, crédito e data, com convenções
            para casos em que essas informações não estão disponíveis.</p>

            <p><strong>Considerações finais:</strong></p>
            <p>Todos esses campos são simultaneamente descritivos e analíticos. Ao preencher "vocabulário controlado" e "palavras-chave",
            estabelece-se a base para análises temáticas e formais. Ao registrar "autores citados" e "nome pessoal como assunto", cria-se a
            possibilidade de estudar redes de influência. Ao marcar iconografia, torna-se possível discutir o papel das imagens no conjunto.
            O sistema de indexação transforma, assim, o conjunto de textos em um banco de dados preparado para operações comparativas de diferentes ordens.</p>
            </div>
            """, unsafe_allow_html=True)


        elif selected_metod == "💡 Dicas de Uso":
            st.markdown("### 💡 Dicas de Uso")

            st.markdown("""
            <div class="metod-section">
            <p>O sistema de catalogação foi pensado para ser útil tanto em consultas pontuais quanto em pesquisas de fôlego. Algumas
            orientações podem facilitar esse uso.</p>

            <p>Uma primeira etapa consiste em transformar perguntas vagas em recortes claros. Em vez de "quero ver artigos sobre teoria",
            é possível formular questões como "ensaios com palavra-chave teoria" ou "textos em que determinado autor aparece como citado".
            A partir disso, os filtros correspondentes podem ser aplicados de forma mais precisa, em especial na aba EXPLORAR DADOS e nas
            páginas de análise.</p>

            <p>Os cruzamentos de dados tornam-se mais interessantes quando se pensa em pares de campos. Alguns exemplos de perguntas que
            o sistema ajuda a responder, combinando filtros e análises:</p>

            <ul>
                <li>Qual a distribuição de tipos textuais em determinado período da coleção?</li>
                <li>Quais autores colaboradores concentram mais publicações em um intervalo de números de revista?</li>
                <li>Quais autores são mais citados em textos classificados como "ensaio – literatura", e como isso se compara a textos
                    classificados como "ensaio – filosofia"?</li>
                <li>Que palavras-chave aparecem com maior frequência em textos bilíngues, identificados depois na coluna de idiomas?</li>
                <li>Em quais tipos de texto a iconografia é mais utilizada?</li>
            </ul>

            <p>As saídas numéricas (contagens e percentuais) precisam ser lidas sempre em relação ao conjunto considerado. Um mesmo autor
            pode aparecer com um percentual baixo na base completa, mas ser central em um recorte específico. Interpretar a proporção dentro
            de cada recorte é decisivo para não generalizar conclusões.</p>

            <p>Os arquivos exportados em planilha permitem prolongar as análises: calcular médias, criar gráficos personalizados, agrupar
            registros por períodos (aproximados pelos números da revista), comparar duas ou mais coleções. Já os relatórios em PDF são adequados
            para registrar o estado de uma pesquisa em determinado momento, servindo como documento de trabalho e registro dos recortes utilizados.</p>

            <p>O uso continuado do sistema também funciona como revisão da própria catalogação. Consultas que retornam resultados inesperados
            podem revelar inconsistências de preenchimento, diferenças indesejadas de grafia ou campos sem dados em lugares estratégicos. Nesse
            sentido, a exploração não apenas extrai informação analítica, mas retroalimenta o cuidado com o banco de dados, fortalecendo a
            confiabilidade do sistema de indexação como um todo.</p>
            </div>
            """, unsafe_allow_html=True)


        elif selected_metod == "🚀 Potencialidades e Usos":
            st.markdown("### 🚀 Potencialidades de Pesquisa e Usos do Sistema")
            
            st.markdown("""
            <div class="metod-section">
            <p>O Sistema NELIC estrutura a massa textual da revista Sibila em um banco de dados relacional. Essa organização permite superar a leitura linear ou impressionista, habilitando o pesquisador a interrogar o corpus por meio de filtros combinados e projeções gráficas. A ferramenta não substitui a interpretação crítica, mas oferece uma base empírica verificável para testar hipóteses sobre a história intelectual e material da publicação.</p>
            </div>
            
            <div class="metod-section">
            <h4>1. ANÁLISE QUANTITATIVA (Bibliometria)</h4>
            <p>A bibliometria aplicada à revista Sibila objetiva mensurar suas <strong>transformações editoriais</strong>. A contagem sistemática de tipos textuais revela as prioridades de cada fase da publicação. Se nos primeiros números predomina a poesia inédita, a análise dos dados pode indicar se houve um deslocamento progressivo para a crítica ou o ensaio teórico nos anos finais (2006-2007).</p>
            
            <p>A análise de produtividade lança luz sobre a <strong>demografia autoral</strong>, isto é, o perfil coletivo de quem escreve na revista (quem são, de onde vêm e quanto produzem). A aplicação de métricas de frequência distingue o núcleo duro de colaboradores regulares dos participantes esporádicos. Da mesma forma, o mapeamento de idiomas quantifica a <strong>abertura internacional ou a manutenção dos vínculos</strong> locais da revista, permitindo identificar quais tradições linguísticas (inglesa, francesa, hispânica) tiveram maior trânsito nas páginas da Sibila.</p>
            </div>

            <div class="metod-section">
            <h4>2. ANÁLISE DAS REDES (SNA)</h4>
            <p>A Análise das Redes <strong>cartografa</strong> o campo literário em <strong>grafos de conexão</strong> — diagramas visuais que traduzem relações sociais e intelectuais em uma geometria de <strong>pontos (nós, representando os autores)</strong> e <strong>linhas (arestas, representando as citações ou colaborações entre eles)</strong>. O sistema processa as listas de Colaboradores e Autores Citados para desenhar a <strong>estrutura de influência da revista</strong>, revelando explicitamente quais figuras de autoridade (o "cânone interno") sustentam teórica e esteticamente o grupo editorial. Uma rede de citações densa em torno de nomes específicos (como Mallarmé ou João Cabral) demonstra empiricamente essas hierarquias e linhagens.</p>
            
            <p>A rede semântica conecta os artigos pelos seus temas. Isso permite visualizar <strong>agrupamentos ("clusters")</strong> de assuntos, ou seja, núcleos de termos que tendem a orbitar juntos. É possível verificar empiricamente hipóteses complexas, como a associação entre nacionalidade e tema; ao cruzar filtros na aba "Explorar Dados", o pesquisador pode investigar se a palavra-chave "Política", por exemplo, predomina em artigos de autores de uma determinada origem ou se concentra em períodos específicos de crise, transformando a intuição de leitura em evidência estruturada.</p>
            </div>

            <div class="metod-section">
            <h4>3. ANÁLISE QUALITATIVA</h4>
            <p>A indexação estruturada orienta o retorno ao texto para uma leitura atenta (<em>Close Reading</em>). O sistema funciona como um índice remissivo inteligente: o levantamento de frequência de termos apontado na análise quantitativa dirige o olhar do pesquisador para os textos fundamentais. Se os dados mostram uma recorrência estatística de conceitos como "barroco" ou "concreto", o crítico pode selecionar apenas os ensaios que mobilizam esses termos para investigar <em>como</em> eles são definidos, disputados ou ressignificados, definindo o vocabulário teórico que sustenta o projeto editorial.</p>
            
            <p>O índice iconográfico, por sua vez, revela o projeto visual da revista como uma camada de sentido autônoma. Ao classificar cada imagem (Foto, Reprodução, Ilustração), o sistema expõe o investimento em visualidade não como mero adorno, mas como discurso. Uma predominância de reproduções de arte contemporânea em detrimento de fotos documentais, por exemplo, sinaliza uma postura editorial que valoriza a intervenção estética contemporânea sobre o registro histórico ou documental, dado que pode ser cruzado com a análise dos textos sobre arte na mesma edição.</p>
            </div>
            
            <div class="metod-section">
            <h4>4. ESCALAS DE ANÁLISE</h4>
            <p>A ferramenta articula três níveis de observação, permitindo ao pesquisador transitar do detalhe ao panorama sem perder o rigor. No <strong>Nível Macro</strong>, observam-se as séries longas: os movimentos de constância e ruptura de toda a coleção (2001-2007), permitindo testar hipóteses sobre a linha editorial (ex: "a revista tornou-se mais acadêmica com o tempo?"). No <strong>Nível Meso</strong>, examina-se a edição como unidade de sentido (o objeto "revista"): como os textos de poesia e ensaio dialogam dentro do volume duplo 8-9? Há uma coerência interna proposital? No <strong>Nível Micro</strong>, acessa-se a "anatomia" do documento: o dado singular, como a escolha de um tradutor específico para um único poema ou uma nota de rodapé polêmica, elementos que muitas vezes contêm a chave de leitura para as escalas maiores.</p>
            </div>
            """, unsafe_allow_html=True)



    # --- MAIS DADOS ---
    elif menu == "MAIS DADOS":
        st.title("📊 MAIS DADOS - ANÁLISE COMPLETA")
        if not df.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("REGISTROS", len(df))
            c2.metric("COLABORADORES", DataModule.get_normalized_series(df, 'autores_colaboradores').nunique())
            c3.metric("AUTORES CITADOS", DataModule.get_normalized_series(df, 'autores_citados').nunique())
            if 'iconografias' in df.columns:
                n_icon = df['iconografias'].apply(
                    lambda x: 1 if isinstance(x, list) and len(x) > 0 else 0
                ).sum()
                p_icon = (n_icon / len(df)) * 100
                c4.metric("ÍNDICE ICONOGRAFIA", f"{p_icon:.1f}%", help=f"{n_icon} registros contêm iconografia")
            else:
                c4.metric("ÍNDICE ICONOGRAFIA", "0%")

            st.markdown("---")
            st.subheader("📥 EXPORTAR BASE COMPLETA")
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            excel_completo = UtilsModule.converter_excel(df)
            pdf_completo = PDFModule.gerar_pdf_analitico(df, len(df), "Base de dados completa")
            json_completo = json.dumps(dados, ensure_ascii=False, indent=2)
            col_exp1.download_button(
                "📊 EXCEL COMPLETO",
                excel_completo,
                f"sibila_completo_{datetime.now().strftime('%Y%m%d')}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch'
            )
            col_exp2.download_button(
                "📄 PDF COMPLETO",
                pdf_completo,
                f"sibila_completo_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf",
                width='stretch'
            )
            col_exp3.download_button(
                "💾 JSON COMPLETO",
                json_completo,
                f"sibila_completo_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json",
                width='stretch'
            )

            st.markdown("---")
            g1, g2 = st.columns(2)
            with g1:
                s = df['vocabulario_controlado'].apply(
                    lambda x: 'Manifesto' if 'manifesto' in str(x).lower() else (str(x).split(' - ')[0] if isinstance(x, str) else x)
                )
                v = s.value_counts().head(10).reset_index()
                v.columns = ['Tipo', 'Qtd']
                fig = px.bar(v, x='Tipo', y='Qtd', text='Qtd')
                fig.update_layout(title="DISTRIBUIÇÃO POR TIPO TEXTUAL", height=380)
                st.plotly_chart(fig, width='stretch')
            with g2:
                r = df['n'].value_counts().reset_index()
                r.columns = ['Revista', 'Qtd']
                fig2 = px.bar(
                    r.sort_values('Revista'),
                    x='Revista',
                    y='Qtd',
                    text='Qtd'
                )
                fig2.update_layout(title="REGISTROS POR REVISTA", height=380)
                fig2.update_xaxes(type='category', tickmode='linear')
                st.plotly_chart(fig2, width='stretch')

            st.markdown("---")

            selected_mais_dados = option_menu(
                menu_title=None,
                options=["PALAVRAS-CHAVE", "AUTORES CITADOS", "COLABORADORES", "TRADUTORES"],
                icons=["chat-quote", "people", "person-badge", "translate"],
                orientation="horizontal",
                key="mais_dados_menu"
            )
            
            def show_stats_with_export(col, label, tab_key):
                s = DataModule.get_normalized_series(df, col)
                if s.empty:
                    st.info(f"Sem dados de {label.lower()}.")
                    return
                counts = UtilsModule.calculate_stats_with_percentage(s)
                df_export = counts.rename(
                    columns={'Termo': 'Campo', 'Qtd': 'Num. Absoluto', '%': 'Percentual'}
                )
                st.markdown(f"### 📥 Exportar dados de {label}")
                exp_col1, exp_col2 = st.columns(2)
                excel_cat = UtilsModule.converter_excel(df_export)
                exp_col1.download_button(
                    f"📊 EXCEL - {label.upper()}",
                    excel_cat,
                    f"sibila_{tab_key}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch',
                    key=f"btn_excel_{tab_key}"
                )
                pdf_cat = PDFModule.gerar_pdf_tabela_estatistica(df_export, label)
                exp_col2.download_button(
                    f"📄 PDF - {label.upper()}",
                    pdf_cat,
                    f"sibila_{tab_key}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "application/pdf",
                    width='stretch',
                    key=f"btn_pdf_{tab_key}"
                )
                st.markdown("---")
                st.markdown(f"**⬆️ {label.upper()} MAIS FREQUENTES (Top 30)**")
                counts.index = counts.index + 1
                st.dataframe(counts.head(30), width='stretch')
                with st.expander(f"Mostrar tabela completa de {label} ({len(counts)} termos)"):
                    st.dataframe(counts, width='stretch')

            if selected_mais_dados == "PALAVRAS-CHAVE":
                show_stats_with_export('palavras_chave', 'Palavra-chave', 'palavras_chave')
            elif selected_mais_dados == "AUTORES CITADOS":
                show_stats_with_export('autores_citados', 'Autor Citado', 'autores_citados')
            elif selected_mais_dados == "COLABORADORES":
                show_stats_with_export('autores_colaboradores', 'Colaborador', 'colaboradores')
            elif selected_mais_dados == "TRADUTORES":
                show_stats_with_export('tradutores', 'Tradutor', 'tradutores')
        else:
            st.warning("⚠️ Base de dados vazia. Cadastre registros na aba CATALOGAÇÃO.")

    # --- EXPORTAR ---
    elif menu == "EXPORTAR":
        st.title("💾 GERENCIAMENTO DE DADOS")
        st.markdown("### 📤 IMPORTAÇÃO")
        c1, c2 = st.columns(2)
        with c1:
            u = st.file_uploader("Importar JSON (catálogo)", type=['json'])
            if u:
                try:
                    n = json.load(u)
                    if isinstance(n, list):
                        dados.extend(n)
                        un = {v.get('_id', str(i)): v for i, v in enumerate(dados)}.values()
                        if PersistenceModule.save_data(list(un)):
                            st.success("✅ Dados importados com sucesso!")
                            st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao importar: {str(e)}")
        with c2:
            u2 = st.file_uploader("Importar JSON (diário de pesquisa)", type=['json'])
            if u2:
                try:
                    d = json.load(u2)
                    if isinstance(d, list):
                        if PersistenceModule.save_diario(d):
                            st.success("✅ Diário importado com sucesso!")
                            st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao importar diário: {str(e)}")

        st.markdown("---")
        st.markdown("### 📥 EXPORTAÇÃO")
        if not df.empty:
            exp_row1_col1, exp_row1_col2 = st.columns(2)
            js = json.dumps(dados, ensure_ascii=False, indent=2)
            exp_row1_col1.download_button(
                "📥 BAIXAR JSON (CATÁLOGO)",
                js,
                f"backup_sibila_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json",
                width='stretch'
            )
            excel_data = UtilsModule.converter_excel(df)
            exp_row1_col2.download_button(
                "📊 BAIXAR EXCEL (CATÁLOGO)",
                excel_data,
                f"backup_sibila_{datetime.now().strftime('%Y%m%d')}.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch'
            )
        else:
            st.info("Nenhum dado para exportar (catálogo).")

        st.markdown("#### Diário de pesquisa")
        diario = PersistenceModule.load_diario()
        if diario:
            js_d = json.dumps(diario, ensure_ascii=False, indent=2)
            st.download_button(
                "📥 BAIXAR JSON (DIÁRIO)",
                js_d,
                f"diario_sibila_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json",
                width='stretch'
            )
        else:
            st.info("Nenhuma entrada no diário para exportar.")

        st.markdown("---")
        st.markdown("### 📊 ESTATÍSTICAS DO SISTEMA")
        stat_col1, stat_col2 = st.columns(2)
        if os.path.exists(BACKUP_DIR):
            backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
            stat_col1.metric("Backups disponíveis", len(backups))
        else:
            backups = []
            stat_col1.metric("Backups disponíveis", 0)
        stat_col2.metric("Total de Registros", len(df))
        diario = PersistenceModule.load_diario()
        st.markdown(f"**Entradas no diário de pesquisa:** {len(diario)}")
        if backups:
            st.markdown("#### 📦 Backups salvos (últimos 5)")
            backups_recentes = backups[:5]
            for bkp in backups_recentes:
                bkp_path = os.path.join(BACKUP_DIR, bkp)
                try:
                    with open(bkp_path, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                    st.download_button(
                        f"📥 Baixar {bkp}",
                        conteudo,
                        file_name=bkp,
                        mime="application/json",
                        width='stretch',
                        key=f"btn_bkp_{bkp}"
                    )
                except Exception as e:
                    st.warning(f"Não foi possível carregar o backup {bkp}: {e}")
            if len(backups) > 5:
                st.info(f"ℹ️ Existem mais {len(backups) - 5} backup(s) antigo(s) não exibido(s).")

if __name__ == "__main__":
    main()
