import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=13f47a39b05529f6e82312c80039a0e9&language=en-US".format(movie_id)
    data = requests.get(url)  
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse =True,key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Help to fetch poster from api
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies = pickle.load(open('movies.pkl','rb'))
similarity  = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommendation App')

selected_movie = st.selectbox(
'Select a movie to get recommendations',
movies['title'].values)

if st.button('Get Recommendations'):
    names,posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5, = st.columns(5)
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

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)
    
    # Poster Grid with CSS Grid and Styling
    st.markdown(
        """
        
        <style>
        /* CSS Reset (add this at the beginning of your <style> block) */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.poster-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
    grid-gap: 10px; 
}

.poster {
    transition: transform 0.2s;
    border-radius: 8px;
    margin: 10px;
}

.poster img {
    width: 100%;
    height: auto;
}

        .poster-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            grid-gap: 10px; 
        }
        .poster {
            transition: transform 0.2s;
            border-radius: 8px;
            margin: 10px;
        }
        .poster:hover {
            transform: scale(1.05); 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        }
        .poster img {
            width: 100%;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="poster-grid">', unsafe_allow_html=True)
    for name, poster in zip(names, posters):
        if poster:
            st.markdown(f'<div class="poster"><p style="text-align: center;">{name}</p><img src="{poster}" style="width: 100%;"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)