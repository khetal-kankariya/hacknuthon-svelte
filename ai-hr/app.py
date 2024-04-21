from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from models.userSchema import UserSchema
from models.questionsSchema import questionsSchema
from bson import json_util
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

try:
    client = MongoClient(
        'mongodb+srv://hrushi2501:TxckwkaV4pQSMvE@scriptsquad.ay4cntn.mongodb.net/?retryWrites=true&w=majority&appName=ScriptSquad')
    db = client['ScriptSquad']
    collection = db['user']
    question_collection = db['questions']
    response_collection = db['responses']
    print("Connected to MongoDB successfully!")
except ConnectionFailure as e:
    print("Could not connect to MongoDB:", e)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        role = data['role']
        # hashed_password = encrypt_password(password)

        user = UserSchema(email, password, role)
        collection.insert_one(user.to_dict())
        return 'User registered successfully!'
    except Exception as e:
        return f'Error registering user: {e}'


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user_data = collection.find_one({'email': email})
        # print(user_data)
        if (user_data['password'] == password):  # type: ignore
            return 'Login successful!'
        else:
            return 'Invalid username or password!'
    except Exception as e:
        return f'Error logging in: {e}'


@app.route('/hr/add_question', methods=['POST'])
def add_question():
    try:
        data = request.get_json()
        questions = data['questions']
        job_post = data['job_post']

        questions = questionsSchema(job_post, questions)
        question_collection.insert_one(questions.to_dict())

        return 'Questions submitted successfully!'
    except Exception as e:
        return f'Error registering user: {e}'


@app.route('/candidate/get_question', methods=['GET'])
def get_question():
    try:
        questions = question_collection.find()
        if questions:
            return json_util.dumps(questions)
        else:
            return 'No questions available.'
    except Exception as e:
        return f'Error: {e}'


@app.route('/candidate/save_response', methods=['POST'])
def save_response():
    try:
        data = request.get_json()
        email = data['email']
        job_post = data['job_post']
        response = data['response']

        response_data = {
            'email': email,
            'job_post': job_post,
            'response': response
        }

        response_collection.insert_one(response_data)

        return 'Response saved successfully!'
    except Exception as e:
        return f'Error saving response: {e}'


@app.route('/hr/get_response', methods=['GET'])
def get_response():
    try:
        job_post = request.args.get('job_post')
        print("Job Post:", job_post)  # Print job post for debugging

        responses = list(response_collection.find({'job_post': job_post}))
        print("Responses:", responses)  # Print responses for debugging

        if responses:
            return json_util.dumps(responses)
        else:
            return 'No responses available for this job post.'
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    app.run(debug=True)
