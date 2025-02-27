# BLOC : Import des bibliothèques
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Comment télécharger un data set ? ....en brut ou via internet et une url 
# Téléchargement d'un dataset financier public
url = "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
df = pd.read_csv(url)

# Affichage des premières lignes du dataset
print("Aperçu des données :")
display(df.head())

# Nettoyage des données
df.dropna(inplace=True)  # Suppression des valeurs manquantes

def calculer_ratios(df):
    """Calcule les principaux ratios financiers."""
    df['Marge brute'] = (df['AAPL.High'] - df['AAPL.Low']) / df['AAPL.Open']
    df['Variation journalière'] = df['AAPL.Close'].pct_change()
    df['Volatilité'] = df['Variation journalière'].rolling(window=10).std()
    df['Moyenne mobile 20j'] = df['AAPL.Close'].rolling(window=20).mean()
    df['Moyenne mobile 50j'] = df['AAPL.Close'].rolling(window=50).mean()
    df['RSI'] = 100 - (100 / (1 + df['Variation journalière'].rolling(14).mean() / df['Variation journalière'].rolling(14).std()))
    return df

df = calculer_ratios(df)

# Affichage des statistiques descriptives
print("Statistiques descriptives des ratios :")
display(df[['Marge brute', 'Variation journalière', 'Volatilité', 'RSI']].describe())

# Visualisation des tendances financières
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x=df.index, y='AAPL.Close', label='Cours de clôture')
sns.lineplot(data=df, x=df.index, y='Moyenne mobile 20j', label='Moyenne mobile 20j', linestyle="--")
sns.lineplot(data=df, x=df.index, y='Moyenne mobile 50j', label='Moyenne mobile 50j', linestyle="--")
plt.title("Évolution du cours de clôture d'Apple avec moyennes mobiles")
plt.legend()
plt.show()

# Heatmap des corrélations entre ratios financiers
plt.figure(figsize=(10, 6))
sns.heatmap(df[['Marge brute', 'Variation journalière', 'Volatilité', 'RSI']].corr(), annot=True, cmap='coolwarm')
plt.title("Corrélation entre les indicateurs financiers")
plt.show()

# Distribution de la variation journalière
plt.figure(figsize=(10, 5))
sns.histplot(df['Variation journalière'].dropna(), bins=50, kde=True)
plt.title("Distribution de la variation journalière du cours de l'action Apple")
plt.show()

# Conclusion
display("Analyse approfondie terminée. Étudiez les indicateurs pour anticiper les tendances et risques liés aux variations du cours de l'action.")
