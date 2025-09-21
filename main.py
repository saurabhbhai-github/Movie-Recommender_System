import streamlit as st
import pickle
import pandas as pd
import requests

st.markdown(
    """
    <style>
    .stApp {
         background-color: black;
         color: white;
     }
div.stButton > button:first-child {
        background-color: black;   
        color: red;                
        border: 2px solid red;     
        border-radius: 10px;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: red;    
        color: white;              
        border: 2px solid white;   
    }    label, .stSelectbox label {
        color: white !important;
        font-weight: bold;
    }
    </style>
     """,
    unsafe_allow_html=True
 )

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommendar System')

selected_movie_name = st.selectbox(
    'Choose a movie',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"<p style='color:white; text-align:center; font-weight:bold;'>{names[i]}</p>",
                unsafe_allow_html=True
            )
            st.image(posters[i])
