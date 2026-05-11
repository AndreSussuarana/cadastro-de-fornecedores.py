import streamlit as st
import re
from funcoes import salvar_dados_excel
import os 

import streamlit as st

st.set_page_config(page_title="Cadastro de Fornecedores", page_icon="📋")
st.title("🚀Fluxo de Credenciamento Digital (Fornecedores)")

st.info("Primeiro, selecione a planilha onde os dados serão adicionados.")
with st.expander("⚠️ Leia as instruções antes de usar", expanded=False):
    st.write("""
    * **Arquivo para uso:** Caso queira repetir o processo com novas informações, anexe o arquivo que já foi alterado a piori.
    * **Importante:** Se você estiver com este arquivo aberto no seu Excel local, o sistema poderá apresentar erro ao tentar salvar novos dados. 
    * **Dica:** Mantenha o arquivo fechado durante a operação no site.
    """)
arquivo_upload = st.file_uploader("Subir planilha Excel", type=["xlsx"])

st.markdown("---")

tipo_cadastro = st.radio("O fornecedor é de quê?", ["MATERIAL", "SERVIÇO"])

material = ""
servico = ""

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

        # Agora enviamos para a função
        conteudo_excel = salvar_dados_excel(arquivo_upload, dados, nome_aba=tipo_cadastro)

        conteudo_excel = salvar_dados_excel(arquivo_upload, dados, nome_aba=tipo_cadastro)

        if conteudo_excel:
            st.success("Arquivo salvo com sucesso!")
            st.download_button(
                        label="📥 Baixar Planilha Atualizada",
                        data=conteudo_excel,
                        file_name="Cadastro de Fornecedores - Núcleo de Compras.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )    
    else:
        for erro in erros:
            st.error(erro)
        for aviso in avisos:
            st.warning(aviso)
   