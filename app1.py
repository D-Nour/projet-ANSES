import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Fonction pour charger les données
def charger_donnees():
    chemin_fichier_csv = "rappel_conso.csv"
    donnees = pd.read_csv(chemin_fichier_csv)
    return donnees

# Charger les données
@st.cache_data
def charger_donnees():
    chemin_fichier_csv = "risques.csv"
    donnees = pd.read_csv(chemin_fichier_csv)
    
    # Effectuer toute modification nécessaire des données ici
    
    return donnees.copy() 

# Fonction pour créer le diagramme en barre avec les 5 sous-catégories de produits ayant les risques spécifiés
def diagramme_barre_sous_cat(donnees_filtrees, risques):
    # Filtrer les données pour inclure uniquement les risques spécifiés
    donnees_filtrees = donnees_filtrees[donnees_filtrees['risques_encourus_par_le_consommateur'].str.contains(risques, na=False)]

    # Compter le nombre de risques par sous-catégorie de produit et trier par ordre décroissant
    risques_par_sous_categorie = donnees_filtrees['sous_categorie_de_produit'].value_counts().sort_values(ascending=False)

    # Calculer le pourcentage de risques pour chaque sous-catégorie de produit
    pourcentages = (risques_par_sous_categorie / len(donnees_filtrees)) * 100

    # Créer le graphique en barres
    fig = px.bar(pourcentages, x=pourcentages.index, y=pourcentages.values, color=pourcentages.values, title=f'Sous-catégories de produits avec Risques encourus par le consommateur ({risques})')

    # Ajouter les pourcentages comme données supplémentaires au survol de la souris
    fig.update_traces(hovertemplate='%{y:.2f}%')

    # Définir une taille plus grande pour le graphique
    fig.update_layout(height=600, width=1000, xaxis_title="Sous-catégorie de produit", yaxis_title="Pourcentage de risques")

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title('Visualisation de la base de données nettoyée')

# Charger les données
donnees = charger_donnees()

# Afficher les données
st.write(donnees)



###################################################################################################################################################

# Fonction pour charger les données
def charger_donnees():
    chemin_fichier_csv = "risques.csv"
    donnees_risques = pd.read_csv(chemin_fichier_csv)
    return donnees_risques

# Fonction pour remplacer les valeurs non valides par "Sans Marque"
def remplacer_valeurs_non_valides(data):
    # Liste des valeurs non valides
    valeurs_non_valides = ['/', '_', '-', '.', '#NOM?', "'Sans Marque'", '', 'sans marque', 'SANS MARQUE','Sans-Marque', 'SANS', 'sans', 'Sans']
    
     # Expression régulière pour rechercher "Sans Marque" dans différentes variantes
    regex_sans_marque = re.compile(r'(sans\s*\(.*\)|sans\s*marque)', flags=re.IGNORECASE)
    
    # Appliquer les remplacements
    data['nom_de_la_marque_du_produit'] = data['nom_de_la_marque_du_produit'].apply(lambda x: 'Sans Marque' if (isinstance(x, float) and pd.isnull(x)) or (isinstance(x, str) and (x.strip() in valeurs_non_valides or regex_sans_marque.search(x))) else x) 
    return data


# Titre de l'application
st.title('Remplacement des valeurs non valides dans la colonne')

# Charger les données
donnees= charger_donnees()


# Remplacer les valeurs non valides
donnees = remplacer_valeurs_non_valides(donnees)

# Afficher les données après le remplacement
st.write("Après le remplacement :")
st.write(donnees)



###################################################################################################################################################



