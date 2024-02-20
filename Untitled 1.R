# Charger la librairie tidyverse pour manipuler les données
library(tidyverse)

# Chemin vers le fichier CSV original
chemin_fichier_csv <- "rappel_conso.csv"

# Lire le fichier CSV original
donnees <- read_csv(chemin_fichier_csv)

# Modifier la colonne "risques_encourus_par_le_consommateur" pour regrouper les risques ensemble
donnees <- donnees %>%
  mutate(risques_encourus_par_le_consommateur = case_when(
    grepl("Salmonella", risques_encourus_par_le_consommateur) ~ "Salmonella",
    grepl("Listeria", risques_encourus_par_le_consommateur) ~ "Listeria",
    grepl("Bacillus", risques_encourus_par_le_consommateur) ~ "Bacillus",
    TRUE ~ "Autre"
  )) %>%
  filter(risques_encourus_par_le_consommateur != "Autre")  # Supprimer les lignes avec "Autre" comme risque

# Chemin pour sauvegarder le fichier CSV avec les risques regroupés
chemin_fichier_csv_risques <- "risques.csv"

# Écrire les données modifiées dans un nouveau fichier CSV
write_csv(donnees, chemin_fichier_csv_risques)

# Lire le fichier CSV des risques
donnees_risques <- read_csv(chemin_fichier_csv_risques)
