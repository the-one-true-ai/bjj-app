import requests
import random
import time
from datetime import datetime, timedelta

# API Endpoint
url = "https://sick-bjj-app.onrender.com/api/v1/users/create_user"

# List of famous BJJ practitioners and additional usernames
bjj_names = [
    "RogerGracie", "MarceloGarcia", "GordonRyan", "RicksonGracie", "RoyceGracie",
    "AndreGalvao", "BernardoFaria", "RafaelMendes", "Cobrinha", "LucasLepri",
    "MikeyMusumeci", "KeenanCornelius", "Buchecha", "XandeRibeiro", "LeandroLo",
    "RomuloBarrera", "JT Torres", "MuriloBustamante", "Terere", "DemianMaia",
    "RobertDrysdale", "SauloRibeiro", "FelipePena", "MendesBrothers", "CraigJones",
    "DeanLister", "RenzoGracie", "JeanJacquesMachado", "BrunoMalfacine", "VitorShaolin",
    "LeoViera", "MuriloSantana", "RodolfoVieira", "FabioGurgel", "BraulioEstima",
    "NickyRyan", "GabiGarcia", "PabloPopovitch", "CelsinhoVinicius", "GustavoDantas",
    "FredsonPaxiao", "CaioTerra", "AndrePederneiras", "AlexandreSoca", "MarioSperry",
    "RicardoArona", "RenatoVerissimo", "PedroSauer", "CrisCyborg", "LeticiaRibeiro",
    "LuannaAlzuguir", "BeaMesquita", "MichelleNicolini", "MackenzieDern", "FfionDavies",
    "MayraBueno", "TalitaAlencar", "AnaCarolina", "TammiMusumeci", "GabrielleMcComb",
    "BiancaBasilio", "ErberthSantos", "VinnyMagalhaes", "ThiagoAlves", "HelioGracie",
    "AdamHightowerEllis", "DanGeoghagen", "AndyRoberts", "ArmyChris", "AmeriDan", "Achal", "PurpleBeltCraig", "BrownBeltTom"
]

# Ensure unique usernames and emails
random.shuffle(bjj_names)
created_users = set()

# Available roles and belts
roles = ["Student", "Coach", "Both"]
belts = ["White", "Blue", "Purple", "Brown", "Black", "Coral"]

def generate_email(username):
    return f"{username.lower()}@example.com"

def random_birthdate():
    """Generate a random birthdate between 18 and 50 years old."""
    today = datetime.today()
    age = random.randint(18, 50)
    birthdate = today - timedelta(days=age * 365)
    return birthdate.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD

for i in range(100):
    try:
        if not bjj_names:
            break  # Stop if we run out of unique names
        
        username = f"{bjj_names.pop()}_{random.randint(1000, 9999)}"
        email = generate_email(username)
        role = random.choice(roles)
        height = random.randint(150, 200)  # Random height between 150cm and 200cm
        weight = random.randint(60, 120)  # Random weight between 60kg and 120kg
        birthdate = random_birthdate()
        belt = random.choice(belts)

        if username in created_users:
            continue
        
        payload = {
            "email": email,
            "password": "securepassword",
            "role": role,
            "username": username,
            "height": height,
            "weight": weight,
            "birthdate": birthdate,
            "belt": belt
        }
        
        response = requests.post(url, json=payload)
        
        print(f"User created: {username} ({role}, {belt}) - {height}cm, {weight}kg, Birthdate: {birthdate}")
        print(f"Response code: {response.status_code}")
        created_users.add(username)

        time.sleep(0.5)  # Prevent overwhelming the server
    except Exception as e:
        print(e)