# Fonction pour créer le diagramme à barres avec un dégradé de couleur, une taille plus grande et les pourcentages au survol
def diagramme_barres_risques_encourus(donnees, risque_selectionne):
    # Filtrer les données en fonction du risque sélectionné
    donnees_filtrees = donnees[donnees['risques_encourus_par_le_consommateur'] == risque_selectionne]
    
    # Calculer les pourcentages
    total_par_marque = donnees_filtrees.groupby('nom_de_la_marque_du_produit').size()
    pourcentages = (total_par_marque / total_par_marque.sum()) * 100
    
    # Trier les marques par ordre décroissant de pourcentage
    top_marques = pourcentages.sort_values(ascending=False)
    
    # Sélectionner les 20 premières marques
    top_20_marques = top_marques.head(20)
    
    # Créer le diagramme à barres avec les 20 premières marques et un dégradé de couleur
    fig = px.bar(x=top_20_marques.index, y=top_20_marques.values, 
                 title=f"Les 20 premières marques avec les pourcentages de risque les plus élevés ({risque_selectionne})",
                 labels={'x': 'Marque de produit', 'y': 'Pourcentage'},
                 color=top_20_marques.values,
                 color_continuous_scale='Blues')  # Palette de couleurs pour le dégradé
    
    # Définir une taille plus grande pour le diagramme
    fig.update_layout(height=800, width=1000)
    
    # Ajouter les pourcentages comme données supplémentaires au survol de la souris
    fig.update_traces(hovertemplate='Pourcentage: %{y:.2f}%')
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title('Risques encourus par le consommateur pour les marques de produits')

# Charger les données
donnees = charger_donnees()

# Remplacer les valeurs non valides
donnees = remplacer_valeurs_non_valides(donnees)


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################

# Fonction pour créer le tableau de regroupement des marques avec le même pourcentage de risques
def tableau_regroupement_marques(donnees, risque_selectionne):
    # Filtrer les données en fonction du risque sélectionné
    donnees_filtrees = donnees[donnees['risques_encourus_par_le_consommateur'] == risque_selectionne]
    
    # Calculer les pourcentages
    total_par_marque = donnees_filtrees['nom_de_la_marque_du_produit'].value_counts()
    pourcentages = (total_par_marque / total_par_marque.sum()) * 100
    
    # Créer un DataFrame avec les pourcentages et le nombre de produits
    df_pourcentages = pd.DataFrame({'Marque de produit': pourcentages.index, 'Pourcentage': pourcentages.values})
    
    # Trier les données en fonction des pourcentages et du nombre de produits
    df_pourcentages = df_pourcentages.sort_values(by=['Pourcentage', 'Marque de produit'], ascending=False)
    
    # Afficher le tableau sans la colonne Groupe
    st.write(df_pourcentages[['Marque de produit', 'Pourcentage']])

# Titre de l'application
st.title('Risques encourus par le consommateur pour les marques de produits')

# Charger les données
donnees = charger_donnees()

# Remplacer les valeurs non valides
donnees = remplacer_valeurs_non_valides(donnees)


###################################################################################################################################################
###################################################################################################################################################

###################################################################################################################################################
###################################################################################################################################################

# Fonction pour extraire les dates de début de commercialisation
def extraire_dates_commercialisation(donnees):
    # Extraire les dates de début de commercialisation
    donnees['Date debut'] = pd.to_datetime(donnees['date_debut_fin_de_commercialisation'].str.extract(r'Du (\d{2}/\d{2}/\d{4})', expand=False), format='%d/%m/%Y')
    return donnees

# Fonction pour créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
def diagramme_pourcentage_distribution_par_mois(donnees):
    # Grouper les données par année et par mois
    donnees['Annee'] = donnees['Date debut'].dt.year.fillna(0).astype(int)  # Remplacer les NaN par 0 avant de convertir en entier
    donnees['Mois'] = donnees['Date debut'].dt.month_name()
    donnees_groupes = donnees.groupby(['Annee', 'Mois'])
    
    # Calculer le nombre de produits pour chaque mois de chaque année
    nb_produits_par_mois = donnees_groupes.size().unstack(fill_value=0)
    
    # Calculer le pourcentage de distribution pour chaque mois de chaque année
    pourcentage_distribution_par_mois = (nb_produits_par_mois.div(nb_produits_par_mois.sum(axis=1), axis=0) * 100).stack().reset_index(name='Pourcentage')
    
    # Créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
    fig = px.line(pourcentage_distribution_par_mois, x='Mois', y='Pourcentage', color='Annee',
                  title="Pourcentage de distribution au fil des mois pour chaque année",
                  labels={'Mois': "Mois", 'Pourcentage': 'Pourcentage de distribution (%)', 'Annee': 'Année'})
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title("Analyse du pourcentage de distribution au fil des mois pour chaque année")

