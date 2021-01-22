import csv

from Database.DBProcessReviewComments import insert_row_into_review_embeddings_table
from SimilarityMethods.ProcessText import process_single_text


def get_all_review_comments_data():
    with open('../Datasets/user-course-rating-review-final.csv', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        result = {}
        for row in csv_reader:
            if row['course_id'] in result.keys():
                result[row['course_id']] = result.get(row['course_id']) + " " + row['reviews']
            else:
                result[row['course_id']] = row['reviews']
    return result


def upload_review_embeddings_database():
    result = get_all_review_comments_data()
    for key, val in result.items():
        processed_val = process_single_text(val)
        insert_row_into_review_embeddings_table(int(key), processed_val)


if __name__ == '__main__':
    # get_all_review_comments_data()
    upload_review_embeddings_database()
