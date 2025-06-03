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
