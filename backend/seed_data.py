print(" Script démarré...")

import oracledb
from faker import Faker
import random
import sys
sys.path.append(".")

from app.config import settings

fake = Faker('fr_FR')

def get_connection():
    print("Connexion Oracle...")
    conn = oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=settings.oracle_dsn
    )
    print(" Oracle connecté!")
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    tables = {
        "CUSTOMERS": """CREATE TABLE bilal.CUSTOMERS (
            id NUMBER PRIMARY KEY,
            nom VARCHAR2(100),
            email VARCHAR2(100),
            ville VARCHAR2(50),
            date_inscription DATE
        )""",
        "PRODUCTS": """CREATE TABLE bilal.PRODUCTS (
            id NUMBER PRIMARY KEY,
            nom VARCHAR2(100),
            prix NUMBER(10,2),
            categorie VARCHAR2(50),
            stock NUMBER
        )""",
        "ORDERS": """CREATE TABLE bilal.ORDERS (
            id NUMBER PRIMARY KEY,
            customer_id NUMBER,
            date_commande DATE,
            montant NUMBER(10,2),
            statut VARCHAR2(20)
        )""",
        "PAYMENTS": """CREATE TABLE bilal.PAYMENTS (
            id NUMBER PRIMARY KEY,
            order_id NUMBER,
            montant NUMBER(10,2),
            methode VARCHAR2(30),
            date_paiement DATE
        )""",
        "EMPLOYEES": """CREATE TABLE bilal.EMPLOYEES (
            id NUMBER PRIMARY KEY,
            nom VARCHAR2(100),
            poste VARCHAR2(50),
            salaire NUMBER(10,2),
            departement VARCHAR2(50)
        )"""
    }

    for name, sql in tables.items():
        try:
            cursor.execute(sql)
            print(f" Table {name} créée")
        except Exception as e:
            print(f" Table {name}: {e}")

    conn.commit()

def seed_customers(conn, n=2000):
    print(f"👥 Insertion {n} customers...")
    cursor = conn.cursor()
    for i in range(1, n+1):
        cursor.execute(
            "INSERT INTO bilal.CUSTOMERS VALUES (:1,:2,:3,:4,:5)",
            (i, fake.name(), fake.email(), fake.city(), fake.date_of_birth())
        )
    conn.commit()
    print(f" {n} customers insérés")

def seed_products(conn, n=500):
    print(f" Insertion {n} products...")
    cursor = conn.cursor()
    categories = ['Electronique', 'Vetements', 'Alimentation', 'Sport', 'Maison']
    for i in range(1, n+1):
        cursor.execute(
            "INSERT INTO bilal.PRODUCTS VALUES (:1,:2,:3,:4,:5)",
            (i, fake.word(), round(random.uniform(10, 1000), 2),
             random.choice(categories), random.randint(0, 500))
        )
    conn.commit()
    print(f" {n} products insérés")

def seed_orders(conn, n=5000):
    print(f" Insertion {n} orders...")
    cursor = conn.cursor()
    statuts = ['EN_COURS', 'LIVRE', 'ANNULE', 'EN_ATTENTE']
    for i in range(1, n+1):
        cursor.execute(
            "INSERT INTO bilal.ORDERS VALUES (:1,:2,:3,:4,:5)",
            (i, random.randint(1, 2000), fake.date_of_birth(),
             round(random.uniform(20, 5000), 2), random.choice(statuts))
        )
    conn.commit()
    print(f" {n} orders insérés")

def seed_payments(conn, n=5000):
    print(f"Insertion {n} payments...")
    cursor = conn.cursor()
    methodes = ['CARTE', 'VIREMENT', 'ESPECES', 'PAYPAL']
    for i in range(1, n+1):
        cursor.execute(
            "INSERT INTO bilal.PAYMENTS VALUES (:1,:2,:3,:4,:5)",
            (i, random.randint(1, 5000), round(random.uniform(20, 5000), 2),
             random.choice(methodes), fake.date_of_birth())
        )
    conn.commit()
    print(f" {n} payments insérés")

def seed_employees(conn, n=200):
    print(f"Insertion {n} employees...")
    cursor = conn.cursor()
    postes = ['Developpeur', 'Manager', 'Comptable', 'Commercial', 'RH']
    departements = ['IT', 'Finance', 'Ventes', 'Marketing', 'Support']
    for i in range(1, n+1):
        cursor.execute(
            "INSERT INTO bilal.EMPLOYEES VALUES (:1,:2,:3,:4,:5)",
            (i, fake.name(), random.choice(postes),
             round(random.uniform(3000, 15000), 2), random.choice(departements))
        )
    conn.commit()
    print(f" {n} employees insérés")

if __name__ == "__main__":
    try:
        conn = get_connection()
        create_tables(conn)
        seed_customers(conn)
        seed_products(conn)
        seed_orders(conn)
        seed_payments(conn)
        seed_employees(conn)
        conn.close()
        print(" Seed terminé avec succès!")
    except Exception as e:
        print(f" Erreur: {e}")