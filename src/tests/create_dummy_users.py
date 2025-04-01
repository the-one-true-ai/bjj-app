import requests
import random
import time
from datetime import datetime, timedelta

# API Endpoint
url = "http://127.0.0.1:8000/api/v1/users/create_user"

# List of famous BJJ practitioners and additional usernames
bjj_names = [
    "RogerGracie",
    "MarceloGarcia",
    "GordonRyan",
    "RicksonGracie",
    "RoyceGracie",
    "AndreGalvao",
    "BernardoFaria",
    "RafaelMendes",
    "Cobrinha",
    "LucasLepri",
    "MikeyMusumeci",
    "KeenanCornelius",
    "Buchecha",
    "XandeRibeiro",
    "LeandroLo",
    "RomuloBarrera",
    "JT Torres",
    "MuriloBustamante",
    "Terere",
    "DemianMaia",
    "RobertDrysdale",
    "SauloRibeiro",
    "FelipePena",
    "MendesBrothers",
    "CraigJones",
    "DeanLister",
    "RenzoGracie",
    "JeanJacquesMachado",
    "BrunoMalfacine",
    "VitorShaolin",
    "LeoViera",
    "MuriloSantana",
    "RodolfoVieira",
    "FabioGurgel",
    "BraulioEstima",
    "NickyRyan",
    "GabiGarcia",
    "PabloPopovitch",
    "CelsinhoVinicius",
    "GustavoDantas",
    "FredsonPaxiao",
    "CaioTerra",
    "AndrePederneiras",
    "AlexandreSoca",
    "MarioSperry",
    "RicardoArona",
    "RenatoVerissimo",
    "PedroSauer",
    "CrisCyborg",
    "LeticiaRibeiro",
    "LuannaAlzuguir",
    "BeaMesquita",
    "MichelleNicolini",
    "MackenzieDern",
    "FfionDavies",
    "MayraBueno",
    "TalitaAlencar",
    "AnaCarolina",
    "TammiMusumeci",
    "GabrielleMcComb",
    "BiancaBasilio",
    "ErberthSantos",
    "VinnyMagalhaes",
    "ThiagoAlves",
    "HelioGracie",
    "AdamHightowerEllis",
    "DanGeoghagen",
    "AndyRoberts",
    "ArmyChris",
    "AmeriDan",
    "Achal",
    "PurpleBeltCraig",
    "BrownBeltTom",
]

# Coach bios
coach_bios = [
    "I have been training BJJ for over 15 years and have a passion for developing both competitors and recreational practitioners.",
    "As a black belt with over 10 years of experience, I specialize in both Gi and No-Gi BJJ and have coached multiple champions.",
    "With a strong emphasis on fundamentals and advanced techniques, I believe in the importance of a strong foundation in BJJ.",
    "A former competitive fighter, now coaching with a focus on creating well-rounded athletes capable of dominating any scenario.",
    "I aim to help my students build confidence through BJJ, no matter their skill level, focusing on both mental and physical growth.",
    "A black belt who has been on the mats since childhood, now sharing my knowledge to build the next generation of BJJ champions.",
    "I believe in the effectiveness of BJJ for self-defense and work with all levels of students to increase both their skill and fitness.",
    "Having trained under some of the best in the world, my coaching philosophy revolves around a mix of technical precision and creativity.",
    "Passionate about teaching BJJ to students of all ages, I focus on developing both the technical aspects and the mindset required for success in competition.",
    "My training philosophy is to give every student the tools they need to succeed, whether in competition or in life outside the academy.",
]

# BJJ techniques
bjj_concepts_techniques = [
    "Guard Passing",
    "Sweeps",
    "Armbar",
    "Triangle Choke",
    "Kimura",
    "Cross Collar Choke",
    "De La Riva Guard",
    "Half Guard",
    "Spider Guard",
    "X-Guard",
    "Omoplata",
    "Leg Locks",
    "Back Control",
    "Mount Position",
    "Side Control",
    "Escape Techniques",
    "Takedowns",
    "Double Leg Takedown",
    "Single Leg Takedown",
    "Guillotine Choke",
    "Knee on Belly",
    "Submission Chains",
    "Pressure Passing",
    "Lapels",
    "Lasso Guard",
    "Submission Defense",
    "Flow Rolling",
    "Sparring Strategies",
    "Positioning",
    "Transitions",
    "Foot Locks",
    "BJJ for Self Defense",
    "Competition Training",
    "No-Gi Grappling",
    "Gi Grappling",
]

# Available roles and belts
roles = ["Student", "Coach", "Both"]
belts = ["White", "Blue", "Purple", "Brown", "Black", "Coral"]

# Available BJJ academies for affiliations
affiliations = [
    "Alliance BJJ",
    "Gracie Barra",
    "Atos Jiu Jitsu",
    "Checkmat",
    "Soul Fighters",
    "Cobrinha Jiu Jitsu",
    "Nova União",
    "Mendes Brothers Academy",
    "BJJ Revolution Team",
    "Evolve MMA",
    "Team Lloyd Irvin",
    "Gracie Academy",
    "Legion Jiu Jitsu",
    "BJJ Superstars",
    "Zenith BJJ",
    "Fight Sports",
    "Marcio Feitosa Academy",
    "BJJ Stars",
]

# Ensure unique usernames and emails
random.shuffle(bjj_names)
created_users = set()


def generate_email(username):
    return f"{username.lower()}@example.com"


def random_birthdate():
    """Generate a random birthdate between 18 and 50 years old."""
    today = datetime.today()
    age = random.randint(18, 50)
    birthdate = today - timedelta(days=age * 365)
    return birthdate.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD


for i in range(50):
    try:
        if not bjj_names:
            break  # Stop if we run out of unique names

        username = f"{bjj_names.pop()}_{random.randint(10, 100)}"
        email = generate_email(username)
        role = random.choice(roles)
        height = random.randint(100, 200)  # Height between 100cm and 200cm
        weight = random.randint(100, 200)  # Weight between 100kg and 200kg
        birthdate = random_birthdate()
        belt = random.choice(belts)
        coach_bio = random.choice(coach_bios)
        expertise = random.sample(bjj_concepts_techniques, random.randint(2, 5))
        areas_working_on = random.sample(bjj_concepts_techniques, random.randint(2, 5))
        affiliations_list = random.sample(affiliations, random.randint(1, 3))

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
            "belt": belt,
            "coach_bio": coach_bio,
            "expertise": expertise,
            "affiliations": affiliations_list,
            "areas_working_on": areas_working_on,
        }

        response = requests.post(url, json=payload)

        print(
            f"User created: {username} ({role}, {belt}) - {height}cm, {weight}kg, Birthdate: {birthdate}"
        )
        print(f"Response code: {response.status_code}")
        created_users.add(username)

        time.sleep(0.5)  # Prevent overwhelming the server
    except Exception as e:
        print(e)
