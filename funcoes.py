import pandas as pd 
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def salvar_dados_excel(dados_dict, nome_aba):
    caminho_downloads = Path.home() / "Downloads"
    nome_arquivo = "Cadastro de Fornecedores - Núcleo de Compras.xlsx"
    caminho_final = caminho_downloads / nome_arquivo

    df_novo = pd.DataFrame(dados_dict)
    
    colunas_para_maiusculo = ["NOME DA EMPRESA", "TIPO DE MATERIAL", "TIPO DE SERVIÇO"]

    for col in colunas_para_maiusculo:
        if col in df_novo.columns:
            df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()

    if caminho_final.exists():
        try:
            df_antigo = pd.read_excel(caminho_final, sheet_name=nome_aba)
            df_antigo = df_antigo.dropna(how='all')
            if 'NOME DA EMPRESA' in df_antigo.columns:
                df_antigo = df_antigo.dropna(subset=['NOME DA EMPRESA'])
            
            df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        except Exception:
            df_final = df_novo

        book = load_workbook(caminho_final)
        
        with pd.ExcelWriter(caminho_final, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Usamos os atributos internos com underline para burlar a proteção de "no setter"
            writer._book = book 
            writer._sheets = {ws.title: ws for ws in book.worksheets}
            
            df_final.to_excel(writer, sheet_name=nome_aba, index=False)
            
            # Acessamos a aba para ajustar a largura
            worksheet = writer._sheets[nome_aba]
            for i, col in enumerate(df_final.columns):
                max_len = df_final[col].astype(str).str.len().max()
                max_len = max(max_len, len(str(col))) + 2
                worksheet.column_dimensions[get_column_letter(i + 1)].width = max_len
    else:
        with pd.ExcelWriter(caminho_final, engine='openpyxl') as writer:
            df_novo.to_excel(writer, sheet_name=nome_aba, index=False)
            worksheet = writer.sheets[nome_aba]
            for i, col in enumerate(df_novo.columns):
                max_len = max(df_novo[col].astype(str).str.len().max(), len(str(col))) + 2
                worksheet.column_dimensions[get_column_letter(i + 1)].width = max_len
            
    return True
