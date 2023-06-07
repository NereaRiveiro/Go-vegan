import pandas as pd
import numpy as np
import pycountry as pc

pd.options.plotting.backend = "plotly"
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans





# limpieza de países con librería pycountry

def filtrar_paises(nombres):
    paises = []
    for nombre in nombres:
        try:
            pais = pc.countries.search_fuzzy(nombre)[0]
            paises.append(pais.name)
        except LookupError:
            pass
    return paises



# grafico de nulos en el dataframe

def plot_missing_values(df):
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isna(),
                yticklabels=False,
                cmap='viridis',
                cbar=False)
    plt.show()

# itera sobre columnas de un df con nulos y las rellena con la moda

def fill_missing_values(dataframe):
    for column in dataframe.columns:
        if dataframe[column].isnull().any():
            mode = dataframe[column].mode()[0]
            dataframe[column].fillna(mode, inplace=True)



# da los porcentajes de nulos por columnas

def nancolsper(data):
    nan_cols = data.isna().mean() * 100
    return nan_cols[nan_cols > 0].sort_values(ascending=False).round(2)



# MACHINE LEARNING

# heatmap de correlaciones. Para columnas no numericas. Hay que importar numpy as np, Pylab as plt y seaborn as sns

def plot_correlation_heatmap(df):
    numeric_columns = df.select_dtypes(include=np.number)

    plt.figure(figsize=(15, 10))
    sns.set(style='white')

    mask = np.triu(np.ones_like(numeric_columns.corr(), dtype=bool))
    cmap = sns.diverging_palette(0, 10, as_cmap=True)

    sns.heatmap(numeric_columns.corr(),
                mask=mask,
                cmap=cmap,
                center=0,
                square=True,
                annot=True,
                linewidths=0.5,
                cbar_kws={'shrink': 0.5})

    plt.show()


# Separación de la data para testeo y train

def split_data(X, y, train_size=0.8, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = tts(X, y, train_size=train_size, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test


# coloreo de matriz de confusión sólo se usa en casos de variables categóricas

def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(15, 8))
    ax = sns.heatmap(cm / cm.sum(), annot=True)
    plt.title('Matriz de Confusión')
    plt.ylabel('Verdad')
    plt.xlabel('Predicción')
    plt.show()


# para buscar clusters antes de kmeans con codo o silueta

def cluster_evaluation(data, max_clusters):
    wcss = []
    silhouette_scores = []

    for k in range(1, max_clusters + 1):
        if k == 1:
            labels = np.zeros(len(data))
            wcss.append(0)
            silhouette_scores.append(0)
        else:
            kmeans = KMeans(nclusters=k)
            kmeans.fit(data)
            wcss.append(kmeans.inertia)
            silhouette_avg = silhouette_score(data, kmeans.labels)
            silhouette_scores.append(silhouette_avg)

    # Elbow Method
    plt.plot(range(1, max_clusters + 1), wcss)
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('WCSS')
    plt.title('Elbow Method')
    plt.show()

    # Silhouette Score
    plt.plot(range(1, max_clusters + 1), silhouette_scores)
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score Method')
    plt.show()