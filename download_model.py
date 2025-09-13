# scrape_models.py
import requests
from bs4 import BeautifulSoup

def get_gpt4all_models():
    url = "https://gpt4all.io/models/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)
    
    models = [
        link["href"] for link in links
        if (link["href"].endswith(".bin") or link["href"].endswith(".gguf"))
    ]
    return models

if __name__ == "__main__":
    models = get_gpt4all_models()
    for m in models:
        print(m)