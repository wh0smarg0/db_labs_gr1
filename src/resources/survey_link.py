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
