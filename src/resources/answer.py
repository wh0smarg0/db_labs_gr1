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

        # 🔍 Перевірка наявності responseId і questionId
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
