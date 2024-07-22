import numpy as np
import pandas as pd
from .models import Rating, Book
from sklearn.decomposition import TruncatedSVD


class Recommender:
    def __init__(self, n_components=5):
        self.n_components = n_components
        self.model = None
        self.ratings_matrix = None
        self.user_id_to_index = {}
        self.book_id_to_index ={}

    def fit(self):
        ratings = Rating.objects.all().values('user_id', 'book_id', 'score')
        df = pd.DataFrame(ratings)
        self.user_id_to_index = {user_id: index for index, user_id in enumerate(df['user_id'].unique())}
        self.book_id_to_index = {book_id: index for index, book_id in enumerate(df['book_id'].unique())}
        ratings_matrix = pd.pivot_table(df, index='user_id', columns='book_id', values='score', fill_value=0)
        self.ratings_matrix = ratings_matrix.values
        self.model = TruncatedSVD(n_components=self.n_components)
        self.ratings_matrix_reduced = self.model.fit_transform(self.ratings_matrix)

    def recommend(self, user_id):
        if self.model is None:
            raise RuntimeError('Model must be fit before recommend.')

        if user_id not in self.user_id_to_index:
            raise ValueError('User not found.')

        user_index = self.user_id_to_index[user_id]
        user_ratings = np.dot(self.ratings_matrix_reduced[user_index, :], self.model.components_)

        recommended_book_indices = np.argsort(user_ratings)[::-1]
        recommended_books = [list(self.book_id_to_index.keys())[index] for index in recommended_book_indices]

        return recommended_books