# Charger les données
donnees = charger_donnees()

# Extraire les dates de début de commercialisation
donnees = extraire_dates_commercialisation(donnees)

# Afficher le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
diagramme_pourcentage_distribution_par_mois(donnees)

###################################################################################################################################################

# Fonction pour extraire les dates de début de commercialisation
def extraire_dates_commercialisation(donnees):
    # Extraire les dates de début de commercialisation
    donnees['Date debut'] = pd.to_datetime(donnees['date_debut_fin_de_commercialisation'].str.extract(r'Du (\d{2}/\d{2}/\d{4})', expand=False), format='%d/%m/%Y')
    return donnees

# Fonction pour créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
def diagramme_pourcentage_distribution_par_mois(donnees, risque_selectionne):
    # Grouper les données par année et par mois
    donnees['Annee'] = donnees['Date debut'].dt.year.fillna(0).astype(int)  # Remplacer les NaN par 0 avant de convertir en entier
    donnees['Mois'] = donnees['Date debut'].dt.month_name()
    donnees_groupes = donnees.groupby(['Annee', 'Mois'])
    
    # Filtrer les données en fonction du risque sélectionné
    donnees_filtrees = donnees[donnees['risques_encourus_par_le_consommateur'] == risque_selectionne]
    
    # Calculer le nombre de produits pour chaque mois de chaque année
    nb_produits_par_mois = donnees_filtrees.groupby(['Annee', 'Mois']).size().unstack(fill_value=0)
    
    # Calculer le pourcentage de distribution pour chaque mois de chaque année
    pourcentage_distribution_par_mois = (nb_produits_par_mois.div(nb_produits_par_mois.sum(axis=1), axis=0) * 100).stack().reset_index(name='Pourcentage')
    
    # Créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
    fig = px.line(pourcentage_distribution_par_mois, x='Mois', y='Pourcentage', color='Annee',
                  title=f"Pourcentage de distribution au fil des mois pour chaque année ({risque_selectionne})",
                  labels={'Mois': "Mois", 'Pourcentage': 'Pourcentage de distribution (%)', 'Annee': 'Année'})
    
    # Ajouter une droite pour voir l'évolution des risques
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil de risque", annotation_position="top left")
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title("Analyse du pourcentage de distribution au fil des mois pour chaque année")

# Charger les données
donnees = charger_donnees()

# Extraire les dates de début de commercialisation
donnees = extraire_dates_commercialisation(donnees)

# Obtenir la liste des risques disponibles
liste_risques = donnees['risques_encourus_par_le_consommateur'].unique()

# Menu déroulant pour choisir le risque
risque_selectionne = st.selectbox("Choisir le risque à analyser:", liste_risques)

# Afficher le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
diagramme_pourcentage_distribution_par_mois(donnees, risque_selectionne)
###################################################################################################################################################


# Fonction pour charger les données
def charger_donnees():
    chemin_fichier_csv = "rappel_conso.csv"
    donnees = pd.read_csv(chemin_fichier_csv)
    return donnees

# Fonction pour extraire les dates de début de commercialisation
def extraire_dates_commercialisation(donnees):
    # Extraire les dates de début de commercialisation
    donnees['Date debut'] = pd.to_datetime(donnees['date_debut_fin_de_commercialisation'].str.extract(r'Du (\d{2}/\d{2}/\d{4})', expand=False), format='%d/%m/%Y')
    return donnees

