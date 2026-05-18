import streamlit as st
import re
import pandas as pd
from funcoes import salvar_no_google_sheets, carregar_dados_google
import os 
import streamlit as st


LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1OTbG6-9Mgobeep-F_bwn-X5rDuEckVsjB20VCu6D6kg/edit?pli=1&gid=1703149077#gid=1703149077"

st.set_page_config(page_title="Cadastro de Fornecedores", page_icon="📋")
st.title("🚀Fluxo de Credenciamento Digital (Fornecedores)")

df_mat = carregar_dados_google("MATERIAL")
df_serv = carregar_dados_google("SERVIÇO")

st.info("A planilha mestre está sincronizada em tempo real com o Google Sheets.")
with st.expander("⚠️ Leia as instruções antes de usar", expanded=False):
    st.write("""
    * **Importante:** Se você estiver com este arquivo aberto no seu Excel local, o sistema poderá apresentar erro ao tentar salvar novos dados. 
    * **Dica:** Mantenha o arquivo fechado durante a operação no site.
    """)

st.markdown("---")

tipo_cadastro = st.radio("O fornecedor é de quê?", ["MATERIAL", "SERVIÇO"])

if tipo_cadastro == "MATERIAL":
    if df_mat is not None:
        with st.expander("🔍 Visualizar Fornecedores de MATERIAL já cadastrados", expanded=False):
            st.dataframe(df_mat)
    else:
        st.warning("Base de materiais ainda não possui dados ou arquivo não encontrado.")
else:
    if df_serv is not None:
        with st.expander("🔍 Visualizar Fornecedores de SERVIÇO já cadastrados", expanded=False):
            st.dataframe(df_serv)
    else:
        st.warning("Base de serviços ainda não possui dados ou arquivo não encontrado.")

st.markdown("---")
st.subheader("📝 Formulário de Novo Cadastro")

nome_empresa = st.text_input("Nome da Empresa", key="NOME DA EMPRESA").upper().strip()
cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00", key="CNPJ")

if tipo_cadastro == "MATERIAL":
    material = st.text_input("Material", key="TIPO DE MATERIAL").upper().strip()
else:
    servico = st.text_input("Serviço Prestado", key="TIPO DE SERVIÇO").upper().strip()

tipo_telefone = st.radio("Qual o tipo de telefone?", ["FIXO", "CELULAR"])
if tipo_telefone == "FIXO":
    telefone = st.text_input("Telefone", placeholder="(98) 6543-2100", key="TELEFONE")
else:
    telefone = st.text_input("Telefone", placeholder="(98) 76543-2100", key="TELEFONE")

email = st.text_input("E-mail", key="ENDEREÇO ELETRÔNICO")
cidade = st.text_input("Cidade", key="CIDADE")
cep = st.text_input("CEP", placeholder="11.111-111", key="CEP")
obs = st.text_input("Observações", key="OBSERVAÇÕES")

if st.button("Salvar dados na Tabela"):
    erros = []
    avisos = []

    if not nome_empresa:
        erros.append("Ponha o nome da empresa")
    
    if cnpj and not re.match(r"^\d{2}\.\d{3}\.\d{3}/\d{4}\-\d{2}$", cnpj):
        erros.append("CNPJ: Corrija aí, os números não completam ou a formatação está errada")
    
    if tipo_cadastro == "SERVIÇO" and not servico:
        avisos.append("Serviço: Vai colocar não?")
    if tipo_cadastro == "MATERIAL" and not material:
        erros.append("Que tipo de material ela fornece?")
        
    if tipo_telefone == "CELULAR" and telefone and not re.match(r"^\(\d{2}\) \d{5}\-\d{4}$", telefone):
        erros.append("Telefone: Digite no formato (XX) XXXXX-XXXX")
    if tipo_telefone == "FIXO" and telefone and not re.match(r"^\(\d{2}\) \d{4}\-\d{4}$", telefone):
        erros.append("Telefone: Digite no formato (XX) XXXX-XXXX")
    if email:
        if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email, re.IGNORECASE):
            erros.append("E-mail: Essa formatação está incorreta")
        
    if not cidade:
        avisos.append("Cidade: De qual cidade ela opera?")
        
    if cep and not re.match(r"^\d{2}\.\d{3}\-\d{3}$", cep):
        erros.append("CEP: Insira corretamente (00.000-000)")
    
    if len(erros) == 0:
       
        # Criamos o dicionário JÁ NA ORDEM CORRETA das colunas do Excel
        if tipo_cadastro == "MATERIAL":
            dados = {
                "NOME DA EMPRESA": [nome_empresa],
                "CNPJ": [cnpj],
                "TIPO DE MATERIAL": [material], # 3ª Coluna
                "TELEFONE": [telefone],
                "ENDEREÇO ELETRÔNICO": [email],
                "CIDADE": [cidade],
                "CEP": [cep],
                "OBSERVAÇÕES": [obs]
            }
        else:
            dados = {
                "NOME DA EMPRESA": [nome_empresa],
                "CNPJ": [cnpj],
                "TIPO DE SERVIÇO": [servico], # 3ª Coluna
                "TELEFONE": [telefone],
                "ENDEREÇO ELETRÔNICO": [email],
                "CIDADE": [cidade],
                "CEP": [cep],
                "OBSERVAÇÕES": [obs]
            }

        with st.spinner("Salvando dados na nuvem..."):
            sucesso = salvar_no_google_sheets(dados, nome_aba=tipo_cadastro)

        if sucesso:
            st.success("✅ Dados salvos com sucesso no Google Sheets!")
            st.balloons()
            st.markdown(f"### [🔗 Clique aqui para abrir a planilha]({LINK_PLANILHA})")
    else:
        for erro in erros:
            st.error(erro)
        for aviso in avisos:
            st.warning(aviso)
   