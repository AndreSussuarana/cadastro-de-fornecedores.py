import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_google():
    """
    Função auxiliar para autenticar tanto localmente quanto na nuvem.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # 1. Tenta carregar dos Secrets do Streamlit (Modo Nuvem)
    if "gcp_service_account" in st.secrets:
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    # 2. Se não achar, carrega o arquivo local (Modo Desenvolvimento)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("chave_google.json", scope)
    
    return gspread.authorize(creds)

def salvar_no_google_sheets(dados_novos, nome_aba):
    client = conectar_google()
    planilha = client.open_by_key("1OTbG6-9Mgobeep-F_bwn-X5rDuEckVsjB20VCu6D6kg")
    sheet = planilha.worksheet(nome_aba)

    df_novo = pd.DataFrame(dados_novos)
    colunas_ajuste = ["NOME DA EMPRESA", "", "TIPO DE MATERIAL", "TIPO DE SERVIÇO"]
    for col in colunas_ajuste.columns:
        if col in df_novo.columns:
            df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()
    
    novas_linhas = df_novo.values.tolist()
    sheet.append_rows(novas_linhas)
    return True

def carregar_dados_google(nome_aba):
    try:
        client = conectar_google()
        planilha = client.open_by_key("1OTbG6-9Mgobeep-F_bwn-X5rDuEckVsjB20VCu6D6kg")
        sheet = planilha.worksheet(nome_aba)
        dados = sheet.get_all_records()
        return pd.DataFrame(dados)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None