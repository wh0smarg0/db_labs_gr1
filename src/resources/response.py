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
