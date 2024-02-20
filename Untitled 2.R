# Charger la librairie tidyverse pour manipuler les données
library(tidyverse)

# Chemin vers le fichier CSV original
chemin_fichier_csv <- "rappel_conso.csv"

# Lire le fichier CSV original
donnees <- read_csv(chemin_fichier_csv)

# Obtenir les différents types de risques encourus par le consommateur
types_de_risques <- unique(donnees$risques_encourus_par_le_consommateur)

# Afficher les différents types de risques
print(types_de_risques)

# Sélectionner les types de risques microbiologiques
microbiologiques <- types_de_risques[str_detect(types_de_risques, "Salmonella|Listeria|Bacillus")]

# Afficher les types de risques microbiologiques
print(microbiologiques)
