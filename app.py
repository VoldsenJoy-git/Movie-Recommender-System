import streamlit as st
import pickle 
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    
    # taking only the poster_path to show the poster in tmdb
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # fetching the index
    distance = similarity[index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key = lambda x: x[1])# making tuple by enumerate and sort in decending , on the 2nd key
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list[1:11]:
        recommended_movies.append(movies.iloc[i[0]].title)
        
        #fetch poster from api
        movie_id = movies.iloc[i[0]].id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters




movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movie_dict)  # -------- 1 -> used movie set














#--------------------------------------------------------------------------------------
st.title("Movie Recommender System")
#------------------------------------------------ selected movie from box
selected_movie_name = st.selectbox(
    'Select/Type a Movie for recommendation of similar movies',
    (movies['title'].values))

#--------------------clicking the button will show recommended movies and corresponding posters(Layout from streamlit)
if st.button('Recommend'):
    names , posters = recommend(selected_movie_name) 
    num_cols = 5
    num_rows = (len(names) + num_cols - 1) // num_cols  # Calculate number of rows required

    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx, col in enumerate(cols):
            movie_idx = row * num_cols + col_idx
            if movie_idx < len(names):
                col.text(names[movie_idx])
                col.image(posters[movie_idx])