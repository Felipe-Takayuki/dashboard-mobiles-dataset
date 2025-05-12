import streamlit as st 
from services.readcsv import formatterCSV

class HomePage:
    def init(): 
        dataFormatted = formatterCSV()
        st.set_page_config(layout="wide")
        st.title("Dashboard de Análise de Custo Beneficio dos Celulares")
        year = st.sidebar.selectbox("Ano de Lançamento", dataFormatted["Launched Year"].unique())
        prices = st.sidebar.selectbox("Preço de Lançamento", dataFormatted["Launched Price (USA)"].unique())
        ram = st.sidebar.selectbox("Memória RAM", dataFormatted["RAM"].unique())
        df_filtered = dataFormatted.copy()

        if year != "Todos":
            df_filtered = df_filtered[df_filtered["Launched Year"] == year]

        if prices != "Todos":
            df_filtered = df_filtered[df_filtered["Launched Price (USA)"] == prices]

        if ram != "Todos":
            df_filtered = df_filtered[df_filtered["RAM"] == ram]
            
        st.table(df_filtered["Model Name"])

