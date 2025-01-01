import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
    return "https://via.placeholder.com/200x300"  # Default placeholder poster

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies_list[movies_list['title'] == movie].index[0]
    except IndexError:
        return ["Movie not found. Please try another title."], []

    distances = similarity[movie_index]
    movies_list_with_scores = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]  # Top 5 similar movies

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list_with_scores:
        movie_id = movies_list.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_list.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_list = pickle.load(open('web/movies.pkl', 'rb'))
movies = movies_list['title'].values
similarity = pickle.load(open('web/similarity.pkl', 'rb'))

# Streamlit app starts here
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Custom styling for the app
st.markdown("""
    <style>
        .main { background-color: #f4f4f4; }
        .stButton>button { color: white; background-color: #007BFF; border-radius: 5px; }
        .stTitle, .stSelectbox { font-family: 'Arial', sans-serif; }
        .caption { font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎥 Movie Recommendation System")

# User input: Select movie
st.write("## 🌟 Select a Movie You Like")
selected_movie = st.selectbox("Search and select a movie:", movies, key="movie_select")

# Recommendation button
if st.button("💡 Recommend Movies"):
    recommended_movies, recommended_posters = recommend(selected_movie)

    if recommended_posters:
        st.write("## 📽️ Recommended Movies")
        # Create a row of columns for aligned boxes
        cols = st.columns(len(recommended_movies))  # Dynamically create as many columns as there are movies

        for col, name, poster in zip(cols, recommended_movies, recommended_posters):
            with col:
                st.image(poster, caption=f"🎬 {name}", use_container_width=True)  # Updated to use_container_width
    else:
        st.error(f"🚫 {recommended_movies[0]}")

# Footer
st.markdown("""
    ---
    **Developed by Syed Subhan Shah**
    """)
