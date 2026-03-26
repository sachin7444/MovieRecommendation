import streamlit as st
import pickle
import pandas as pd
import requests

st.markdown("""
    <style>
    .stButton>button {
        background-color: red;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
def fetch_poster(movie_id):
    response = requests.get('http://api.themoviedb.org/3/movie/{}?api_key=27ddbc9392dfadc0b76f75f646ccf892&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch posters from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.caption(names[0])
        st.image(posters[0])

    with col2:
        st.caption(names[1])
        st.image(posters[1])

    with col3:
        st.caption(names[2])
        st.image(posters[2])
    
    with col4:
        st.caption(names[3])
        st.image(posters[3])
    
    with col5:
        st.caption(names[4])
        st.image(posters[4])
