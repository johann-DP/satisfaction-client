import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import pyspark.sql.functions as F

# Charger le modèle Spark
spark = SparkSession.builder \
    .appName("Sentiment Analysis") \
    .getOrCreate()

model_path = "modele_V1"
model = PipelineModel.load(model_path)

# Charger le fichier CSV
input_file = "apprentissage_light.csv"
df = spark.read.csv(input_file, header=True, sep=";")

# Renommer les colonnes
df = df.withColumnRenamed("Review", "SentimentText").withColumnRenamed("Evaluation", "label")

# Faire des prédictions
predictions = model.transform(df)

# Ajouter la colonne "Sentiment" basée sur les prédictions
predictions = predictions.withColumn("Sentiment", \
                    F.when(predictions["prediction"] >= 4, "positif") \
                    .when(predictions["prediction"] == 3, "neutre") \
                    .otherwise("negatif"))

# Sélectionner les colonnes nécessaires
predictions = predictions.select("Nom_de_la_banque", "Date_de_l_extraction", "SentimentText", "label", "date_review", "Reponse", "Date_reponse", "Sentiment")

# Enregistrer les prédictions dans un nouveau fichier CSV
output_file = "predictions.csv"
predictions.toPandas().to_csv(output_file, index=False)
