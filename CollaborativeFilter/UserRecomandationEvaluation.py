import os

import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans, accuracy
from surprise.model_selection import train_test_split, cross_validate


def collaborative_eval():
    data_path = '../Datasets/'
    ratings_filename = 'user-course-rating.csv'
    df_ratings = pd.read_csv(
        os.path.join(data_path, ratings_filename),
        usecols=['user_id', 'course_id', 'rating'],
        dtype={'user_id': 'int32', 'course_id': 'int32', 'rating': 'float32'})
    # print(df_ratings.head())

    # pivot ratings into course features
    df_courses_features = df_ratings.pivot_table(
        index='course_id',
        columns='user_id',
        values='rating'
    ).fillna(0)

    reader = Reader(rating_scale=(1, 5))

    # Loads Pandas dataframe
    data = Dataset.load_from_df(df_ratings[['user_id', 'course_id', 'rating']], reader)

    # To use item-based cosine similarity
    sim_options = {
        "name": "cosine",
        "user_based": False,  # Compute  similarities between items
    }
    algo = KNNWithMeans(sim_options=sim_options)

    trainset, testset = train_test_split(data, test_size=.25)
    # trainingSet = data.construct_trainset()
    algo.fit(trainset)
    predictions = algo.test(testset)
    df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
    print(df)
    print(accuracy.rmse(predictions))

    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


if __name__ == '__main__':
    collaborative_eval()





