from flask import *
from flask_restful import *
from flask_restful.reqparse import *
from addict import *
from datetime import datetime

from models.score import Score
from mlab import *

mlab_connect()
app = Flask(__name__)
api = Api(app)

parser = RequestParser()
parser.add_argument('name', type=str, location='form')
parser.add_argument('score', type=int, location='form')

class ScoreRes(Resource):
    def get(self):
        return {
            'success': 1,
            'data': list2json(Score.objects())
        }

    def post(self):
        args = Dict(parser.parse_args())
        new_score = Score(name=args.name, score=args.score, added_time=datetime.now())
        new_score.save()
        return {
            'success': 1,
            'message': 'New score added successfully',
            'data': item2json(new_score)
        }

    def delete(self):
        Score.drop_collection()
        return {
            'success': 1,
            'message': 'Congrats, all data erased'
        }


class TopScoreRes(Resource):
    def get(self):
        highest_score = Score.objects().order_by('-score').limit(-1).first()
        if highest_score is None:
            return {
                'success': 0,
                'message': 'No score to return'
            }
        else:
            return {
                'success': 1,
                'message': 'Top score retrive successfully',
                'data': item2json(highest_score)
            }


api.add_resource(ScoreRes, '/score')
api.add_resource(TopScoreRes, '/top')

if __name__ == "__main__":
    app.run(debug=True)