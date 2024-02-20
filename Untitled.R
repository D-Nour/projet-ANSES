# Charger la librairie tidyverse pour manipuler les données
library(tidyverse)

# Chemin vers le fichier TXT
chemin_fichier_txt <- "rappel_conso.txt"

# Lire le fichier TXT en utilisant la fonction read_table de la librairie readr
donnees <- read_delim(chemin_fichier_txt, delim = "\t", locale = locale(encoding = "UTF-16LE"))

# Modifier la colonne "risques_encourus_par_le_consommateur"
donnees_nettoyees <- donnees %>%
  mutate(risques_encourus_par_le_consommateur = if_else(str_detect(risques_encourus_par_le_consommateur, "Escherichia coli shiga toxinogène (STEC) Listeria monocytogenes"), "STEC", risques_encourus_par_le_consommateur))

# Modifier la colonne "risques_encourus_par_le_consommateur" pour supprimer les parties spécifiques
donnees_nettoyees <- donnees_nettoyees %>%
  mutate(risques_encourus_par_le_consommateur = gsub("\\(agent responsable de la salmonellose\\)|\\(agent responsable de la listériose\\)", "", risques_encourus_par_le_consommateur))

# Sélectionner les colonnes spécifiées
donnees_nettoyees <- select(donnees_nettoyees, categorie_de_produit, sous_categorie_de_produit, risques_encourus_par_le_consommateur, nom_de_la_marque_du_produit, date_debut_fin_de_commercialisation, distributeurs, motif_du_rappel)

# Chemin pour sauvegarder le fichier CSV
chemin_fichier_csv <- "rappel_conso.csv"

# Écrire les données dans un fichier CSV en utilisant la fonction write_csv de la librairie readr
write_csv(donnees_nettoyees, chemin_fichier_csv)
