# importing the necessary libraries
import os # for providing the paths 
import numpy as np
import pandas as pd
import streamlit as st
from pyresparser import ResumeParser

st.set_page_config(layout = 'wide')
st.title('Resume/CV Parser')
st.header('Upload Your Resume/CV')

# File Uploads
uploaded_files = st.file_uploader("Choose your Resume/CV", accept_multiple_files = True, type = ['docx', 'pdf', 'doc']) 
data = []
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        file_data = uploaded_file.getvalue()
        fo = open(uploaded_file.name, 'wb').write(file_data) # writing the files to the directory
        data.append((ResumeParser(uploaded_file.name).get_extracted_data())) # extracting useful information
        os.remove(uploaded_file.name) # removing files from the directory
             
name, email, mobile_number, skills = [], [], [], []
for i in range(0, len(data)):
    dictionary = data[i]
    name.append(dictionary['name'])
    email.append(dictionary['email'])
    mobile_number.append(dictionary['mobile_number'])
    skills.append(dictionary['skills'])

# cleaning the skills list and converting to string
arr = np.array(skills, dtype = object)
for i in range(0, len(skills)):
    x = ', '.join(str(item) for item in skills[i])
    arr[i] = x    

# creating dataframe named df
df = pd.DataFrame({'name': name, 'email': email, 'mobile_number': mobile_number, 'skills': arr})
st.dataframe(df)

# finding unique skills in all the resumes
l1 = [j for i in df['skills'] for j in i.split(',')]
l2 = [i.strip() for i in l1]

# Removing whitespaces present in l1
skills = []
for i in l2:
    if i not in skills:
        skills.append(i)

# creating columns for unique skills
skill_set = pd.DataFrame(columns = skills)
for i in range(len(df)):
    split_text = df.loc[i,'skills'].split(',')
    cols = list(skill_set.columns)
    for j in range(len(split_text)):
        strip_text = split_text[j].strip(); skill_set.loc[i,strip_text] = 1 
        cols.remove(strip_text); skill_set.loc[i,cols] = 0

# creating a selectbox, check streamlit docs
option = st.selectbox('Which skill you want?', (skill_set.columns))
st.write('You selected:', option)             
new_df = pd.concat([df, skill_set], axis = 1)
if option is None:
    st.dataframe(df)
else:
    x = new_df[new_df[option] == 1.0]
    st.dataframe(x[['name', 'email', 'mobile_number', 'skills']])
    
    
    
    
    
    
    
    
    
    
    
    
    
    











