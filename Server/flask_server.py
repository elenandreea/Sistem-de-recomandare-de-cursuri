from flask import Flask, request, jsonify
from flask_cors import CORS
from Database.database_interaction import *
from Database.database_user import checkUser
from SimilarityMethods.cosine_similarity_spacy import get_similar_courses

app = Flask(__name__)
CORS(app)


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
    result = get_similar_courses(course_id)
    return jsonify(result)


@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.json('username')
    password = request.json('password')
    result = checkUser(username, password)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
