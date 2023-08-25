#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#atualizado

import pandas as pd
import streamlit as st
import time
import requests
import requests
import base64
import json
import pandas as pd
from unidecode import unidecode
import gspread
from datetime import datetime, date
import smtplib
import email.message





def consultaProj(token):
        headers = {'Content-type': "application/json"} 
        data = {
                "call":"ListarProjetos", 
                "app_key": "2423921576076",
                "app_secret": "3c942267c01ee0b7c2f0bf15beca87a1",
                "param": [ 

                            {
                                "pagina": 1,
                                "registros_por_pagina": 1,
                                "apenas_importado_api": "N",
                                "nome_projeto": token, 

                             }
                        ]
                }

        endPoint = f'https://app.omie.com.br/api/v1/geral/projetos/'  
        r = requests.post(endPoint,headers=headers, json = data )
        r = r.json()
        return r['registros']
    
    
def consultaVendedores():
        headers = {'Content-type': "application/json"} 
        data = {
                "call":"ListarVendedores", 
                "app_key": "2423921576076",
                "app_secret": "3c942267c01ee0b7c2f0bf15beca87a1",
                "param": [ 

                            {
                                "pagina": 1,
                                "registros_por_pagina": 50,
                                "apenas_importado_api": "N",
                             }
                        ]
                }

        endPoint = f'https://app.omie.com.br/api/v1/geral/vendedores/'  
        r = requests.post(endPoint,headers=headers, json = data )
        r = r.text
        return r
    
def enviarEmail(emailTo, token, dtVencimento, doc, valor):

    valor =  "{:.2f}".format(float(valor))
    valor = str(valor)
    valor = valor.replace(".", ",")
         
    corpo_email = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #ffffff;
            }}
            .header, .footer {{
                background-color: #C14AF2;
                color: #ffffff;
                padding: 10px;
                text-align: center;
                display: center;
                align-items: center;
                justify-content: center;
            
            }}
            .header img {{
                max-width: 400px;
                height: auto;
                margin-right: 10px;
            }}
            .section {{
                margin: 20px;
                padding: 20px;
                background-color: #C14AF2;
                border: 1px solid #ffffff;
                color: #ffffff;
                border-radius: 5px;
            
            }}
            h1, h2 {{
                font-size: 24px;
                color: #ffffff;
            }}
            .link {{
                color: #ffffff;
                text-decoration: none;
            }}
            .link:hover {{
                text-decoration: underline;
                color: #ffffff;
                
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="https://live.staticflickr.com/65535/53120644017_fff920544a_k.jpg" alt="Logo da Empresa">
        </div>
        <div class="section">
            <h2>Dados para preenchimento do Formulário</h2>
            <p>CNPJ/CPF: {doc} </p>
            <p>Código do Projeto: {token} </p>
            <p>Valor: {valor} </p>
        </div>
        <div class="section">
            <h2>Dados para emissão da Nota Fiscal</h2>
            <p>Razão Social: Br Influenciadores Marketing LTDA</p>
            <p>CNPJ: 25.018.794/0001-41</p>
            <p>Data de vencimento: {dtVencimento} </p>
        </div>
        <div class="section">
            <h2>Let's go</h2>
            <p class="footer-text"><a class="link" href="https://parceiro-brmediagroup.streamlit.app/" style="color: white;">╔═║ Preencher Formulário - Clicando aqui ║═╝</a></p>
        </div>
        <div class="footer">
            <p class="footer-text">© 2023 BR MEDIA GROUP. Todos os direitos reservados. <a class="link" href="mailto:contas@br-mediagroup.com" style="color: white;">╔═║ Ajuda - Clicando aqui ║═╝</a></p>
        </div>
    </body>
    </html>
    """


















        
    msg = email.message.Message()
    msg['Subject'] = f"Ordem de Pagamento - Br Media Group"
    msg['From'] = 'contas-noreply@br-mediagroup.com'
    msg['To'] = f'{emailTo}'
    password = 'petzkgvgtoakfxly'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587') #padrão google
    s.starttls()
    
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    

def tratData (dataVcto):
    dataVctoD = dataVcto.strftime("%d")
    dataVctoM = dataVcto.strftime("%m")
    dataVctoY = dataVcto.strftime("%Y")
    dataVctoTrat = str(dataVctoD+"/"+dataVctoM+"/"+dataVctoY)
    return dataVctoTrat




credentials = {
                  "type": "service_account",
                  "project_id": "sheetseasyapi",
                  "private_key_id": "a752403f561710866640be76189aa522aab49627",
                  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCZSdDfxJgfhxrO\n61UJ1jv5NhxYnI4KJsORKhur+sYa/Ci9Pm9jFYECxVvoLTeQn9xWtpQ4JEuEgMUg\nHw/JhFpgbxhZW2Vx4IQAPbgNCqCG9c3gPxiQmljPRZKzGn0R/jlWEEXC0tsTxvlq\nqqcBPWDHV9YDSx/KF0lGuvH93NCk8sFhgntkZw0Slcqu3LYyDgZvq6rCrHgsIuUb\nghfPJ+pWYN6rfC60vEPONULrjkppWWKisLyrn8S4noLXnLXzJiog/udfgPncfN9b\nJLUO/qhcFj5qQLX43FqhbIxafFlAVEmaonXXmhdTq0LQNeRCJzoCl6RTQXU4cqtZ\nBkUC7iqTAgMBAAECgf8S6xuZRXNQJ6u/uVfXwHqOBEpKjQfWLLWg8dSEqEPvfmBL\n1laHcD51ydmgQdwBWN4PpOayUEJXEgdalBlMakAq79RIV4uJDqBgi8/Ds+d9g6f3\nVGR84f11fvYDquXQ6w9ZQJyw1m2U5M8UVPt4Vl32zp1YIAvq0ui4RdQ2blmClCn5\nfe6c9MKvpJmtVAVndCqXry1kg+dcUA9Hc8a5ivhYp0RQR7c3M8V8nGB2bfPsJpr7\n9SpzxBLRM95WTHu9vlRpEJ5nxOdP9jqA0KrsPVoYATzBD4j6sqYrzRUWIC0u007q\nkRGfs2ZH8L0AFrkfM8m9wH8H/ZPMhwa9BGlEw8kCgYEA0fV57UAyByNI3F7PJFpO\nUDFEDG9we+K2kQ8gxc+AZjskDG/c1gw4WGNNY33zgVbkctf51HpDIdmADO2vIpez\na08OqiNVi+DwYrUah9ObKQujZenA2lkE+uHINFcZk08jb42Dumg+jsA8s4eEcjlY\nNynLxuJwnwDcXLNRJc9106sCgYEAuucCLHJHmkryQS58byoifh2pVrVpbWCOJ+Xk\noir7l4ZFKhWffrJwu5YbtxeXCJVhCIx4WAryIYXgYVX00Vhz6DUt7c0vrcGbZWVx\n7okc+pZJlG0btLecptbPPVZj7CWmBgHJZAsr4wIczLnLB2GTW6kD0OwA9T8IlEIy\nE9FknLkCgYAieykSAKf2qiHOJzfnpXkVDHI7hJW5ksse2ZgtRF227GGINVrUQF+E\njJJqE4ZJKIcOIVAjSAz8Yyb3eJV5neZWaj5jTLhA56ky3MFFq0fhHssv8oq8kUAT\nH79scR1/JtEQAfKvS21yrjmJ1mi3BZnqPU/9ErUiN9b41m4uQnr8TwKBgBjHofkk\nmauyPhY4RJU0f+g6pIXzfWvb/lz51OtPSZYYXjkrLr9MhzfHuhr3TLX9oCTTAu2h\nXeLl7g7Zp6DN2mgyDMnXh3fBEIpL/eQDV809ebntEVxPb7yLBGT8fDkF8NIhEINs\nG8B4OjtGcs2iuTfQ28mqUKIzXj7R2/PWskE5AoGBAJiEKlLCwWlYVaKCZ2bWZ9hv\ngxmhIUfJK+RxHxjAgasyuwy0BxxmXyNARTmqQ7129I3YwZ1v24bQS6cbEuLG00Q3\nOGfQITCWX6vf6IDXeSUOwIcwFmJK5+FY+QXaax+QLdGTfVIQHXy48M8aiBPRb7pF\n3AUcjs/fVD0UXFGBdi0s\n-----END PRIVATE KEY-----\n",
                  "client_email": "projformseasy@sheetseasyapi.iam.gserviceaccount.com",
                  "client_id": "105862664438268915241",
                  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                  "token_uri": "https://oauth2.googleapis.com/token",
                  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/projformseasy%40sheetseasyapi.iam.gserviceaccount.com",
                  "universe_domain": "googleapis.com"
            }

    
    
df = st.file_uploader('Arquivo excel [.xlsx]', type="xlsx", accept_multiple_files=False, help="Faça o upload do arquivo padrão.")


while df == "":
    time.sleep(1)
    
df = pd.read_excel(df)
    
for item in df['documento']:
    st.write(item)
    
time.sleep(60)




    
doc = st.number_input("N° CNPJ/CPF [somente números]", help="Documento do fornecedor. Apenas números, não digite pontos ou espaços.")
    
doc = str(doc)

    
emailTo = st.text_input("E-mail", help="E-mail do fornecedor.")
catAux = st.selectbox('Categoria', ['Produção','Influenciadores/Agências'], index=1, help='Selecione uma Categoria')
valor = str(st.number_input("Valor", min_value = 0.0, max_value = 500000.00, format="%.2f", step =None))
token = st.text_input("Código do Projeto")
dataVcto = st.date_input("Data de Vencimento", value = None, min_value = datetime.now().date())
codVendedor = st.empty().text_input("Código Vendedor", type="password")

while (codVendedor == "") or (token == "") or (valor == "0.0") or (emailTo == "") or (doc == "") or (dataVcto == ""):
    time.sleep(1)


if catAux == 'Produção':
        catAux = 'pro'
else:
        catAux = 'iAg'
        

    
protocoloBack = token+doc+valor
protocoloBack = "#" + protocoloBack


#config button    
def disable():
    st.session_state.disabled = True
    
if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.form("myform"):
    submit_button = st.form_submit_button(
        "Enviar", on_click=disable, disabled=st.session_state.disabled
    )

#Fim config button
    if submit_button:
        registrosProj = consultaProj(token)
        vendedoresAux = consultaVendedores()
        dataVcto = tratData(dataVcto)

        if registrosProj > 0:
            if codVendedor in vendedoresAux:

                idSheet = "1XO5p0WAJmPJIfWeHYISPrjDv5B5IpyoPzWEh7nqUjVU"
                #arquivo de permissão
                gc = gspread.service_account_from_dict(credentials)
                #abrindo pasta de trabalho
                fileWork = gc.open_by_key(idSheet)
                #selecionando uma planilha
                sheet = fileWork.worksheet('MariMidea')
                sheet.append_row([valor, doc, token, protocoloBack, emailTo, dataVcto, codVendedor, catAux])
                
                st.write(f'OP incluída com sucesso. Este procedimento gerou o protocolo: {protocoloBack}')
                st.markdown("[Acompanhe Clicando Aqui](https://docs.google.com/spreadsheets/d/1XO5p0WAJmPJIfWeHYISPrjDv5B5IpyoPzWEh7nqUjVU/edit#gid=1658200171)")
                    
                


                enviarEmail(emailTo, token, dataVcto, doc, valor)


            else: 
                st.write('Código do vendedor inválido, tente novamente.')



        else:
            st.write('Código do projeto inválido, consulte seu gestor.')
    

