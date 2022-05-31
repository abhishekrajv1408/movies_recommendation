import numpy as np
import pandas as pd
import matplotlib.pyplot as py
import ast
import nltk

def recommend(mov):
    movies =pd.read_csv("movies_data.csv")

#genres , id , keywords , title, overview
    movie_data=movies[['id', 'genres','keywords','title','overview']]
    movie_data.dropna(inplace=True)



    def modifie(obj):
        Lt = []
        for i in ast.literal_eval(obj):
            Lt.append(i['name'])
        return Lt
    movie_data['genres']=movie_data['genres'].apply(modifie)
    movie_data['keywords']=movie_data['keywords'].apply(modifie)
    movie_data['overview']=movie_data['overview'].apply(lambda x:x.split())

    movie_data['genres']=movie_data['genres'].apply(lambda x:[i.replace(" ","")for i in x])
    movie_data['keywords']=movie_data['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
    movie_data['overview']=movie_data['overview'].apply(lambda x:[i.replace(" ","")for i in x])

    movie_data['tag']=movie_data['overview']+movie_data['genres']+movie_data['keywords']
    movie=movie_data[['id','title','tag']]

    movie['tag']=movie['tag'].apply(lambda x:" ".join(x))
    movie['tag'].iloc[0]
    movie['tag']=movie['tag'].apply(lambda x:x.lower())

    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=5000,stop_words='english')

    vectors =cv.fit_transform(movie['tag']).toarray()
    
    from nltk.stem.porter import PorterStemmer
    ps= PorterStemmer()

    def stem(text):
        y= []
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)

    movie['tag']=movie['tag'].apply(stem)

    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=5000,stop_words='english')

    vectors =cv.fit_transform(movie['tag']).toarray()

    from sklearn.metrics.pairwise import cosine_similarity
    similarity= cosine_similarity(vectors)


    movie_index = movie[movie['title'] == mov].index[0]
    distances = similarity[movie_index]
    movies_list = (sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7])
    b=[]
    for i in movies_list:
        b.append(movie.iloc[i[0]].title)
    # data=pd.DataFrame(data)
    return b
    