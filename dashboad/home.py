import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils.readcsv import formatterCSV


class HomePage:

    def init():
        dataFormatted = formatterCSV()

        dataFormatted["Storage"] = dataFormatted["Storage"].astype(str).str.extract(
            r'(\d+)').astype(float)

        dataFormatted["Launched Price (USA)"] = pd.to_numeric(
            dataFormatted["Launched Price (USA)"].astype(str).str.replace(
                r'[^\d.]', '', regex=True),
            errors='coerce'
        )

        dataFormatted["Battery Capacity"] = dataFormatted["Battery Capacity"]
        dataFormatted["Screen Size"] = dataFormatted["Screen Size"]
        dataFormatted["RAM"] = dataFormatted["RAM"]
        dataFormatted["Front Camera MP"] = dataFormatted["Front Camera"]
        dataFormatted["Back Camera MP"] = dataFormatted["Back Camera"]
        dataFormatted["Launched Year"] = dataFormatted["Launched Year"].astype(int)

        st.set_page_config(layout="wide")
        st.title("Dashboard de Análise de Dados de Dispositivos Mobile")

        # Filtros
        marcasList = ['Todas'] + \
            sorted(dataFormatted["Company Name"].unique().tolist())
        marcas = st.sidebar.selectbox("Marca", marcasList)

        modelosList = ['Todos'] + \
            sorted(dataFormatted["Model Name"].unique().tolist())
        modelos = st.sidebar.selectbox("Modelo", modelosList)  # Novo filtro de modelo

        # Filtro de Preço
        min_price = float(dataFormatted["Launched Price (USA)"].min())
        max_price = float(dataFormatted["Launched Price (USA)"].max())

        preco_minimo, preco_maximo = st.sidebar.slider(
            "Faixa de Preço (USD)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price)
        )

        num_top = st.sidebar.slider(
            "Número de dispositivos no ranking do gráfico", min_value=5, max_value=20, value=10)
        df_filtered = dataFormatted.copy()
        if marcas != "Todas":
            df_filtered = df_filtered[df_filtered["Company Name"] == marcas]
        if modelos != "Todos":
            df_filtered = df_filtered[df_filtered["Model Name"] == modelos]  # Aplicar filtro de modelo


        df_filtered = df_filtered[
            (df_filtered["Launched Price (USA)"] >= preco_minimo) &
            (df_filtered["Launched Price (USA)"] <= preco_maximo)
        ]

        # Score Custo Beneficio
        st.markdown("---")
        st.subheader("🏆 Ranking de Custo-Benefício")
        st.markdown(
            "```FORMULA = RAM (GB) + Capacidade da Bateria (mAh) + Megapixels da Câmera Traseira / Preço (USD) ```")
        # Score de custo-benefício
        # Garantindo que as colunas usadas no cálculo existam e são numéricas
        if all(col in df_filtered.columns for col in [
                "RAM", "Battery Capacity", "Back Camera MP", "Launched Price (USA)"]):
            df_filtered["Score CustoBenefício"] = (
                df_filtered["RAM"].fillna(0) +
                df_filtered["Battery Capacity"].fillna(0) +
                pd.to_numeric(df_filtered["Back Camera MP"], errors='coerce').fillna(
                    0)
            ) / df_filtered["Launched Price (USA)"].fillna(1)  # Evitar divisão por zero
            df_score = df_filtered.sort_values(
                "Score CustoBenefício", ascending=False).reset_index(drop=True)

            st.markdown("#### Top Dispositivos por Custo-Benefício")
            top_cost_benefit = df_score.head(num_top)[
                ["Company Name", "Model Name", "RAM", "Storage", "Battery Capacity",
                 "Back Camera MP", "Launched Price (USA)", "Score CustoBenefício"]
            ]
            top_cost_benefit.columns = ["Marca", "Modelo", "RAM (GB)",
                                        "Armazenamento (GB)", "Bateria (mAh)",
                                        "Câmera Traseira (MP)", "Preço (USD)",
                                        "Score Custo-Benefício"]
            st.dataframe(top_cost_benefit, use_container_width=True)

        else:
            st.warning(
                "Colunas necessárias para calcular o Score de Custo-Benefício não encontradas.")

        # Gráfico do score (movido para antes das tabelas de consumidor)
        st.markdown("#### Visualização do Score de Custo-Benefício")

        top_devices = df_score.head(num_top)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_devices["Model Name"],
                top_devices["Score CustoBenefício"], color='mediumseagreen')
        ax.invert_yaxis()
        ax.set_title(f'Top {num_top} Dispositivos com Melhor Custo-Benefício')
        ax.set_xlabel("Score Custo-Benefício")
        st.pyplot(fig)
        
        # Comparação
        st.markdown("---")
        st.subheader("🔍 Comparação de Modelos")

        # Selectbox para selecionar os modelos a comparar
        modelos_para_comparar = st.multiselect(
            "Selecione os modelos para comparar",
            df_filtered["Model Name"].unique()
        )

        if modelos_para_comparar:
            # Filtrar o DataFrame com base nos modelos selecionados
            df_comparacao = df_filtered[df_filtered["Model Name"].isin(
                modelos_para_comparar)]

            # Selecionar as colunas para comparação
            colunas_comparacao = ["Company Name", "Model Name", "RAM", "Storage",
                                 "Battery Capacity", "Back Camera MP", "Launched Price (USA)"]
            df_comparacao = df_comparacao[colunas_comparacao].copy()  # Criar uma cópia para evitar warnings
            df_comparacao.columns = ["Marca", "Modelo", "RAM (GB)", "Armazenamento (GB)",
                                    "Bateria (mAh)", "Câmera Traseira (MP)", "Preço (USD)"]

            # Exibir a tabela de comparação
            st.dataframe(df_comparacao)

            # Criar gráficos de comparação
            st.subheader("Gráficos de Comparação")

            caracteristicas_para_comparar = {
                "RAM (GB)": "RAM (GB)",
                "Armazenamento (GB)": "Armazenamento (GB)",
                "Bateria (mAh)": "Bateria (mAh)",
                "Preço (USD)": "Preço (USD)"
            }

            for caracteristica, coluna in caracteristicas_para_comparar.items():
                fig, ax = plt.subplots(figsize=(8, len(modelos_para_comparar) * 0.5))  # Ajustar altura da figura
                sns.barplot(x=df_comparacao[coluna], y=df_comparacao["Modelo"], ax=ax, palette="viridis")
                ax.set_title(f"Comparação de {caracteristica}")
                ax.set_xlabel(caracteristica)
                ax.set_ylabel("")  # Remover rótulo do eixo y para economizar espaço
                st.pyplot(fig)

        else:
            st.info("Selecione pelo menos um modelo para comparar.")

        st.markdown("---")
        st.subheader("📊 Gráficos de Análise")

        # Gráfico 1: Média de Preço em Dólar por Marca
        st.markdown("#### Média de Preço em Dólar por Marca/Modelo")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        avg_price = df_filtered.groupby("Company Name")["Launched Price (USA)"].mean().sort_values(ascending=True)
        ax1.plot(avg_price.values, avg_price.index, marker='o')

        if modelos != "Todos":
            avg_price = df_filtered.groupby("Model Name")[
                "Launched Price (USA)"].mean().sort_values(ascending=True)
            ax1.barh(avg_price.index, avg_price.values)
            ax1.set_xlabel("Média de Preço (USD)")
            ax1.set_ylabel("Modelo")
        ax1.grid(True)
        st.pyplot(fig1)

        # Gráfico 2: Marca vs Bateria
        st.markdown("#### Média de Bateria (mAh) por Marca/Modelo")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        avg_baterry = df_filtered.groupby("Company Name")["Battery Capacity"].mean().sort_values(ascending=False)
        sns.barplot(x=avg_baterry.values,y=avg_baterry.index, palette="viridis", ax=ax2)
        ax2.set_xlabel("Média da Capacidade da Bateria (mAh)")
        ax2.set_ylabel("Fabricante")
        if modelos != "Todos":  
            avg_baterry = df_filtered.groupby("Model Name")[
                "Battery Capacity"].mean().sort_values(ascending=False)
            sns.barplot(x=avg_baterry.values,
                        y=avg_baterry.index, palette="viridis", ax=ax2)
            ax2.set_xlabel("Média da Capacidade da Bateria (mAh)")
            ax2.set_ylabel("Modelo")
        st.pyplot(fig2)
        
        # Gráfico 3: Média de RAM (GB) por Marca/Modelo
        st.markdown("#### Média de RAM (GB) por Marca/Modelo")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        if modelos == "Todos":
            avg_ram = df_filtered.groupby("Company Name")["RAM"].mean().sort_values(ascending=False)
            sns.barplot(x=avg_ram.index, y=avg_ram.values, palette="plasma", ax=ax3)  # Eixos trocados
            ax3.set_ylabel("Média de RAM (GB)")
            ax3.set_xlabel("Fabricante")
            plt.xticks(rotation=45, ha="right")
        else:
            avg_ram = df_filtered.groupby("Model Name")["RAM"].mean().sort_values(ascending=False)
            sns.barplot(x=avg_ram.index, y=avg_ram.values, palette="plasma", ax=ax3)  # Eixos trocados
            ax3.set_ylabel("Média de RAM (GB)") 
            ax3.set_xlabel("Modelo")
            plt.xticks(rotation=45, ha="right")
        st.pyplot(fig3)

        ### Gráfico Processador
        st.markdown("#### Contagem de Modelos por Processador (Top 10)")
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        top_n = 10
        processor_counts = df_filtered["Processor"].value_counts().nlargest(top_n)
        sns.barplot(x=processor_counts.values, y=processor_counts.index, palette="viridis", ax=ax5)
        ax5.set_xlabel("Número de Modelos")
        ax5.set_ylabel("Processador")
        st.pyplot(fig5)

