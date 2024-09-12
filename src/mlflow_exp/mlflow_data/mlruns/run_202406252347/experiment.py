import mlflow
import mlflow.spark
from mlflow.tracking import MlflowClient
from datetime import datetime
import argparse
import os
import shutil
import nltk
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

parser = argparse.ArgumentParser(description='Sentiment Analysis with Spark and MLflow')
parser.add_argument('--port', type=int, default=8080, help='Port for MLflow tracking server')
args = parser.parse_args()

tracking_uri = f"http://localhost:{args.port}"
mlflow.set_tracking_uri(tracking_uri)
experiment_name = "Sentiment_Analysis"
mlflow.set_experiment(experiment_name)

# Configuration Spark avec augmentation de la mémoire
spark = SparkSession.builder \
    .appName("Sentiment Analysis") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

schema = StructType([
    StructField("Nom_de_la_banque", StringType(), True),
    StructField("Date_de_l_extraction", StringType(), True),
    StructField("Review", StringType(), True),
    StructField("Evaluation", IntegerType(), True),
    StructField("date_review", StringType(), True),
    StructField("Reponse", StringType(), True),
    StructField("Date_reponse", StringType(), True)
])

trainDataset = spark.read.option("header", True).option("delimiter", ";").schema(schema).csv("/app/apprentissage.csv")

trainDataset = trainDataset.na.fill({"Evaluation": -1})
data = trainDataset.select("Review", "Evaluation").withColumnRenamed('Review', 'SentimentText').withColumnRenamed('Evaluation', 'label')
data = data.withColumn("label", col("label").cast(IntegerType()))

train, validation, test = data.randomSplit([0.6, 0.2, 0.2])

tokenizer = Tokenizer(inputCol="SentimentText", outputCol="SentimentWords")
stopwordList = nltk.corpus.stopwords.words('french')
additional_stopwords = [
    # (additional stopwords)
]
stopwordList.extend(additional_stopwords)
swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="MeaningfulWords", stopWords=stopwordList)
hashTF = HashingTF(inputCol=swr.getOutputCol(), outputCol="features")

lr = LogisticRegression(maxIter=500, regParam=0.01, family="multinomial")
pipeline = Pipeline(stages=[tokenizer, swr, hashTF, lr])

current_time = datetime.now().strftime("%Y%m%d%H%M")
run_name = f"run_{current_time}"
script_path = "/app/scripts/experiment.py"

def validate_model(model, validation_data):
    predictions = model.transform(validation_data)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", labelCol="label", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    precision = evaluator.evaluate(predictions, {evaluator.metricName: "weightedPrecision"})
    recall = evaluator.evaluate(predictions, {evaluator.metricName: "weightedRecall"})
    f1_score = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
    if accuracy >= 0.75 and precision >= 0.70 and recall >= 0.70 and f1_score >= 0.70:
        return True
    return False

client = MlflowClient()
model_name = "SentimentAnalysisModel"
try:
    client.get_registered_model(model_name)
except mlflow.exceptions.RestException:
    client.create_registered_model(model_name)

with mlflow.start_run(run_name=run_name) as run:
    mlflow.log_params({"maxIter": 500, "regParam": 0.01, "family": "multinomial"})
    mlflow.set_tag("model_type", "LogisticRegression")
    mlflow.log_artifact(script_path, artifact_path="scripts")
    model = pipeline.fit(train)
    predictions = model.transform(test)
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", labelCol="label", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    precision = evaluator.evaluate(predictions, {evaluator.metricName: "weightedPrecision"})
    recall = evaluator.evaluate(predictions, {evaluator.metricName: "weightedRecall"})
    f1_score = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("test_precision", precision)
    mlflow.log_metric("test_recall", recall)
    mlflow.log_metric("test_f1_score", f1_score)
    model_uri = "spark-model"
    mlflow.spark.log_model(model, model_uri)
    model_version = client.create_model_version(
        name=model_name,
        source=f"runs:/{run.info.run_id}/{model_uri}",
        run_id=run.info.run_id
    )
    client.update_model_version(
        name=model_name,
        version=model_version.version,
        description="Model version in Staging"
    )
    client.set_model_version_tag(
        name=model_name,
        version=model_version.version,
        key="stage",
        value="Staging"
    )
    if validate_model(model, validation):
        client.update_model_version(
            name=model_name,
            version=model_version.version,
            description="Model version in Production"
        )
        client.set_model_version_tag(
            name=model_name,
            version=model_version.version,
            key="stage",
            value="Production"
        )
        print("Le modèle a été promu en Production.")
    else:
        print("La validation du modèle a échoué.")
    final_model_uri = f"runs:/{run.info.run_id}/"
    mlflow.spark.save_model(model, final_model_uri)
    mlflow.log_artifact(script_path, artifact_path="scripts")
    model_version = client.create_model_version(
        name=model_name,
        source=f"runs:/{run.info.run_id}/",
        run_id=run.info.run_id
    )
    client.update_model_version(
        name=model_name,
        version=model_version.version,
        description="Final model version"
    )
    client.set_model_version_tag(
        name=model_name,
        version=model_version.version,
        key="stage",
        value="Production"
    )
    print("Le modèle final a été enregistré et promu en Production.")
    
    local_run_dir = f"/app/mlflow_data/mlruns/{run_name}"
    os.makedirs(local_run_dir, exist_ok=True)
    shutil.copy(script_path, os.path.join(local_run_dir, "experiment.py"))
    print(f"Script Python copié dans {local_run_dir}")
    source_sparkml_dir = f"/app/runs:/{run.info.run_id}/sparkml"
    dest_sparkml_dir_name = f"MODELE_{current_time}"
    dest_sparkml_dir = os.path.join(local_run_dir, dest_sparkml_dir_name)
    if os.path.exists(source_sparkml_dir):
        shutil.copytree(source_sparkml_dir, dest_sparkml_dir)
        print(f"Dossier sparkml copié et renommé en {dest_sparkml_dir}")
    else:
        print(f"Le dossier {source_sparkml_dir} n'existe pas. Vérifiez le chemin.")

print("Expérience terminée.")