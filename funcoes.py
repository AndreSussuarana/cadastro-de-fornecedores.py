import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Esta função substitui a 'salvar_dados_excel' para a nuvem
def salvar_no_google_sheets(dados_novos, nome_aba):
    """
    Conecta ao Google Sheets, limpa os dados e insere na nuvem.
    """
    # 1. Autenticação (O seu crachá digital)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("chave_google.json", scope)
    client = gspread.authorize(creds)

    # 2. Abertura da Planilha (Acesso à sala)
    # Use o nome exato que aparece no topo da sua planilha no navegador
    planilha = client.open_by_key("1OTbG6-9Mgobeep-F_bwn-X5rDuEckVsjB20VCu6D6kg")
    sheet = planilha.worksheet(nome_aba)

    # 3. Preparação e Padronização (O rigor da Engenharia)
    df_novo = pd.DataFrame(dados_novos)
    
    # Normalizando para MAIÚSCULAS (evita bagunça no banco de dados)
    for col in df_novo.columns:
        df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()
    
    # O Google Sheets recebe listas de listas (linhas)
    novas_linhas = df_novo.values.tolist()

    # 4. Gravação (O 'Pulo do Gato' moderno)
    # O append_rows já localiza a primeira linha vazia e preserva o cabeçalho
    sheet.append_rows(novas_linhas)
    
    return True

def carregar_dados_google(nome_aba):
    """
    Lê os dados da nuvem para exibir no st.dataframe do seu App
    """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("chave_google.json", scope)
        client = gspread.authorize(creds)
        
        planilha = client.open_by_key("1OTbG6-9Mgobeep-F_bwn-X5rDuEckVsjB20VCu6D6kg")
        sheet = planilha.worksheet(nome_aba)
        
        # Puxa tudo e vira DataFrame
        dados = sheet.get_all_records()
        return pd.DataFrame(dados)
    except Exception as e:
        print(f"Erro ao carregar: {e}")
        return None