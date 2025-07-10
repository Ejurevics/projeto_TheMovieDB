import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# ATIVAR VENC:  ->  .\venv\Scripts\Activate.ps1

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configurações da API
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Obter os gêneros (para converter genre_ids -> nomes)
def get_genres():
    url = f"{BASE_URL}/genre/movie/list?language=pt-BR&api_key={API_KEY}"
    response = requests.get(url)
    genres_data = response.json()["genres"]
    return {genre["id"]: genre["name"] for genre in genres_data}

# Obter filmes populares (pode variar a página para mais resultados)
def get_popular_movies(page):
    url = f"{BASE_URL}/movie/popular?language=pt-BR&page={page}&api_key={API_KEY}"
    response = requests.get(url)
    return response.json()["results"]

# Função principal
def main():
    print("Coletando dados dos filmes populares...")
    all_movies = []
    genres_dict = get_genres()

    for page in range(1, 6):  # Coletar 5 páginas (~100 filmes)
        movies = get_popular_movies(page)
        for movie in movies:
            all_movies.append({
                "id": movie["id"],
                "titulo": movie["title"],
                "data_lancamento": movie["release_date"],
                "popularidade": movie["popularity"],
                "nota_media": movie["vote_average"],
                "votos": movie["vote_count"],
                "idioma": movie["original_language"],
                "generos": ", ".join([genres_dict.get(g, "Desconhecido") for g in movie["genre_ids"]])
            })
        time.sleep(0.3)  # Evitar sobrecarga da API

    df = pd.DataFrame(all_movies)
    df.to_csv("dados/filmes_populares.csv", index=False, encoding="utf-8-sig")
    print("Dados salvos em: dados/filmes_populares.csv")

if __name__ == "__main__":
    main()
