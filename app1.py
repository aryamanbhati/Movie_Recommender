import streamlit as st
import pickle
import pandas as pd
import requests
import os
import subprocess
import sys

# Function to install gdown if it's not already installed
def install_gdown():
    try:
        import gdown
    except ImportError:
        # Install gdown if not found
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gdown'])

# Install gdown
install_gdown()
import gdown  # Import gdown after installation

# Function to download similarity.pkl from Google Drive if it doesn't exist
def download_similarity_file():
    file_id = '1iS9QWhaFr17mJUOOokbEOOqwdbisTlld'  # Replace with your actual Google Drive File ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = 'similarity.pkl'
    
    # Check if the file already exists, if not, download it
    if not os.path.exists(output_path):
        with st.spinner("Downloading model file..."):
            gdown.download(url, output_path, quiet=False)

# Download the similarity file if necessary
download_similarity_file()

# Load the similarity.pkl file
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    recommended_movies = []
    recommended_movie_poster = []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movie_poster

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
st.title("Movie Recommendation System")
selected_movie_name = st.selectbox('Movie Name', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
