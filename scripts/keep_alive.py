import requests
import time

URL = "https://sick-bjj-app.onrender.com/docs"

def visit_url():
    while True:
        try:
            response = requests.get(URL)
        except requests.exceptions.RequestException as e:
            print(f"Error visiting {URL}: {e}")
        
        time.sleep(30)  # Wait 30 seconds before the next request

if __name__ == "__main__":
    visit_url()