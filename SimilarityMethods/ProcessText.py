from Database.database_interaction import get_all_descriptions
import spacy

nlp = spacy.load("en_core_web_lg")


def process_single_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if not token.text.isalpha():
            continue
        if token.pos_ == 'PRON':
            continue
        result.append(token.lemma_)
    return " ".join(result)


def process_all_descriptions():
    courses = get_all_descriptions()
    processed_courses = {}
    for k_id, v_desc in courses.items():
        processed_courses[k_id] = process_single_text(v_desc)
    return processed_courses
