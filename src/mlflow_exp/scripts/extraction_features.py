import os
import json
import csv
from datetime import datetime
import re


print("Current working directory:", os.getcwd())
print("Files in the current directory:", os.listdir())

folder_path = '/app/data/bank'
extracted_data = []

print(f"Traitement des fichiers dans le dossier : {folder_path}")

for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.startswith('.'):
            continue  # Ignore hidden files like .DS_Store
        file_path = os.path.join(root, file_name)
        print(f"Traitement du fichier : {file_path}")
        if "reviews" in file_name:
            with open(file_path, 'r', encoding='utf-8') as file:
                data_list = json.load(file)
                for data in data_list:
                    bank_name = data.get("identifyingName", "")
                    extraction_date = datetime.strptime(data.get("extractionDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                    for review in data.get("reviews", []):
                        review_text = review.get("text", "").replace("\n", " ")
                        review_text = re.sub(r'\s+', ' ', review_text)
                        date_review = datetime.strptime(review.get("dates", {}).get("publishedDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                        rating = review.get("rating", "")
                        reply = review.get("reply", None)
                        reply_message = reply.get("message") if reply else None
                        reply_date = datetime.strptime(reply.get("publishedDate", "")[:10], "%Y-%m-%d").strftime("%d/%m/%Y") if reply else None
                        review_text = review_text.replace(";", ",")
                        reply_message = reply_message.replace(";", ",") if reply_message else None
                        extracted_data.append([bank_name, extraction_date, review_text, rating, date_review, "oui" if reply_message else "non", reply_date])

print(f"Nombre de lignes extraites : {len(extracted_data)}")

csv_file_path = "/app/apprentissage.csv"
if os.path.isdir(csv_file_path):
    os.rmdir(csv_file_path)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(["Nom_de_la_banque", "Date_de_l_extraction", "Review", "Evaluation", "date_review", "Reponse", "Date_reponse"])
    writer.writerows(extracted_data)

print(f"Fichier CSV généré à : {csv_file_path}")


