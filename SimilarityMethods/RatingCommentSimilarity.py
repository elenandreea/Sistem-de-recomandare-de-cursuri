import spacy

from Database.DBInteractCourses import get_courses_by_ids
from SimilarityMethods.DescriptionSimilarity import calculate_similarity

nlp = spacy.load("en_core_web_lg")


def find_best_rating_comment_similarity(id_course):
    new_comments = get_all_rating_comments()
    rating_comment = nlp(new_comments[id_course])
    del new_comments[id_course]

    similar_comments = []
    for k_id, curr_comment in new_comments.items():
        similarity_rate = calculate_similarity(rating_comment, curr_comment)
        if similarity_rate > 0.98:
            similar_comments.append((k_id, similarity_rate))
    return similar_comments


def get_similar_rating_comments(course_id):
    sim_rating_comments = find_best_rating_comment_similarity(course_id)
    sim_rating_comments.sort(key=lambda x: x[1], reverse=True)
    sim_ids = [c[0] for c in sim_rating_comments]
    if len(sim_ids) > 5:
        sim_ids = sim_ids[:5]
    return get_courses_by_ids(sim_ids)