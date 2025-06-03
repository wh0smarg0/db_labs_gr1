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
