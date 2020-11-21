from flask import Flask, request, jsonify
from flask_cors import CORS
from Database.database_interaction import *

app = Flask(__name__)
CORS(app)


@app.route("/allCourses")
def all_courses():
    result = get_all_courses()
    return jsonify(result)


@app.route("/CourseById", methods=['POST', 'GET'])
def course_by_id():
    course_id = request.json['idCourse']
    result = get_course_by_id(course_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run()