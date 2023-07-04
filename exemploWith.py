#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import streamlit as st
import time
import requests
import base64
import json
import pandas as pd
from unidecode import unidecode
import gspread
import base64
import hashlib
import io
from base64 import b64decode
from datetime import datetime, date, timedelta
import os
from zipfile import ZipFile
import zipfile
from io import BytesIO





def enviarPdf(bytesFilePdf):
    
    mem_zip = BytesIO() 
    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('nf.pdf', bytesFilePdf)

    bytesFileZip = mem_zip.getvalue()
    

    base64Bytes = base64.b64encode(bytesFileZip) #encodando EM BASE 64 para conseguir passar para string UTF-8
    jDConvert = json.dumps(base64Bytes.decode('utf-8')) #tranformando em texto(formato json, string)
    baseMd5 = hashlib.md5(jDConvert.encode("utf-8")).hexdigest() #md5 precisa que seja encondado em str
    
    headers = {'Content-type': "application/json"} 
    data = {
              "call":"IncluirAnexo", 
              "app_key": "2423921576076",
              "app_secret": "3c942267c01ee0b7c2f0bf15beca87a1",
              "param": [ 
                            {
                                "nId": 5767613303,
                                "cTabela": "cliente",
                                "cNomeArquivo": 'nf.pdf',
                                "cArquivo": jDConvert,
                                "cMd5": baseMd5,
                                
                            }


                        ]
            }

 
    
    
    endPoint = f'https://app.omie.com.br/api/v1/geral/anexo/'  
    r = requests.post(endPoint,headers=headers, json = data)
    r = r.json()
    st.write(r)

    
    return


    


st.session_state["arquivoObject"] = st.file_uploader("Upload da Nota/RPA", type =['.pdf'])
if st.session_state["arquivoObject"] != None:
    bytesFilePdf = st.session_state["arquivoObject"].getvalue()
    enviarPdf(bytesFilePdf)
    
    



# import requests
# import base64
# import json
# import streamlit as st
# 
# st.session_state["arquivoObject"] = st.file_uploader("Upload da Nota/RPA", type =['.pdf'])
# if st.session_state["arquivoObject"] != None:
#     bytesFilePdf = st.session_state["arquivoObject"].getvalue()
# 
# 
#     githubToken = "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"
#     githubAPIURL = "https://api.github.com/repos/Samuelcapucho/testFiles/contents/intermedio.zip"
#     headers = {
#                     "Authorization": f'''Bearer {githubToken}''',
#                     "Content-type": "application/vnd.github+json",
#                  }
#     r = requests.get(githubAPIURL, headers=headers)
# 
#     texto = r.json()['content']
#     #print(texto) #ele está decode (ex-base64),ou seja, formato texto
#     texto = base64.b64decode(texto) #virou bytes 
#     print(texto)
# 
# 
#     with ZipFile(texto, 'wb') as myzip:
#         myzip.write(bytesFilePdf)
# 
# 

# In[ ]:




