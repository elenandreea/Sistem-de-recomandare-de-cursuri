from Database.DBInteractCourses import get_all_descriptions
from Database.DBProcessDescription import insert_row_into_embeddings_table
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

    for k_id, v_desc in courses.items():
        processed_desc = process_single_text(v_desc)
        insert_row_into_embeddings_table(k_id, processed_desc)
    return True


# if __name__ == '__main__':
#     process_all_descriptions()
