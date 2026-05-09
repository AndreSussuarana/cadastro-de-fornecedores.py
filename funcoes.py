import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def salvar_dados_excel(arquivo_upload, dados_novos, nome_aba):
    # 1. Carregar o arquivo enviado para a memória
    # O arquivo_upload vindo do Streamlit já se comporta como um arquivo aberto
    df_novo = pd.DataFrame(dados_novos)
    
    # Padronização (Sua lógica de maiúsculas)
    colunas_para_maiusculo = ["NOME DA EMPRESA", "TIPO DE MATERIAL", "TIPO DE SERVIÇO"]
    for col in colunas_para_maiusculo:
        if col in df_novo.columns:
            df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()

    # 2. Ler o conteúdo atual para concatenar
    try:
        # Resetamos o ponteiro do arquivo para garantir que a leitura comece do zero
        arquivo_upload.seek(0)
        df_antigo = pd.read_excel(arquivo_upload, sheet_name=nome_aba)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    except Exception:
        df_final = df_novo

    # 3. Preparar o salvamento mantendo a formatação (Sua técnica original)
    output = BytesIO()
    arquivo_upload.seek(0) # Volta ao início de novo para o load_workbook
    book = load_workbook(arquivo_upload)
    
    with pd.ExcelWriter(output, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        # Aqui está o seu "pulo do gato" preservado:
        writer._book = book
        writer._sheets = {ws.title: ws for ws in book.worksheets}
        
        df_final.to_excel(writer, sheet_name=nome_aba, index=False)
        
        # Ajuste de largura (Sua lógica original)
        worksheet = writer._sheets[nome_aba]
        for i, col in enumerate(df_final.columns):
            max_len = df_final[col].astype(str).str.len().max()
            max_len = max(max_len if pd.notna(max_len) else 0, len(str(col))) + 2
            worksheet.column_dimensions[get_column_letter(i + 1)].width = max_len
            
    # Retornamos os bytes do arquivo novo (com a formatação do antigo preservada)
    return output.getvalue()