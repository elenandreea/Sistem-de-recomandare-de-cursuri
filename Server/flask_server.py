from flask import Flask, request, jsonify
from flask_cors import CORS
from Database.database_interaction import *
from Database.database_user import checkUser
from SimilarityMethods.DescriptionSimilarity import get_similar_courses
from SimilarityMethods.ProcessText import process_all_descriptions
import copy

app = Flask(__name__)
CORS(app)

processed_courses_desc = process_all_descriptions()
print("Descrierile au fost incarcate")


@app.route("/allCourses")
def all_courses():
    result = get_all_courses()
    return jsonify(result)


@app.route("/CourseById", methods=['POST', 'GET'])
def course_by_id():
    course_id = 2830
    # course_id = request.json['idCourse']
    result = get_course_by_id(course_id)
    return jsonify(result)


@app.route("/similarCourses", methods=['POST', 'GET'])
def similar_courses():
    course_id = 2830
    # course_id = request.json['idCourse']
    start_time = time.time()
    copy_desc = copy.deepcopy(processed_courses_desc)
    print(time.time() - start_time)
    result = get_similar_courses(course_id, copy_desc)
    print(len(processed_courses_desc))
    return jsonify(result)


@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.json('username')
    password = request.json('password')
    result = checkUser(username, password)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
