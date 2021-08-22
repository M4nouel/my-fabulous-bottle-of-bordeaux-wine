import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import json

BordeauxWines = pd.read_csv('bordeaux_wines_knn_ready.csv', index_col = 0)
taste_knn_tmp = BordeauxWines.iloc[:,8:] # select only the attribute columns
taste_knn = taste_knn_tmp.loc[:,taste_knn_tmp.sum(axis =0) != 0] # delete columns always equal to 0
knn = NearestNeighbors(n_neighbors=7, metric='jaccard')
knn.fit(taste_knn)

# saves the model to disk
# will be load by the API
filename = 'knn_model.sav'
pickle.dump(knn, open(filename, 'wb'))

# transforms the csv to be load in Postgres: keeps only the label columns and
# strores the boolean taste columns as a json array inside the Tastes column
wines = BordeauxWines.iloc[:,:8]
parsed_json = json.loads(taste_knn.head(2).to_json(orient="values"))
parsed_json = json.loads(taste_knn.to_json(orient="values"))
wines['Tastes'] = [json.dumps([row]) for row in parsed_json]
# strores the csv with ';' sep since the json array contains ','
wines.to_csv('bordeaux_wines_bdd_ready.csv', sep=';')