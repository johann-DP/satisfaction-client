import os
import json
import csv
from datetime import datetime
import re  # Importer le module de expressions régulières

# Chemin vers le dossier contenant les fichiers JSON
folder_path = "/Users/mercier/git_depo/projet_DS/projet_DST_satisfaction_client/data/bank"

# Liste pour stocker les données extraites
extracted_data = []

# Parcour des fichiers dans le dossier
for file_name in os.listdir(folder_path):
    if "reviews" in file_name:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
            for data in data_list:
                bank_name = data.get("identifyingName", "")
                extraction_date = datetime.strptime(data.get("extractionDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                for review in data.get("reviews", []):
                    review_text = review.get("text", "")  # Extraire le texte de l'examen
                    # Remplacer les caractères de nouvelle ligne par un espace
                    review_text = review_text.replace("\n", " ")
                    # Remplacer les espaces multiples par un seul espace
                    review_text = re.sub(r'\s+', ' ', review_text)
                    date_review = datetime.strptime(review.get("dates", {}).get("publishedDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                    rating = review.get("rating", "")
                    reply = review.get("reply", None)
                    reply_message = reply.get("message") if reply else None
                    reply_date = datetime.strptime(reply.get("publishedDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y") if reply else None
                    # Remplacer les points-virgules par des virgules dans les données
                    review_text = review_text.replace(";", ",")
                    reply_message = reply_message.replace(";", ",") if reply_message else None
                    extracted_data.append([bank_name, extraction_date, review_text, rating, date_review, "oui" if reply_message else "non", reply_date])

# Écriture des données extraites dans un fichier CSV avec des virgules comme délimiteur
with open("/Users/mercier/git_depo/projet_DS/projet_DST_satisfaction_client/apprentissage_test.csv", 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')  # Utiliser une virgule comme délimiteur
    writer.writerow(["Nom_de_la_banque", "Date_de_l_extraction", "Review", "Evaluation", "date_review", "Reponse", "Date_reponse"])
    writer.writerows(extracted_data)
