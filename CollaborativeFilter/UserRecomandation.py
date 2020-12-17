import os
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz


def fuzzy_matching(mapper, fav_course, verbose=True):
    """
    return the closest match via fuzzy ratio.

    Parameters
    ----------
    mapper: dict, map course title name to index of the course in data
    fav_course: str, name of user input course

    verbose: bool, print log if True
    Return
    ------
    index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_course.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple[0][1]


# In[25]:


def make_recommendation(model_knn, data, mapper, fav_course, df_courses, n_recommendations):
    """
    return top n similar course recommendations based on user's input course
    Parameters
    ----------
    model_knn: sklearn model, knn model
    data: course-user matrix
    mapper: dict, map course name to index of the course in data
    fav_course: str, name of user input course
    n_recommendations: int, top n recommendations
    Return
    ------
    list of top n similar course recommendations
    """
    # fit
    model_knn.fit(data)
    # get input course index
    print('You have input course:', fav_course)
    idx = fuzzy_matching(mapper, fav_course, verbose=True)

    print('Recommendation system start to make inference')
    print('......\n')
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations + 1)

    raw_recommends = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[
                     :0:-1]
    print(raw_recommends)
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    recommended_courses = []
    print('Recommendations for {}:'.format(fav_course))
    for i, (idx, dist) in enumerate(raw_recommends):
        print('{0}: {1} - {2}, with distance of {3}'.format(i + 1, df_courses.course_id[idx], reverse_mapper[idx], dist))
        recommended_courses.append(df_courses.course_id[idx])
    return recommended_courses


def collaborative_users(my_course):
    data_path = '../Datasets/'
    courses_filename = 'id_courses_coursera.csv'
    ratings_filename = 'user-course-rating.csv'
    df_courses = pd.read_csv(
        os.path.join(data_path, courses_filename),
        usecols=['course_id', 'course_name'],
        dtype={'course_id': 'int32', 'course_name': 'str'})
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

    # map course titles to images
    course_to_idx = {
        course: i for i, course in
        enumerate(list(df_courses.set_index('course_id').loc[df_courses_features.index].course_name))
    }

    mat_courses_features = csr_matrix(df_courses_features.values)
    # print(df_courses_features)

    num_users = len(df_ratings.user_id.unique())
    num_items = len(df_ratings.course_id.unique())
    # print('There are {} unique users and {} unique courses in this data set'.format(num_users, num_items))

    df_ratings_cnt_tmp = pd.DataFrame(df_ratings.groupby('rating').size(), columns=['count'])
    # print(df_ratings_cnt_tmp)

    # there are a lot more counts in rating of zero
    total_cnt = num_users * num_items
    rating_zero_cnt = total_cnt - df_ratings.shape[0]

    df_ratings_cnt = df_ratings_cnt_tmp.append(
        pd.DataFrame({'count': rating_zero_cnt}, index=[0.0]),
        verify_integrity=True,
    ).sort_index()
    # print(df_ratings_cnt)

    # log normalise to make it easier to interpret on a graph
    df_ratings_cnt['log_count'] = np.log(df_ratings_cnt['count'])
    # print(df_ratings_cnt)

    plt.style.use('ggplot')

    # get_ipython().run_line_magic('matplotlib', 'inline')
    ax = df_ratings_cnt[['count']].reset_index().rename(columns={'index': 'rating score'}).plot(
        x='rating score',
        y='count',
        kind='bar',
        figsize=(12, 8),
        title='Count for Each Rating Score (in Log Scale)',
        logy=True,
        fontsize=12,
    )
    ax.set_xlabel("course rating score")
    ax.set_ylabel("number of ratings")
    # plt.show()

    # define model
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    # fit
    model_knn.fit(mat_courses_features)

    recommended_courses = make_recommendation(
        model_knn=model_knn,
        data=mat_courses_features,
        fav_course=my_course,
        df_courses=df_courses,
        mapper=course_to_idx,
        n_recommendations=10)

    # print(recommended_courses)
    return recommended_courses


if __name__ == '__main__':
    collaborative_users('Financial Markets')





