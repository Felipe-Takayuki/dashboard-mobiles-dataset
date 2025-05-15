import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
from services.readcsv import formatterCSV


class HomePage:
    def init(): 
        dataFormatted = formatterCSV()

        # Limpeza para garantir que 'Launched Price (USA)' seja numérico
        dataFormatted["Launched Price (USA)"] = pd.to_numeric(
            dataFormatted["Launched Price (USA)"].astype(str).str.replace(r'[^\d.]', '', regex=True),
            errors='coerce'
        )

        # Suas transformações originais
        dataFormatted["Battery Capacity"] = dataFormatted["Battery Capacity"]
        dataFormatted["Screen Size"] = dataFormatted["Screen Size"]
        dataFormatted["RAM"] = dataFormatted["RAM"]
        dataFormatted["Front Camera MP"] = dataFormatted["Front Camera"]
        dataFormatted["Back Camera MP"] = dataFormatted["Back Camera"]
        dataFormatted["Launched Year"] = dataFormatted["Launched Year"].astype(int)

        st.set_page_config(layout="wide")
        st.title("Dashboard de Análise de Custo Benefício dos Celulares")

        # Filtros
        ramList = ['Todos'] + sorted(dataFormatted["RAM"].dropna().unique().tolist())
        ram = st.sidebar.selectbox("Memória RAM", ramList)

        df_filtered = dataFormatted.copy()
        if ram != "Todos":
            df_filtered = df_filtered[df_filtered["RAM"] == ram]
        
        st.subheader("Modelos filtrados:")
        st.table(df_filtered["Company Name"] + " " + df_filtered["Model Name"])

        st.markdown("---")
        st.subheader("📊 Gráficos de Análise")

        # Gráfico 1: Média de Preço por Fabricante
        st.markdown("#### Média de Preço (EUA) por Fabricante")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        avg_price = df_filtered.groupby("Company Name")["Launched Price (USA)"].mean().sort_values(ascending=False)
        sns.barplot(x=avg_price.values, y=avg_price.index, palette="viridis", ax=ax1)
        st.pyplot(fig1)

        # Gráfico 2: Preço vs Bateria
        st.markdown("#### Preço vs Capacidade da Bateria")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_filtered, x="Battery Capacity", y="Launched Price (USA)", hue="Company Name", ax=ax2)
        st.pyplot(fig2)

        # Gráfico 3: Tamanho da Tela por Marca
        st.markdown("#### Distribuição do Tamanho da Tela por Marca")
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df_filtered, x="Company Name", y="Screen Size", palette="Set3", ax=ax3)
        ax3.tick_params(axis='x', rotation=45)
        st.pyplot(fig3)

        # Gráfico 4: Preço vs RAM
        st.markdown("#### Preço vs Memória RAM")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_filtered, x="RAM", y="Launched Price (USA)", hue="Company Name", ax=ax4)
        st.pyplot(fig4)

        # Gráfico 5: Evolução do Preço Médio por Ano
        st.markdown("#### Evolução do Preço Médio por Ano de Lançamento (EUA)")
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        avg_by_year = df_filtered.groupby("Launched Year")["Launched Price (USA)"].mean()
        sns.lineplot(x=avg_by_year.index, y=avg_by_year.values, marker="o", ax=ax5)
        st.pyplot(fig5)

        # Gráfico 6: Preço vs Câmera Frontal
        st.markdown("#### Preço vs Megapixels da Câmera Frontal")
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_filtered, x="Front Camera MP", y="Launched Price (USA)", hue="Company Name", ax=ax6)
        st.pyplot(fig6)

        # Gráfico 7: Preço vs Câmera Traseira
        st.markdown("#### Preço vs Megapixels da Câmera Traseira")
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_filtered, x="Back Camera MP", y="Launched Price (USA)", hue="Company Name", ax=ax7)
        st.pyplot(fig7)