# Fonction pour créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
def diagramme_pourcentage_distribution_par_mois(donnees, risque_selectionne):
    # Grouper les données par année et par mois
    donnees['Annee'] = donnees['Date debut'].dt.year.fillna(0).astype(int)  # Remplacer les NaN par 0 avant de convertir en entier
    donnees['Mois'] = donnees['Date debut'].dt.month_name()
    donnees_groupes = donnees.groupby(['Annee', 'Mois'])
    
    # Filtrer les données en fonction du risque sélectionné
    donnees_filtrees = donnees[donnees['risques_encourus_par_le_consommateur'] == risque_selectionne]
    
    # Calculer le nombre de produits pour chaque mois de chaque année
    nb_produits_par_mois = donnees_filtrees.groupby(['Annee', 'Mois']).size().unstack(fill_value=0)
    
    # Calculer le pourcentage de distribution pour chaque mois de chaque année
    pourcentage_distribution_par_mois = (nb_produits_par_mois.div(nb_produits_par_mois.sum(axis=1), axis=0) * 100).stack().reset_index(name='Pourcentage')
    
    # Créer le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
    fig = px.line(pourcentage_distribution_par_mois, x='Mois', y='Pourcentage', color='Annee',
                  title=f"Pourcentage de distribution au fil des mois pour chaque année ({risque_selectionne})",
                  labels={'Mois': "Mois", 'Pourcentage': 'Pourcentage de distribution (%)', 'Annee': 'Année'})
    
    # Ajouter une droite pour voir l'évolution des risques
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil de risque", annotation_position="top left")
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title("Analyse du pourcentage de distribution au fil des mois pour chaque année")

# Charger les données
donnees = charger_donnees()

# Extraire les dates de début de commercialisation
donnees = extraire_dates_commercialisation(donnees)

# Obtenir la liste des risques disponibles
liste_risques = donnees['risques_encourus_par_le_consommateur'].unique()

# Menu déroulant pour choisir le risque
risque_selectionne = st.selectbox("Choisir le risque à analyser:", liste_risques)

# Afficher le diagramme courbe du pourcentage de distribution au fil des mois pour chaque année
diagramme_pourcentage_distribution_par_mois(donnees, risque_selectionne)

###################################################################################################################################################


# Fonction pour charger les données
def charger_donnees():
    chemin_fichier_csv = "rappel_conso.csv"
    donnees = pd.read_csv(chemin_fichier_csv)
    return donnees

# Calculer les pourcentages pour chaque catégorie de risque
total = len(donnees)
risques_microbiologiques = donnees[donnees['risques_encourus_par_le_consommateur'].str.contains('Salmonella|Listeria|Bacillus', case=False, regex=True)]
total_microbiologique = len(risques_microbiologiques)
pourcentage_microbiologique = (total_microbiologique / total) * 100
pourcentage_autre = 100 - pourcentage_microbiologique

# Créer un dataframe pour les pourcentages
data = {
    "Risque": ["Microbiologiques", "Autre"],
    "Pourcentage": [pourcentage_microbiologique, pourcentage_autre]
}

df = pd.DataFrame(data)

# Créer un diagramme à barres
fig, ax = plt.subplots()
ax.bar(df["Risque"], df["Pourcentage"])
ax.set_xlabel("Risque")
ax.set_ylabel("Pourcentage")
ax.set_title("Pourcentage de risques microbiologiques")

# Afficher le diagramme dans Streamlit
st.pyplot(fig)

# Fonction pour créer le diagramme circulaire
def diagramme_circulaire(donnees):
    # Regrouper les types de risques microbiologiques ensemble
    donnees['risques_groupes'] = 'Autre'
    donnees.loc[donnees['risques_encourus_par_le_consommateur'].str.contains('Salmonella'), 'risques_groupes'] = 'Salmonella'
    donnees.loc[donnees['risques_encourus_par_le_consommateur'].str.contains('Listeria'), 'risques_groupes'] = 'Listeria'
    donnees.loc[donnees['risques_encourus_par_le_consommateur'].str.contains('Bacillus'), 'risques_groupes'] = 'Bacillus'

    # Calculer les pourcentages des risques encourus par le consommateur
    pourcentages = donnees['risques_groupes'].value_counts(normalize=True) * 100

    # Créer le diagramme circulaire interactif avec Plotly
    fig = px.pie(names=pourcentages.index, values=pourcentages.values,
                 title="Pourcentage des risques encourus par le consommateur",
                 labels={'names': 'Risques', 'values': 'Pourcentage'},
                 hole=0)  # Spécifier un trou de taille nulle pour un cercle complet

    # Afficher le diagramme interactif
    st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title('Visualisation des risques encourus par le consommateur')

