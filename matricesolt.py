import pandas as pd
import numpy as np
import streamlit as st

# Import du fichier Excel
uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=1)

# Interface utilisateur Streamlit
st.title("Calcul de la matrice Saisie Soltea")
st.sidebar.subheader("Sélectionnez les écoles pour 30% :")
selected_ecoles_30pct = st.sidebar.text_area("Entrez les noms des écoles, séparés par des virgules", "")
if st.sidebar.button("Calculer la matrice"):
    # Calcul de la matrice
 if not selected_ecoles_30pct : 
    nb_sirets = df['SIRET ENTREP'].replace(r'^\s*$', np.nan, regex=True).notnull().sum()
    keys = df['SIRET ENTREP'].iloc[1:1+nb_sirets].to_list()
    values = list(map(int, df['MONTANT ETABLISSEMENT'].iloc[1:1+nb_sirets].to_list()))
    sirets = dict(zip(keys, values))
    sirets_30pct = {key:value*.3 for key, value in sirets.items()}
    ecoles = df.iloc[0][5:-3].to_dict()
    n_siret = len(sirets)
    n_ecoles = len(ecoles)
    grid = np.zeros((n_siret, n_ecoles))
    sirets_names = list(sirets.keys())
    ecoles_names = list(ecoles.keys())
    i_ecole = 0
    i_siret = 0
    while i_ecole < n_ecoles and i_siret < n_siret:
        montant = min(sirets[sirets_names[i_siret]], ecoles[ecoles_names[i_ecole]])
        grid[i_siret][i_ecole] = montant
        sirets[sirets_names[i_siret]] -= montant 
        ecoles[ecoles_names[i_ecole]] -= montant
        if sirets[sirets_names[i_siret]] == 0:
            i_siret += 1
        if ecoles[ecoles_names[i_ecole]] == 0:
            i_ecole += 1
    # Création du dataframe avec les résultats
    new_df = pd.DataFrame(grid, columns=ecoles_names, index=sirets_names)
    
    # Affichage du dataframe sur Streamlit
    st.write(new_df)

 else : 
    nb_sirets = df['SIRET ENTREP'].replace(r'^\s*$', np.nan, regex=True).notnull().sum()
    keys = df['SIRET ENTREP'].iloc[1:1+nb_sirets].to_list()
    values = list(map(int, df['MONTANT ETABLISSEMENT'].iloc[1:1+nb_sirets].to_list()))
    sirets = dict(zip(keys, values))
    sirets_30pct = {key:value*.3 for key, value in sirets.items()}
    ecoles = df.iloc[0][5:-3].to_dict()
    n_siret = len(sirets)
    n_ecoles = len(ecoles)
    grid = np.zeros((n_siret, n_ecoles))
    sirets_names = list(sirets.keys())
    ecoles_names = list(ecoles.keys())
    liste_ecoles_30pct = [e.strip() for e in selected_ecoles_30pct.split(",")]
    for eco in liste_ecoles_30pct:
        i_siret = 0
        while ecoles[eco] > 0:
            siret_name = sirets_names[i_siret]
            montant_siret = min(sirets_30pct[siret_name], sirets[siret_name])
            montant_to_sub = min(ecoles[eco], montant_siret)
            grid[i_siret][ecoles_names.index(eco)] = montant_to_sub
            ecoles[eco] -= montant_to_sub
            sirets[siret_name] -= montant_to_sub 
            i_siret += 1
        i_ecole = 0
    i_siret = 0
    while i_ecole < n_ecoles and i_siret < n_siret:
        montant = min(sirets[sirets_names[i_siret]], ecoles[ecoles_names[i_ecole]])
        grid[i_siret][i_ecole] = montant
        sirets[sirets_names[i_siret]] -= montant 
        ecoles[ecoles_names[i_ecole]] -= montant
        if sirets[sirets_names[i_siret]] == 0:
            i_siret += 1
        if ecoles[ecoles_names[i_ecole]] == 0:
            i_ecole += 1
            while i_ecole < n_ecoles and ecoles_names[i_ecole] in liste_ecoles_30pct: i_ecole += 1
    
    # Création du dataframe avec les résultats
    new_df = pd.DataFrame(grid, columns=ecoles_names, index=sirets_names)
    
    # Affichage du dataframe sur Streamlit
    st.write(new_df)
