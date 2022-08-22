import pandas as pd
import numpy as np

import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


movie_md=pd.read_csv('D:/data/movies_metadata.csv',low_memory=False)
movie_keywords=pd.read_csv('D:/data/keywords.csv',low_memory=False)
movie_credits=pd.read_csv('D:/data/credits.csv',low_memory=False)
print(movie_md.shape)
movie_md = movie_md[movie_md['vote_count']>=55]
movie_md = movie_md[['id','original_title','overview','genres']]
movie_md['title'] = movie_md['original_title'].copy()
movie_md.reset_index(inplace=True, drop=True)
movie_credits = movie_credits[['id','cast']]

print(movie_credits.head())
print(movie_md.head())
#Data Cleaning & Preprocessing
#movie_md = movie_md[movie_md['id'].str.isnumeric()]
movie_md['id'] = movie_md['id'].astype(int)

df = pd.merge(movie_md, movie_keywords, on='id', how='left')

df.reset_index(inplace=True, drop=True)

df = pd.merge(df, movie_credits, on='id', how='left')

df.reset_index(inplace=True, drop=True)

print(df.head())


df['genres'] = df['genres'].apply(lambda x: [i['name'] for i in eval(x)])

df['genres'] = df['genres'].apply(lambda x: ' '.join([i.replace(" ","") for i in x]))
#Filling the nan values as []
df['keywords'].fillna('[]', inplace=True)

df['keywords'] = df['keywords'].apply(lambda x: [i['name'] for i in eval(x)])

df['keywords'] = df['keywords'].apply(lambda x: ' '.join([i.replace(" ",'') for i in x]))

#Filling the nan values as []

df['cast'].fillna('[]', inplace=True)

df['cast'] = df['cast'].apply(lambda x: [i['name'] for i in eval(x)])

df['cast'] = df['cast'].apply(lambda x: ' '.join([i.replace(" ",'') for i in x]))
print(df.head())

#merge all content/description of movies as a single feature
df['tags'] = df['overview'] + ' ' + df['genres'] +  ' ' + df['original_title'] + ' ' + df['keywords'] + ' ' + df['cast']

# Delete useless columns
df.drop(columns=['genres','overview','original_title','keywords','cast'], inplace=True)
print(df.head())

print(df.isnull().sum())

df.drop(df[df['tags'].isnull()].index, inplace=True)
df.drop_duplicates(inplace=True)

tfidf = TfidfVectorizer(max_features=5000)
vectorized_data = tfidf.fit_transform(df['tags'].values)
vectorized_dataframe = pd.DataFrame(vectorized_data.toarray(), index=df['tags'].index.tolist())
#Perform Dimension Reduction¶
svd = TruncatedSVD(n_components=3000)

# Fit transform the data
reduced_data = svd.fit_transform(vectorized_dataframe)

# Print the shape
print(reduced_data.shape)
#Compute a similarity metric on vectors for recommendation
similarity = cosine_similarity(reduced_data)

#Making recommendations for a given movie
def recommendation(movie_title):
    id_of_movie = df[df['title'] == movie_title].index[0]
    distances = similarity[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    for i in movie_list:
        print(df.iloc[i[0]].title)

print(recommendation('The Shawshank Redemption'))