import requests
import random
import time

# API Endpoint
url = "http://127.0.0.1:8000//api/v1/users/create_user"

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
    "AdamHightowerEllis", "DanGeoghagen", "AndyRoberts", "ArmyChris", "AmeriDan", "Achal", "PurpleBeltSmoke",
    "MiaKhalifa", "AngelaWhite", "LanaRhoades", "RileyReid",
    "JennaJameson", "ToriBlack", "AsaAkira", "SashaGrey", "BrandiLove",
    "AbellaDanger", "MadisonIvy", "NicoleAniston", "JessaRhodes", "LexiBelle",
    "SunnyLeone", "RomiRain", "AlettaOcean", "DaniDaniels", "AJApplegate",
    "AugustAmes", "ChristyMack", "KendraLust", "EvaLovia", "NatashaNice"
]

# Ensure unique usernames and emails
random.shuffle(bjj_names)
created_users = set()

# Available roles
roles = ["Student", "Coach", "Both"]

def generate_email(username):
    return f"{username.lower()}@example.com"

for i in range(100):
    if not bjj_names:
        break  # Stop if we run out of unique names
    
    username = bjj_names.pop()
    username = username  # Limit to 7 characters and remove spaces
    email = generate_email(username)
    role = random.choice(roles)
    
    if username in created_users:
        continue
    
    payload = {
        "email": email,
        "password": "securepassword",
        "role": role,
        "username": username
    }
    
    response = requests.post(url, json=payload)
    
    print(f"User created: {username} ({role})")
    print(f"Response code is:{response.status_code}")
    created_users.add(username)

    time.sleep(0.5)  # Prevent overwhelming the server