# Charger les données
donnees = pd.read_csv("rappel_conso.csv")  # Remplacez "votre_fichier.csv" par le chemin de votre fichier CSV contenant les données

# Afficher le diagramme circulaire pour les risques spécifiés
diagramme_circulaire(donnees)


# Fonction pour charger les données
def charger_donnees():
    chemin_fichier_csv = "risques.csv"
    donnees = pd.read_csv(chemin_fichier_csv)
    # Créer une copie des données pour éviter toute modification ultérieure
    donnees_copy = donnees.copy()
    return donnees_copy

# Charger les données
donnees = st.cache_data(charger_donnees)

# Fonction pour remplacer les valeurs non valides par "Sans Marque"
def remplacer_valeurs_non_valides(data):
    # Liste des valeurs non valides
    valeurs_non_valides = ['/', '_', '-', '.', '#NOM?', "'Sans Marque'", '', 'sans marque', 'SANS MARQUE', 'Sans-Marque', 'SANS', 'sans', 'Sans']
    
    # Expression régulière pour rechercher "Sans Marque" dans différentes variantes
    regex_sans_marque = re.compile(r'(sans\s*\(.*\)|sans\s*marque)', flags=re.IGNORECASE)
    
    # Appliquer les remplacements
    data['nom_de_la_marque_du_produit'] = data['nom_de_la_marque_du_produit'].apply(lambda x: 'Sans Marque' if (isinstance(x, float) and pd.isnull(x)) or (isinstance(x, str) and (x.strip() in valeurs_non_valides or regex_sans_marque.search(x))) else x) 
    return data

# Charger les données
donnees = charger_donnees()

# Remplacer les valeurs non valides
donnees = remplacer_valeurs_non_valides(donnees)

# Calculer les pourcentages pour chaque catégorie de risque
pourcentages = donnees.groupby('nom_de_la_marque_du_produit')['risques_encourus_par_le_consommateur'].value_counts(normalize=True).unstack().fillna(0) * 100

# Reformater les données pour le tracé du nuage de points
pourcentages.reset_index(inplace=True)
pourcentages = pourcentages.melt(id_vars='nom_de_la_marque_du_produit', var_name='Risque', value_name='Pourcentage')

# Trier les marques par nombre total de risques décroissant
top_30_marques = donnees['nom_de_la_marque_du_produit'].value_counts().nlargest(30).index
pourcentages = pourcentages[pourcentages['nom_de_la_marque_du_produit'].isin(top_30_marques)]

# Créer le nuage de points avec Plotly Express
fig = px.scatter(pourcentages, x='nom_de_la_marque_du_produit', y='Pourcentage', color='Risque', title="Pourcentage de risques encourus par le consommateur selon la marque du produit en nuage")
fig.update_layout(xaxis_title="Nom de la marque du produit", yaxis_title="Pourcentage de risques")
st.plotly_chart(fig, use_container_width=True)

# Titre de l'application
st.title('Pourcentage de risques microbiologiques par marque de produit en nuage')









#####################################################

# Page d'accueil
def page_accueil():
    st.title("Bienvenue sur notre application")

    st.write("""
    Cette application propose différentes fonctionnalités pour visualiser des données et accéder à des ressources sur les bases de données.
    """)

