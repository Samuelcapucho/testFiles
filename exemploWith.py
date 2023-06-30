#!/usr/bin/env python
# coding: utf-8

# In[11]:


#!/usr/bin/env python
# coding: utf-8

# In[27]:


import streamlit as st
from zipfile import ZipFile
import zipfile
import base64
import os
import requests 

st.write(os.getcwd())


st.session_state["arquivoObject"] = st.file_uploader("Upload da Nota/RPA", type =['.pdf'])
if st.session_state["arquivoObject"] != None:
    st.session_state["arquivoObject"] = st.session_state["arquivoObject"].getvalue()

    
with ZipFile('intermedio.zip', 'w') as myzip:
    myzip.writestr('protocolo.pdf', st.session_state["arquivoObject"])


with ZipFile('intermedio.zip', 'r') as myzipTwo:
    bytesData = myzipTwo.read()

st.write(bytesData)

jDConvert = json.dumps(bytesData.decode('utf-8')) #tranformando em texto(formato json, string)
baseMd5 = hashlib.md5(jDConvert.encode("utf-8")).hexdigest() #Encode (bytes), do padrão usado (encolding) codifincando do padrão utf-8. md5 precisa que seja encondado (PADRÃO BYTES)
st.write(jDConvert)
st.write(baseMd5)

    


# In[ ]:





# In[ ]:




