# Реалізація інформаційного та програмного забезпечення

У рамках проєкту розробляється:
- SQL-скрипти для створення та початкового наповнення бази даних;
- RESTfull сервіс для керування обліковими записами користувачів системи.


## SQL-скрипти
### main.sql
```sql
  CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordHash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    isActive BOOLEAN NOT NULL
);

CREATE TABLE Survey (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    creationDate DATETIME NOT NULL,
    closeDate DATETIME,
    userId INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE Question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    isRequired BOOLEAN NOT NULL,
    `order` INT NOT NULL,
    surveyId INT NOT NULL,
    FOREIGN KEY (surveyId) REFERENCES Survey(id) ON DELETE CASCADE
);

CREATE TABLE SurveyLink (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(100) NOT NULL UNIQUE,
    isActive BOOLEAN NOT NULL,
    expiryDate DATETIME,
    clicks INT NOT NULL DEFAULT 0,
    surveyId INT NOT NULL,
    FOREIGN KEY (surveyId) REFERENCES Survey(id) ON DELETE CASCADE
);

CREATE TABLE Response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submissionDate DATETIME NOT NULL,
    isComplete BOOLEAN NOT NULL,
    surveyLinkId INT NOT NULL,
    FOREIGN KEY (surveyLinkId) REFERENCES SurveyLink(id) ON DELETE CASCADE
);

CREATE TABLE Answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value TEXT NOT NULL,
    responseId INT NOT NULL,
    questionId INT NOT NULL,
    FOREIGN KEY (responseId) REFERENCES Response(id) ON DELETE CASCADE,
    FOREIGN KEY (questionId) REFERENCES Question(id) ON DELETE CASCADE
);
```

### test_d.sql
```sql
  INSERT INTO User (email, passwordHash, role, isActive) VALUES
('admin@example.com', 'hash1', 'admin', TRUE),
('user1@example.com', 'hash2', 'respondent', TRUE),
('user2@example.com', 'hash3', 'respondent', TRUE);

INSERT INTO Survey (title, description, status, creationDate, closeDate, userId) VALUES
('Customer Satisfaction Survey', 'Tell us about your experience.', 'active', NOW(), NULL, 1),
('Product Feedback', 'We value your thoughts on our new product.', 'draft', NOW(), NULL, 1),
('Website Usability', 'How easy is it to use our website?', 'active', NOW(), NULL, 1);

INSERT INTO Question (text, type, isRequired, `order`, surveyId) VALUES
-- Survey 1
('How satisfied are you?', 'rating', TRUE, 1, 1),
('What can we improve?', 'text', FALSE, 2, 1),
-- Survey 2
('Is the product useful?', 'yesno', TRUE, 1, 2),
('Would you recommend it?', 'yesno', TRUE, 2, 2),
-- Survey 3
('Was the site easy to navigate?', 'yesno', TRUE, 1, 3),
('Any technical issues?', 'text', FALSE, 2, 3);

INSERT INTO SurveyLink (token, isActive, expiryDate, clicks, surveyId) VALUES
('link1', TRUE, DATE_ADD(NOW(), INTERVAL 10 DAY), 5, 1),
('link2', TRUE, DATE_ADD(NOW(), INTERVAL 5 DAY), 0, 1),
('link3', TRUE, DATE_ADD(NOW(), INTERVAL 15 DAY), 2, 2),
('link4', TRUE, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 3);

INSERT INTO Response (submissionDate, isComplete, surveyLinkId) VALUES
(NOW(), TRUE, 1),
(NOW(), TRUE, 2),
(NOW(), FALSE, 3),
(NOW(), TRUE, 4);

-- Response 1 (link1, survey 1)
INSERT INTO Answer (value, responseId, questionId) VALUES
('4', 1, 1),
('More options needed.', 1, 2);

-- Response 2 (link2, survey 1)
INSERT INTO Answer (value, responseId, questionId) VALUES
('5', 2, 1),
('Nothing to improve.', 2, 2);

-- Response 3 (link3, survey 2) — incomplete, only one answer
INSERT INTO Answer (value, responseId, questionId) VALUES
('Yes', 3, 3);

-- Response 4 (link4, survey 3)
INSERT INTO Answer (value, responseId, questionId) VALUES
('Yes', 4, 5),
('No issues', 4, 6);
```


