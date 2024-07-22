import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book, Rating


class ContentBasedRecommender:
    def __init__(self):
        self.books = None
        self.tfidf_matrix = None
        self.indices = None

    def fit(self):
        books = Book.objects.all().values('id', 'title', 'author', 'genre')
        self.books = pd.DataFrame(books)

        self.books['features'] = self.books['title'] + ' ' + self.books['author'] + ' ' + self.books['genre']

        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.books['features'])
        self.indices = pd.Series(self.books.index, index=self.books['id'])

    def recommend(self, user_id):
        user_ratings = Rating.objects.filter(user_id=user_id).values('book_id', 'score')
        user_ratings_df = pd.DataFrame(user_ratings)

        recommended_books = pd.DataFrame()
        for book_id in user_ratings_df['book_id']:
            if book_id in self.indices.index:
                idx = self.indices[book_id]
                sim_scores = list(enumerate(linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:11]

                book_indices = [i[0] for i in sim_scores]
                similar_books = self.books.iloc[book_indices]
                recommended_books = pd.concat([recommended_books, similar_books])

        recommended_books = recommended_books.drop_duplicates()
        recommended_books = recommended_books[~recommended_books['id'].isin(user_ratings_df['book_id'])]
        print(recommended_books.reset_index(drop=True))
        return dict(recommended_books.reset_index(drop=True))
