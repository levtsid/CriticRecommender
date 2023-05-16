# CriticRecommender
ML movie recs
 
Tensorflow based system that scrapes critic ratings from metacritic and uses maximum likelihood listwise ranking to make recommendations. 

Essentially compares the critics to each other to predict how they would score a movie they have/haven't scored.  

Embedding dimensionality, dense size, and dropouts feature as moddable.

Next steps include adding user input for user score prediction based on critic ratings.

Based on work by Raj Mehrota on Kaggle and tensorflow documentation.
