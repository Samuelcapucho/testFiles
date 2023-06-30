#!/usr/bin/env python
# coding: utf-8

# In[110]:


import requests
import base64
import json
import streamlit as st

st.session_state["arquivoObject"] = st.file_uploader("Upload da Nota/RPA", type =['.pdf'])
if st.session_state["arquivoObject"] != None:
    bytesFilePdf = st.session_state["arquivoObject"].getvalue()


    githubToken = "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"
    githubAPIURL = "https://api.github.com/repos/Samuelcapucho/testFiles/contents/intermedio.zip"
    headers = {
                    "Authorization": f'''Bearer {githubToken}''',
                    "Content-type": "application/vnd.github+json",
                 }
    r = requests.get(githubAPIURL, headers=headers)

    texto = r.json()['content']
    #print(texto) #ele está decode (ex-base64),ou seja, formato texto
    texto = base64.b64decode(texto) #virou bytes 
    print(texto)


    with ZipFile(texto, 'wb') as myzip:
        myzip.write(bytesFilePdf)


# In[ ]:




