import spacy


from Database.database_interaction import get_all_descriptions

nlp = spacy.load("en_core_web_lg")


def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)


def calculate_similarity(text1, text2):
    text2 = nlp(process_text(text2))
    return text1.similarity(text2)


def find_best_description_similarity(id_course):
    courses = get_all_descriptions()
    print(courses[id_course])
    description_course = nlp(process_text(courses[id_course]))
    del courses[id_course]

    similar_courses = []
    for k_id, v_description in courses.items():
        similarity_rate = calculate_similarity(description_course, v_description)
        if similarity_rate > 0.85:
            similar_courses.append((k_id, similarity_rate))
    return similar_courses


if __name__ == '__main__':
    fav_courses = find_best_description_similarity('0')
    fav_courses.sort(key=lambda x: x[1], reverse=True)
    print(fav_courses)
