import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def salvar_dados_excel(arquivo_upload, dados_novos, nome_aba):
    # 1. Criar o DataFrame com os novos dados
    df_novo = pd.DataFrame(dados_novos)
    
    # Padronização (Maiúsculas)
    colunas_para_maiusculo = ["NOME DA EMPRESA", "TIPO DE MATERIAL", "TIPO DE SERVIÇO"]
    for col in colunas_para_maiusculo:
        if col in df_novo.columns:
            df_novo[col] = df_novo[col].astype(str).str.upper().str.strip()

    # 2. Ler o arquivo existente e combinar os dados
    try:
        arquivo_upload.seek(0)
        # Lemos o arquivo inteiro para garantir que não perderemos outras abas
        todas_as_abas = pd.read_excel(arquivo_upload, sheet_name=None)
        
        if nome_aba in todas_as_abas:
            df_antigo = todas_as_abas[nome_aba]
            df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        else:
            df_final = df_novo
            todas_as_abas[nome_aba] = df_final
            
        todas_as_abas[nome_aba] = df_final # Atualiza a aba específica
    except Exception:
        df_final = df_novo
        todas_as_abas = {nome_aba: df_final}

    # 3. Salvar tudo em um novo objeto na memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for aba, df in todas_as_abas.items():
            df.to_excel(writer, sheet_name=aba, index=False)
            
            # Ajuste de largura das colunas
            worksheet = writer.sheets[aba]
            for i, col in enumerate(df.columns):
                max_len = df[col].astype(str).str.len().max()
                max_len = max(max_len if pd.notna(max_len) else 0, len(str(col))) + 2
                worksheet.column_dimensions[get_column_letter(i + 1)].width = max_len
            
    return output.getvalue()