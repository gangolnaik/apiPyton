from flask import Flask, jsonify, request
import os, json

app = Flask(__name__)

@app.route('/courses', methods=['GET'])
def list_of_courses():
    if os.path.exists('data/courses.json'):
        with open('data/courses.json') as file:
            readData = file.read()
            coursesList = json.loads(readData)
            return jsonify(coursesList)
    else:
        coursesList = []
        with open('data/courses.json','w') as file:
            rawText = json.dumps(coursesList)
            file.write(rawText)
            file.close()

        return jsonify(rawText)


@app.route('/courses', methods=['POST'])
def create_course():
    course = request.json
    with open('data/courses.json') as file:
        readData = file.read()
        coursesList = json.loads(readData)
        course['id'] = len(coursesList) + 1
        if 'name' in course and 'description' in course:
            coursesList.append(course)
        else:
            return jsonify({'errorMsg':"Check your json."})
    with open('data/courses.json','w') as content:
        rawText = json.dumps(coursesList)
        content.write(rawText)
        content.close()

    return jsonify(course)


@app.route('/courses/<int:courseId>', methods=['GET'])
def get_course_by_id(courseId):
    with open('data/courses.json') as file:
        readData = file.read()
        coursesList = json.loads(readData)
        for course in coursesList:
            if course['id'] == courseId:
                return jsonify(course)

        return jsonify({"errorMsg":"Enter correct id of course."})

@app.route('/courses/<int:courseId>',methods=['PUT'])
def update_course_by_id(courseId):
    courseResponse = get_course_by_id(courseId)
    course = json.loads(courseResponse.data.decode('utf-8')) # Here we decode the response in bytes to dict type
    if 'name' in request.json and 'description' in request.json:
        course['name'] = request.json['name']
        course['description'] = request.json['description']
    elif 'name' in request.json:
        course['name'] = request.json['name']
    elif 'description' in request.json:
        course['description'] = request.json['description']
    else:
        return jsonify({"errorMsg":"Check your json file."})

    return jsonify(course)

@app.route('/courses/<int:courseId>/exercises',methods=['GET'])
def list_of_exercises(courseId):
    tmp_list = []
    if os.path.exists('data/exercises.json'):
        with open('data/exercises.json') as file:
            readData = file.read()
            exercisesList = json.loads(readData)
            for exercise in exercisesList:
                if exercise['courseId'] == courseId:
                    tmp_list.append(exercise)
        return jsonify(tmp_list)  
    else:
        exercisesList = []
        with open('data/exercises.json','w') as file:
            rawText = json.dumps(exercisesList)
            file.write(rawText)
            file.close()

        return jsonify(rawText)
    

@app.route('/courses/<int:courseId>/exercises',methods=['POST'])
def create_exercises(courseId):
    exercise = request.json
    with open('data/exercises.json') as file:
        readData = file.read()
        exercisesList = json.loads(readData)
        exercise['id'] = len(exercisesList) + 1
        exercise['courseId'] = courseId
        if 'name' in exercise and 'content' in exercise and 'hint' in exercise:
            exercisesList.append(exercise)
        else:
            return jsonify({"errorMsg":"Check your json file"})

    with open('data/exercises.json','w') as content:
        rawText = json.dumps(exercisesList)
        content.write(rawText)
        content.close()

    return jsonify(exercise)

@app.route('/courses/<int:courseId>/exercises/<int:exerciseId>',methods=['GET'])
def get_exercise_by_id(courseId,exerciseId):
    with open('data/exercises.json') as file:
        readData = file.read()
        exercisesList = json.loads(readData)
        for exercise in exercisesList:
            if exercise['courseId'] == courseId and exercise['id'] == exerciseId:
                return jsonify(exercise)
        return jsonify({"errorMsg":"Enter coorect id of exersise or course"})

@app.route('/courses/<int:courseId>/exercises/<int:exerciseId>',methods=['PUT'])
def update_exercise_by_id(courseId,exerciseId):
    exerciseResponse = get_exercise_by_id(courseId,exerciseId)
    exercise = json.loads(exerciseResponse.data.decode('utf-8')) # Here we decode the response in bytes to dict type
    if 'name' in request.json and 'content' in request.json and 'hint' in request.json:
        exercise['name'] = request.json['name']
        exercise['content'] = request.json['content']
        exercise['hint'] = request.json['hint']
    elif 'name' in request.json:
        exercise['name'] = request.json['name']
    elif 'content' in request.json:
        course['content'] = request.json['content']
    elif 'hint' in request.json:
        exercise['hint'] = request.json['hint']
    else:
        return jsonify({"errorMsg":"Check your json file."})

    return jsonify(exercise)     

@app.route('/courses/<int:courseId>/exercises/<int:exerciseId>/submissions',methods=['GET'])
def list_of_submissions(courseId,exerciseId):
    if os.path.exists('data/submissions.json'):
        with open('data/submissions.json') as file:
            readData = file.read()
            submissionsList = json.loads(readData)
            return jsonify(submissionsList)
    else:
        submissionsList = []
        with open('data/submissions.json','w') as file:
            rawText = json.dumps(submissionsList)
            file.write(rawText)
            file.close()

        return jsonify(rawText)

@app.route('/courses/<int:courseId>/exercises/<int:exerciseId>/submissions',methods=['POST'])
def create_submissions(courseId,exerciseId):
    submission = request.json
    with open('data/submissions.json') as file:
        readData = file.read()
        submissionsList = json.loads(readData)
        submission['id'] = len(submissionsList) + 1
        submission['courseId'] = courseId
        submission['exerciseId'] = exerciseId
        if 'userName' in submission and 'content' in submission:
            submissionsList.append(submission)
        else:
            return jsonify({"errorMsg":"Check your json file"})
    with open('data/submissions.json','w') as content:
        rawText = json.dumps(submissionsList)
        content.write(rawText)
        content.close()
    return jsonify(submission)

if __name__ == '__main__':
    app.run(debug=True)
