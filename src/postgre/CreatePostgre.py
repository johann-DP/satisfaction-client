import os
import json
import psycopg2

# Charger le fichier JSON
with open('/app/data/bank/companies/bank.json', 'r') as file:
    data = json.load(file)

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# Création des tables d'après le diagramme UML
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bank (
        businessUnitId VARCHAR PRIMARY KEY,
        identifyingName VARCHAR,
        displayName VARCHAR,
        logoUrl VARCHAR,
        numberOfReviews INTEGER,
        trustScore FLOAT,
        isRecommendedInCategories BOOLEAN
    );
    CREATE TABLE IF NOT EXISTS Location (
        locationId SERIAL PRIMARY KEY,
        address VARCHAR,
        city VARCHAR,
        zipCode VARCHAR,
        country VARCHAR,
        businessUnitId VARCHAR REFERENCES Bank(businessUnitId)
    );
    CREATE TABLE IF NOT EXISTS Contact (
        contactId SERIAL PRIMARY KEY,
        website VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        businessUnitId VARCHAR REFERENCES Bank(businessUnitId)
    );
    CREATE TABLE IF NOT EXISTS Category (
        categoryId VARCHAR PRIMARY KEY,
        displayName VARCHAR,
        isPredicted BOOLEAN,
        businessUnitId VARCHAR REFERENCES Bank(businessUnitId)
    );
    CREATE TABLE IF NOT EXISTS BankCategory (
        businessUnitId VARCHAR,
        categoryId VARCHAR,
        PRIMARY KEY (businessUnitId, categoryId),
        FOREIGN KEY (businessUnitId) REFERENCES Bank(businessUnitId),
        FOREIGN KEY (categoryId) REFERENCES Category(categoryId)
    );
""")
conn.commit()

# Insertion des données dans les tables
for entry in data:
    # Insertion dans la table Bank
    cursor.execute("""
        INSERT INTO Bank (businessUnitId, identifyingName, displayName, logoUrl, numberOfReviews, trustScore, isRecommendedInCategories)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (businessUnitId) DO NOTHING;
    """, (entry['businessUnitId'], entry['identifyingName'], entry['displayName'], entry['logoUrl'], entry['numberOfReviews'], entry['trustScore'], entry['isRecommendedInCategories']))

    # Insertion dans la table Location
    cursor.execute("""
        INSERT INTO Location (address, city, zipCode, country, businessUnitId)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (locationId) DO NOTHING;
    """, (entry['location']['address'], entry['location']['city'], entry['location']['zipCode'], entry['location']['country'], entry['businessUnitId']))

    # Insertion dans la table Contact
    cursor.execute("""
        INSERT INTO Contact (website, email, phone, businessUnitId)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (contactId) DO NOTHING;
    """, (entry['contact']['website'], entry['contact']['email'], entry['contact']['phone'], entry['businessUnitId']))

    # Insertion dans la table Category
    for category in entry['categories']:
        cursor.execute("""
            INSERT INTO Category (categoryId, displayName, isPredicted, businessUnitId)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (categoryId) DO NOTHING;
        """, (category['categoryId'], category['displayName'], category['isPredicted'], entry['businessUnitId']))

        # Insertion dans la table de jointure BankCategory
        cursor.execute("""
            INSERT INTO BankCategory (businessUnitId, categoryId)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (entry['businessUnitId'], category['categoryId']))

conn.commit()
conn.close()
