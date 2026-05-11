import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def salvar_dados_excel(arquivo_upload, dados_novos, nome_aba):
    # 1. Preparar os dados novos
    df_novo = pd.DataFrame(dados_novos)
    colunas_para_maiusculo = ["NOME DA EMPRESA", "TIPO DE MATERIAL", "TIPO DE SERVIÇO"]
    for col in colunas_para_maiusculo:
        if col in df_novo.columns:
            df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()

    # 2. Carregar o arquivo original com openpyxl para manter os estilos
    arquivo_upload.seek(0)
    book = load_workbook(arquivo_upload)
    
    if nome_aba not in book.sheetnames:
        book.create_sheet(nome_aba)
    sheet = book[nome_aba]

    # --- NOVA LÓGICA PARA ACHAR A LINHA REAL ---
    # Em vez de confiar no max_row, vamos procurar o primeiro buraco na Coluna A
    linha_vazia = 1
    
    while sheet.cell(row=linha_vazia, column=1).value is not None:
        linha_vazia += 1
    
    
    if linha_vazia == 1:
        # Escreve cabeçalhos apenas se a folha estiver zerada
        for c_idx, col_name in enumerate(df_novo.columns, 1):
            sheet.cell(row=1, column=c_idx, value=col_name)
        linha_vazia = 2

    # Escrever os dados novos na posição exata encontrada
    for r_idx, row in df_novo.iterrows():
        for c_idx, value in enumerate(row, 1):
            sheet.cell(row=linha_vazia + r_idx, column=c_idx, value=value)

    # Ajuste de largura (ajustado para ser mais preciso)
    for i, col in enumerate(df_novo.columns, 1):
        column_letter = get_column_letter(i)
        # Tenta pegar o tamanho do novo dado ou manter um mínimo
        val_str = str(df_novo.iloc[0, i-1])
        new_width = max(len(val_str), 15)
        sheet.column_dimensions[column_letter].width = new_width

    output = BytesIO()
    book.save(output)
    return output.getvalue()