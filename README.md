# Dashboard Mobile

## Integrantes
- Felipe Takahashi
- Lucas 
- Mateus 
- Nicolas 
- Paulo Henrique

## Como Instalar ?

- No linux/mac
``` 
git clone https://github.com/Felipe-Takayuki/dashboard-mobiles-dataset.git 

cd dashboard-mobiles-dataset

python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt

streamlit run main.py
```
- No Windows 
``` 
git clone https://github.com/Felipe-Takayuki/dashboard-mobiles-dataset.git 

cd dashboard-mobiles-dataset

python -m venv venv 
venv\Scripts\activate.bat 
pip install -r requirements.txt

streamlit run main.py

``` 


## Explicação 
A ideia geral para esse dashboard foi feito pensando principalmente na utilidade para o consumidor

### 1 - Ranking de Custo-Benefício
Nessa sessão, o usuário consegue identificar os aparelhos que oferecem mais recursos (RAM, bateria, câmera) pelo menor preço, sendo uma das partes que  mais agrega valor ao nosso dashboard. 

Obs: Ainda é necessário uma revisão no calculo disso. 

### 2 - Comparação de Modelos
O usuário pode escolher modelos específicos e comparar diretamente suas características técnicas para auxiliar na decisão de compra com uma tabela e graficos com todos dispositivos selecionados

### 3 - Visão Geral das Marcas e Modelos
Esta seção oferece uma análise agregada dos dados, permitindo ao usuário identificar tendências e comparações gerais entre as marcas e modelos disponíveis:

- Média de Preço (USD) por Marca/Modelo: Apresenta o preço médio dos dispositivos de cada marca/modelo, facilitando a identificação de faixas de preço típicas.
- Média de Bateria (mAh) por Marca/Modelo: Exibe a capacidade média da bateria dos dispositivos de cada marca/modelo, útil para comparar a autonomia esperada.
- Média de RAM (GB) por Marca/Modelo: Mostra a quantidade média de memória RAM dos dispositivos de cada marca/modelo, relevante para avaliar o desempenho multitarefas.
- Contagem de Modelos por Processador (Top 10): Ilustra a distribuição dos modelos entre os 10 processadores mais comuns, oferecendo insights sobre as plataformas de hardware mais utilizadas.



