from flask import *
from flask_restful import *
from flask_restful.reqparse import *
from addict import *
from datetime import datetime, timedelta
from flask_cors import CORS

from models.score import Score
from mlab import *

mlab_connect()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

parser = RequestParser()
parser.add_argument('name', type=str, location='form')
parser.add_argument('score', type=int, location='form')


@app.route('/')
def index():
    return render_template("index.html")


class ScoreRes(Resource):
    def get(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        pipeline_topten_today = [
            {
                '$match': {
                    'added_time': {'$gte': today - timedelta(days=1)}
                }
            },
            {
                       '$sort': {'score': -1}
            },
            {
                '$limit': 10
            }
        ]

        pipeline_ten_lastrecord = [
            {
                '$limit': 10
            },
            {
               '$sort': {'score': -1}
            }
        ]

        top_ten = Score.objects.aggregate(*pipeline_topten_today)

        if len([score for score in top_ten]) < 10:
            top_ten = Score.objects.aggregate(*pipeline_ten_lastrecord)

        return {
            'success': 1,
            'data': [{
                'score': score['score'],
                'name': score['name']
            } for score in top_ten]
        }

    def post(self):
        args = Dict(parser.parse_args())
        new_score = Score(name=args.name, score=args.score, added_time=datetime.now())
        new_score.save()
        return {
            'success': 1,
            'message': 'New score added successfully',
            'data': {
                'score': new_score.score,
                'name': new_score.name
            }
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
                'message': 'Top score retrived successfully',
                'data': {
                    'score': highest_score.score,
                    'name': highest_score.name
                }
            }


api.add_resource(ScoreRes, '/score')
api.add_resource(TopScoreRes, '/top')

if __name__ == "__main__":
    app.run(debug=True)
