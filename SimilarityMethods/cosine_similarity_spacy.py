import spacy


from Database.database_interaction import get_all_descriptions, get_courses_by_ids

nlp = spacy.load("en_core_web_lg")


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.pos_ == 'PRON':
            continue
        result.append(token.lemma_)
    return " ".join(result)


def calculate_similarity(text1, text2):
    text2 = nlp(process_text(text2))
    if text1 and text2:
        return text1.similarity(text2)
    return 0


def find_best_description_similarity(id_course):
    courses = get_all_descriptions()
    description_course = nlp(process_text(courses[id_course]))
    del courses[id_course]

    similar_courses = []
    for k_id, v_description in courses.items():
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


# if __name__ == '__main__':
#     courses = get_similar_courses('2830')
#     print(courses)
