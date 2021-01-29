from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache

from CollaborativeFilter.UserRecomandation import collaborative_users
from Database.DBInteractCourses import *
from Database.DBUser import checkUser
from SimilarityMethods.DescriptionSimilarity import get_similar_courses
from SimilarityMethods.RatingCommentSimilarity import get_similar_review_comments
import json

app = Flask(__name__)
CORS(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.json('username')
    password = request.json('password')
    result = checkUser(username, password)
    return jsonify(result)


@app.route("/allCourses")
@cache.cached(timeout=50)
def all_courses():
    result = get_all_courses()
    return jsonify(result)


@app.route("/allCoursesDetails")
@cache.cached(timeout=50)
def all_courses_detailed():
    result = get_top_100_courses_with_all_details()
    return jsonify(result)


@app.route("/CourseById", methods=['POST', 'GET'])
@cache.cached(timeout=50)
def course_by_id():
    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])
    result = get_course_by_id(course_id)
    return jsonify(result)


@app.route("/similarCourses", methods=['POST', 'GET'])
@cache.cached(timeout=50)
def similar_courses():
    # course_id = 3640
    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])
    result = get_similar_courses(course_id)
    return jsonify(result)


@app.route("/similarReview", methods=['POST', 'GET'])
@cache.cached(timeout=50)
def similar_course_reviews():
    # course_id = 3640
    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])
    result = get_similar_review_comments(course_id)
    return jsonify(result)


@app.route("/recommendUsers", methods=['POST', 'GET'])
@cache.cached(timeout=50)
def recommend_users():
    course_name = 'Getting Started with SAS Programming'
    data = json.loads(request.data.decode())
    course_id = int(data["idCourse"])
    result = get_courses_by_ids(collaborative_users(course_id))
    return jsonify(result)


@app.route("/coursesWithFilters", methods=['POST', 'GET'])
@cache.cached(timeout=50)
def courses_with_filters():
    data = json.loads(request.data.decode())
    filters = list(data["filters"])
    result = get_courses_with_filters(filters)

    return jsonify(result)

if __name__ == "__main__":
    app.run()
