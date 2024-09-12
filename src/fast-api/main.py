import logging
import os
from fastapi import FastAPI
from elasticsearch import Elasticsearch, NotFoundError
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from typing import Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Réduire le niveau de journalisation pour Py4J
logger_py4j = logging.getLogger("py4j")
logger_py4j.setLevel(logging.WARN)

app = FastAPI()

# Route de test
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}

# Configuration Elasticsearch
ELASTIC_ADDRESS = os.getenv("ELASTIC_ADDRESS", "http://es-container:9200")
ELASTIC_INDEX = "reviews"
MODEL_PATH = "/app/modele_V1"

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Sentiment Analysis") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.sql.shuffle.partitions", "10") \
    .config("spark.sql.autoBroadcastJoinThreshold", -1) \
    .config("spark.network.timeout", "600s") \
    .config("spark.executor.heartbeatInterval", "100s") \
    .getOrCreate()

# Charger le modèle de prédiction
try:
    model = PipelineModel.load(MODEL_PATH)
    logger.info("Model loaded successfully from %s", MODEL_PATH)
except Exception as e:
    logger.error("Error loading model: %s", str(e))
    model = None

# Elasticsearch client
try:
    es = Elasticsearch(hosts=ELASTIC_ADDRESS)
    logger.info("Connected to Elasticsearch at %s", ELASTIC_ADDRESS)
except Exception as e:
    logger.error("Error connecting to Elasticsearch: %s", str(e))
    es = None

class PredictionRequest(BaseModel):
    limit: Optional[int] = None

class TestRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict_reviews(request: PredictionRequest):
    if not model:
        return {"error": "Model not loaded"}
    if not es:
        return {"error": "Elasticsearch not connected"}

    try:
        limit = request.limit or float('inf')  # Si aucune limite n'est définie, prendre tous les enregistrements
        logger.info("Received prediction request with limit: %s", limit)

        query = {
            "query": {"match_all": {}},
            "size": 100  # Taille du lot pour la pagination
        }

        response = es.search(index=ELASTIC_INDEX, body=query, scroll='1m')
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']

        predictions = []
        total_processed = 0

        while hits and total_processed < limit:
            batch_predictions = []

            for hit in hits:
                if total_processed >= limit:
                    break

                review_id = hit['_id']
                text = hit['_source']['text']
                logger.info("Processing review with id: %s", review_id)

                data = spark.createDataFrame([(text,)], ["text"])
                data = data.withColumnRenamed("text", "SentimentText")

                result = model.transform(data)
                prediction = result.collect()[0]['prediction']
                logger.info("Prediction for id %s: %s", review_id, prediction)

                batch_predictions.append({"id": review_id, "text": text, "prediction": prediction})
                total_processed += 1

            # Mise à jour des prédictions dans Elasticsearch
            for pred in batch_predictions:
                try:
                    es.update(
                        index=ELASTIC_INDEX,
                        id=pred['id'],
                        body={
                            "doc": {
                                "prediction": pred['prediction']
                            }
                        }
                    )
                except NotFoundError:
                    logger.error("Document with id %s not found in Elasticsearch. Skipping update.", pred['id'])

            if total_processed < limit:
                try:
                    response = es.scroll(scroll_id=scroll_id, scroll='1m')
                    scroll_id = response['_scroll_id']
                    hits = response['hits']['hits']
                except Exception as e:
                    logger.error("Error during scrolling: %s", str(e))
                    break

        return {"message": "Elasticsearch updated", "predictions_count": total_processed}

    except Exception as e:
        logger.error("Error during prediction: %s", str(e))
        return {"error": str(e)}

@app.post("/test")
async def test_model(request: TestRequest):
    if not model:
        return {"error": "Model not loaded"}

    try:
        logger.info("Received test request with text: %s", request.text)

        # Créer un DataFrame Spark pour la prédiction
        data = spark.createDataFrame([(request.text,)], ["text"])

        # Renommer la colonne pour correspondre à ce que le modèle attend
        data = data.withColumnRenamed("text", "SentimentText")

        # Effectuer la prédiction
        result = model.transform(data)
        prediction = result.collect()[0]['prediction']

        logger.info("Prediction for text: %s", prediction)

        return {"text": request.text, "prediction": prediction}

    except Exception as e:
        logger.error("Error during prediction: %s", str(e))
        return {"error": str(e)}

@app.get("/es_health")
async def es_health():
    try:
        health = es.cluster.health()
        return {"status": health['status']}
    except Exception as e:
        logger.error("Error connecting to Elasticsearch: %s", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
