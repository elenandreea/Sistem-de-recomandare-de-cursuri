import spacy

from Database.DBInteractCourses import get_courses_by_ids
from Database.DBProcessDescription import get_all_embeddings

nlp = spacy.load("en_core_web_sm")


def calculate_similarity(text1, text2):
    text2 = nlp(text2)
    return text1.similarity(text2)


def find_best_description_similarity(id_course):
    new_courses = get_all_embeddings()
    description_course = nlp(new_courses[id_course])
    del new_courses[id_course]

    similar_courses = []
    for k_id, v_description in new_courses.items():
        similarity_rate = calculate_similarity(description_course, v_description)
        if similarity_rate > 0.85:
            similar_courses.append((k_id, similarity_rate))
    return similar_courses


def get_similar_courses(course_id):
    sim_courses = find_best_description_similarity(course_id)
    sim_courses.sort(key=lambda x: x[1], reverse=True)
    sim_ids = [c[0] for c in sim_courses]
    if len(sim_ids) > 10:
        sim_ids = sim_ids[:10]
    return get_courses_by_ids(sim_ids)
