import pandas as pd
from tqdm import tqdm
from AOC import AOC
from ftfy import fix_text #fixing encoding issues

BordeauxWines = pd.read_csv('BordeauxWines.csv')

#fixing encoding issues
for w in tqdm(range(len(BordeauxWines['Wine'].to_list()))):
    BordeauxWines.loc[w,'Wine'] = fix_text(BordeauxWines['Wine'][w])

# split price and quantity when possible
Price = BordeauxWines['Price'].replace('^\$',
                                      '',
                                      regex = True).replace('ml$',
                                                            '',
                                                            regex = True).str.split('/',
                                                                                    n = 1,
                                                                                    expand = True)
Price.columns = ['Price','Quantity']

Price['Price'] = pd.to_numeric(Price['Price'],errors = 'coerce')
# stores quantity as float to handle NaN and Inf
Price['Quantity'] = pd.to_numeric(Price['Quantity'],errors = 'coerce').astype(float)
# extract Name, AOC, Cuvee from the Wine column
NameAOC = BordeauxWines.Wine.str.split('^(.*)('+'|'.join(AOC)+')(.*)$',expand = True)
NameAOC = NameAOC.loc[:,1:3]
NameAOC.columns = ['Name','AOC', 'Cuvee']

BordeauxWines_split = BordeauxWines.drop('Price',axis = 1)
BordeauxWines_split = NameAOC.join(Price.join(BordeauxWines_split))
BordeauxWines_split.to_csv('bordeaux_wines_knn_ready.csv')