## RESTfull сервіс для управління даними
### Ресурси
user.py
```py
from flask_restful import Resource, reqparse
from models import db,User

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('passwordHash', type=str, required=True)
parser.add_argument('role', type=str, required=True)
parser.add_argument('isActive', type=bool, required=True)

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': u.id, 'email': u.email, 'role': u.role, 'isActive': u.isActive} for u in users]

    def post(self):
        args = parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created', 'id': user.id}, 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'email': user.email, 'role': user.role, 'isActive': user.isActive}

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = parser.parse_args()
        for key, value in args.items():
            setattr(user, key, value)
        db.session.commit()
        return {'message': 'User updated'}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}

```
survey-links.py
```py
from flask_restful import Resource, reqparse
from models import db, SurveyLink
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True)
parser.add_argument('isActive', type=bool, required=True)
parser.add_argument('expiryDate', type=str)
parser.add_argument('clicks', type=int)
parser.add_argument('surveyId', type=int, required=True)

class SurveyLinkListResource(Resource):
    def get(self):
        links = SurveyLink.query.all()
        return [{'id': l.id, 'token': l.token, 'isActive': l.isActive} for l in links]

    def post(self):
        args = parser.parse_args()
        if args['expiryDate']:
            args['expiryDate'] = datetime.fromisoformat(args['expiryDate'])
        link = SurveyLink(**args)
        db.session.add(link)
        db.session.commit()
        return {'message': 'Survey link created', 'id': link.id}, 201

class SurveyLinkResource(Resource):
    def get(self, link_id):
        l = SurveyLink.query.get_or_404(link_id)
        return {'id': l.id, 'token': l.token, 'isActive': l.isActive, 'clicks': l.clicks}

    def put(self, link_id):
        l = SurveyLink.query.get_or_404(link_id)
        args = parser.parse_args()
        if args['expiryDate']:
            args['expiryDate'] = datetime.fromisoformat(args['expiryDate'])
        for k, v in args.items():
            setattr(l, k, v)
        db.session.commit()
        return {'message': 'Survey link updated'}

    def delete(self, link_id):
        l = SurveyLink.query.get_or_404(link_id)
        db.session.delete(l)
        db.session.commit()
        return {'message': 'Survey link deleted'}
```
survey.py
```py
from flask_restful import Resource, reqparse
from models import db, Survey
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True)
parser.add_argument('description', type=str)
parser.add_argument('status', type=str, required=True)
parser.add_argument('creationDate', type=str, required=True)
parser.add_argument('closeDate', type=str)
parser.add_argument('userId', type=int, required=True)

class SurveyListResource(Resource):
    def get(self):
        surveys = Survey.query.all()
        return [{'id': s.id, 'title': s.title, 'status': s.status} for s in surveys]

    def post(self):
        args = parser.parse_args()
        args['creationDate'] = datetime.fromisoformat(args['creationDate'])
        if args['closeDate']:
            args['closeDate'] = datetime.fromisoformat(args['closeDate'])
        survey = Survey(**args)
        db.session.add(survey)
        db.session.commit()
        return {'message': 'Survey created', 'id': survey.id}, 201

class SurveyResource(Resource):
    def get(self, survey_id):
        s = Survey.query.get_or_404(survey_id)
        return {'id': s.id, 'title': s.title, 'description': s.description, 'status': s.status}

    def put(self, survey_id):
        s = Survey.query.get_or_404(survey_id)
        args = parser.parse_args()
        args['creationDate'] = datetime.fromisoformat(args['creationDate'])
        if args['closeDate']:
            args['closeDate'] = datetime.fromisoformat(args['closeDate'])
        for k, v in args.items():
            setattr(s, k, v)
        db.session.commit()
        return {'message': 'Survey updated'}

    def delete(self, survey_id):
        s = Survey.query.get_or_404(survey_id)
        db.session.delete(s)
        db.session.commit()
        return {'message': 'Survey deleted'}
```
response.py
```py
from flask_restful import Resource, reqparse
from models import db, Response
from datetime import datetime

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('true', '1', 't', 'y', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'f', 'n', 'no'):
        return False
    else:
        raise ValueError('Boolean value expected.')

parser = reqparse.RequestParser()
parser.add_argument('submissionDate', type=str, required=True)
parser.add_argument('isComplete', type=str_to_bool, required=True)
parser.add_argument('surveyLinkId', type=int, required=True)

class ResponseListResource(Resource):
    def get(self):
        responses = Response.query.all()
        return [{'id': r.id, 'isComplete': r.isComplete, 'surveyLinkId': r.surveyLinkId} for r in responses]

    def post(self):
        args = parser.parse_args()
        args['submissionDate'] = datetime.fromisoformat(args['submissionDate'])
        response = Response(**args)
        db.session.add(response)
        db.session.commit()
        return {'message': 'Response created', 'id': response.id}, 201

class ResponseResource(Resource):
    def get(self, response_id):
        r = Response.query.get_or_404(response_id)
        return {'id': r.id, 'submissionDate': r.submissionDate.isoformat(), 'isComplete': r.isComplete}

    def put(self, response_id):
        r = Response.query.get_or_404(response_id)
        args = parser.parse_args()
        args['submissionDate'] = datetime.fromisoformat(args['submissionDate'])
        for k, v in args.items():
            setattr(r, k, v)
        db.session.commit()
        return {'message': 'Response updated'}

    def delete(self, response_id):
        r = Response.query.get_or_404(response_id)
        db.session.delete(r)
        db.session.commit()
        return {'message': 'Response deleted'}
```
question.py
```py
from flask_restful import Resource, reqparse
from models import db, Question

parser = reqparse.RequestParser()
parser.add_argument('text', type=str, required=True)
parser.add_argument('type', type=str, required=True)
parser.add_argument('isRequired', type=bool, required=True)
parser.add_argument('order', type=int, required=True)
parser.add_argument('surveyId', type=int, required=True)

class QuestionListResource(Resource):
    def get(self):
        questions = Question.query.all()
        return [{'id': q.id, 'text': q.text, 'type': q.type, 'isRequired': q.isRequired} for q in questions]

    def post(self):
        args = parser.parse_args()
        question = Question(**args)
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question created', 'id': question.id}, 201

class QuestionResource(Resource):
    def get(self, question_id):
        q = Question.query.get_or_404(question_id)
        return {'id': q.id, 'text': q.text, 'type': q.type, 'isRequired': q.isRequired, 'order': q.order}

    def put(self, question_id):
        q = Question.query.get_or_404(question_id)
        args = parser.parse_args()
        for k, v in args.items():
            setattr(q, k, v)
        db.session.commit()
        return {'message': 'Question updated'}

    def delete(self, question_id):
        q = Question.query.get_or_404(question_id)
        db.session.delete(q)
        db.session.commit()
        return {'message': 'Question deleted'}
```
answer.py
```py
from flask_restful import Resource, reqparse
from models import db, Answer, Response, Question

parser = reqparse.RequestParser()
parser.add_argument('value', type=str, required=True)
parser.add_argument('responseId', type=int, required=True)
parser.add_argument('questionId', type=int, required=True)

class AnswerListResource(Resource):
    def get(self):
        answers = Answer.query.all()
        return [{'id': a.id, 'value': a.value, 'responseId': a.responseId, 'questionId': a.questionId} for a in answers]

    def post(self):
        args = parser.parse_args()

        # Перевірка наявності responseId і questionId
        if not Response.query.get(args['responseId']):
            return {'message': f"Response with id {args['responseId']} not found"}, 404
        if not Question.query.get(args['questionId']):
            return {'message': f"Question with id {args['questionId']} not found"}, 404

        try:
            answer = Answer(**args)
            db.session.add(answer)
            db.session.commit()
            return {'message': 'Answer created', 'id': answer.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Internal error: {str(e)}'}, 500

class AnswerResource(Resource):
    def get(self, answer_id):
        a = Answer.query.get_or_404(answer_id)
        return {'id': a.id, 'value': a.value, 'responseId': a.responseId, 'questionId': a.questionId}

    def put(self, answer_id):
        a = Answer.query.get_or_404(answer_id)
        args = parser.parse_args()
        for k, v in args.items():
            setattr(a, k, v)
        db.session.commit()
        return {'message': 'Answer updated'}

    def delete(self, answer_id):
        a = Answer.query.get_or_404(answer_id)
        db.session.delete(a)
        db.session.commit()
        return {'message': 'Answer deleted'}
```
app.py
```py
from flask import Flask
from flask_restful import Api
from models import db

# Імпорт ресурсів
from DB.user import UserResource, UserListResource
from DB.survey import SurveyResource, SurveyListResource
from DB.question import QuestionResource, QuestionListResource
from DB.survey_link import SurveyLinkResource, SurveyLinkListResource
from DB.response import ResponseResource, ResponseListResource
from DB.answer import AnswerResource, AnswerListResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wh0smarg0:1234@localhost/lab6_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

# USERS
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

# SURVEYS
api.add_resource(SurveyListResource, '/surveys')
api.add_resource(SurveyResource, '/surveys/<int:survey_id>')

# QUESTIONS
api.add_resource(QuestionListResource, '/questions')
api.add_resource(QuestionResource, '/questions/<int:question_id>')

# SURVEY LINKS
api.add_resource(SurveyLinkListResource, '/survey-links')
api.add_resource(SurveyLinkResource, '/survey-links/<int:link_id>')

# RESPONSES
api.add_resource(ResponseListResource, '/responses')
api.add_resource(ResponseResource, '/responses/<int:response_id>')

# ANSWERS
api.add_resource(AnswerListResource, '/answers')
api.add_resource(AnswerResource, '/answers/<int:answer_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Створити всі таблиці, якщо ще не існують
    app.run(debug=True)
```
models.py
```py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    passwordHash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)

    surveys = db.relationship('Survey', backref='user', cascade="all, delete-orphan")

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False)
    creationDate = db.Column(db.DateTime, nullable=False)
    closeDate = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    questions = db.relationship('Question', backref='survey', cascade="all, delete-orphan")
    links = db.relationship('SurveyLink', backref='survey', cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    isRequired = db.Column(db.Boolean, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    surveyId = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

    answers = db.relationship('Answer', backref='question', cascade="all, delete-orphan")

class SurveyLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)
    isActive = db.Column(db.Boolean, nullable=False)
    expiryDate = db.Column(db.DateTime)
    clicks = db.Column(db.Integer, default=0, nullable=False)
    surveyId = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

    responses = db.relationship('Response', backref='survey_link', cascade="all, delete-orphan")

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submissionDate = db.Column(db.DateTime, nullable=False)
    isComplete = db.Column(db.Boolean, nullable=False)
    surveyLinkId = db.Column(db.Integer, db.ForeignKey('survey_link.id'), nullable=False)

    answers = db.relationship('Answer', backref='response', cascade="all, delete-orphan")

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    responseId = db.Column(db.Integer, db.ForeignKey('response.id'), nullable=False)
    questionId = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
```
