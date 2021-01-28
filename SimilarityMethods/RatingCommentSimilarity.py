import spacy

from Database.DBInteractCourses import get_courses_by_ids
from Database.DBProcessReviewComments import get_all_review_embeddings
from SimilarityMethods.DescriptionSimilarity import calculate_similarity

nlp = spacy.load("en_core_web_sm")


def find_best_review_comment_similarity(id_course):
    new_comments = get_all_review_embeddings()
    review_comment = nlp(new_comments[id_course])
    del new_comments[id_course]

    similar_comments = []
    for k_id, curr_comment in new_comments.items():
        similarity_rate = calculate_similarity(review_comment, curr_comment)
        if similarity_rate > 0.95:
            similar_comments.append((k_id, similarity_rate))
    return similar_comments


def get_similar_review_comments(course_id):
    sim_review_comments = find_best_review_comment_similarity(course_id)
    sim_review_comments.sort(key=lambda x: x[1], reverse=True)
    sim_ids = [c[0] for c in sim_review_comments]
    if len(sim_ids) > 5:
        sim_ids = sim_ids[:5]
    return get_courses_by_ids(sim_ids)