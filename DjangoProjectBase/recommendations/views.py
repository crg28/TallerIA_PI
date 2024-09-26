from django.shortcuts import render
from movie.models import Movie
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Funciones auxiliares
def get_embedding(text, client, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Vista para recomendar película
def recomendar_pelicula(request):
    movie_recomendada = None
    if request.method == 'POST':
        # Cargar la API key de OpenAI desde el archivo .env
        load_dotenv('../api_keys.env')
        client = OpenAI(api_key=os.environ.get('openai_api_key'))

        # Obtener el prompt enviado por el usuario desde el formulario
        prompt = request.POST.get('prompt')

        # Obtener el embedding del prompt
        emb_req = get_embedding(prompt, client)

        # Obtener todas las películas
        items = Movie.objects.all()

        # Calcular la similitud con cada película
        sim = []
        for item in items:
            emb = item.emb
            emb = list(np.frombuffer(emb))
            sim.append(cosine_similarity(emb, emb_req))

        # Encontrar la película más similar
        sim = np.array(sim)
        idx = np.argmax(sim)
        movie_recomendada = items[int(idx)]

    # Renderizar la misma plantilla y pasar los detalles de la película recomendada si existe
    return render(request, 'recomendar.html', {'pelicula': movie_recomendada})