def page_selection_diagramme():
    st.title("Types de diagrammes")

    choix_diagramme = st.selectbox("Sélectionnez le type de diagramme :", [
        "Sous-catégories de produits avec Risques encourus par le consommateur",
        "Risques encourus par le consommateur pour les marques de produits",
        "Analyse du pourcentage de distribution au fil des mois pour chaque année",
        "Visualisation des risques encourus par le consommateur",
        "Pourcentage de risques microbiologiques par marque de produit en nuage"
    ])

    return choix_diagramme

def page_diagrammes(choix_diagramme):
    donnees = charger_donnees()  # Chargement des données une fois pour toute l'application

    if choix_diagramme == "Sous-catégories de produits avec Risques encourus par le consommateur":
        risque = st.selectbox("Choisir le type de risque :", ["Salmonella", "Listeria", "Bacillus"])
        # Liste des risques encourus par le consommateur
        liste_risques = ['Salmonella', 'Listeria', 'Bacillus']

        # Menu déroulant pour choisir le type de risques
        risques_choisis = st.selectbox('Choisir le type de risques encourus par le consommateur :', liste_risques)

        # Afficher le diagramme en barres pour les risques choisis
        diagramme_barre_sous_cat(donnees, risques_choisis)
    elif choix_diagramme == "Risques encourus par le consommateur pour les marques de produits":
        risque = st.selectbox("Choisir le type de risque :", ["Salmonella", "Listeria", "Bacillus"])
        # Menu déroulant pour choisir le risque
        risque_selectionne = st.selectbox("Choisir le type de risque:", ["Listeria", "Salmonella", "Bacillus"])

        # Afficher le diagramme à barres
        diagramme_barres_risques_encourus(donnees, risque_selectionne)
    elif choix_diagramme == "Risques encourus par le consommateur pour les marques de produits 2":

        # Menu déroulant pour choisir le risque (ajout d'une partie du nom de la fonction comme clé)
        risque_selectionne = st.selectbox("Choisir le type de risque:", ["Listeria", "Salmonella", "Bacillus"], key="selectbox_risque")

        # Afficher le tableau de regroupement des marques (ajout d'une partie du nom de la fonction comme clé)
        tableau_regroupement_marques(donnees, risque_selectionne)

        tableau_regroupement_marques(donnees, risque)
    elif choix_diagramme == "Analyse du pourcentage de distribution au fil des mois pour chaque année":
        diagramme_pourcentage_distribution_par_mois(donnees)
    elif choix_diagramme == "Visualisation des risques encourus par le consommateur":
        st.write("Visualisation des risques encourus par le consommateur")
        diagramme_circulaire(donnees)
    elif choix_diagramme == "Pourcentage de risques microbiologiques par marque de produit en nuage":
        remplacer_valeurs_non_valides(donnees)

# Page ressources pour afficher les bases de données
def page_ressources():
    st.title("Ressources sur les bases de données")

    st.write("""
    Vous trouverez ici des liens et des informations sur les bases de données.
    """)
    st.write("""
    - [Nom de la base de données 1](lien_vers_la_base_de_donnees_1)
    - [Nom de la base de données 2](lien_vers_la_base_de_donnees_2)
    """)

# Menu principal
def main():
    st.sidebar.title("Menu")
    choix_page = st.sidebar.selectbox("Choisir une page :", ["Accueil", "Diagrammes", "Ressources"])

    choix_diagramme = None
    if choix_page == "Diagrammes":
        choix_diagramme = st.sidebar.selectbox("Sélectionnez le type de diagramme :", [
            "Sous-catégories de produits avec Risques encourus par le consommateur",
            "Risques encourus par le consommateur pour les marques de produits",
            "Analyse du pourcentage de distribution au fil des mois pour chaque année",
            "Visualisation des risques encourus par le consommateur",
            "Pourcentage de risques microbiologiques par marque de produit en nuage"
        ])

    if choix_page == "Accueil":
        page_accueil()
    elif choix_page == "Diagrammes":
        page_diagrammes(choix_diagramme)
    elif choix_page == "Ressources":
        page_ressources()

if __name__ == "__main__":
    main()
