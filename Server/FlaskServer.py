from flask import Flask, request, jsonify
from flask_cors import CORS

from CollaborativeFilter.UserRecomandation import collaborative_users
from Database.DBInteractCourses import *
from Database.DBUser import checkUser
from SimilarityMethods.DescriptionSimilarity import get_similar_courses
import json

app = Flask(__name__)
CORS(app)


@app.route("/allCourses")
def all_courses():
    result = get_all_courses()
    return jsonify(result)

@app.route("/allCoursesDetails")
def all_courses_detailed():
    result = get_top_100_courses_with_all_details()
    return jsonify(result)

@app.route("/CourseById", methods=['POST', 'GET'])
def course_by_id():
    # course_id = 2830

    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])

    result = get_course_by_id(course_id)
    return jsonify(result)


@app.route("/similarCourses", methods=['POST', 'GET'])
def similar_courses():
    # course_id = 2830

    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])

    result = get_similar_courses(course_id)

    return jsonify(result)


@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.json('username')
    password = request.json('password')
    result = checkUser(username, password)
    return jsonify(result)


@app.route("/recommandUsers", methods=['POST', 'GET'])
def recommandUsers():

    # data = json.loads(request.data.decode())
    # course_id = int(data["idCourse"])
    # print(course_id)

    course_name = 'Financial Markets'
    result = collaborative_users(course_name)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
