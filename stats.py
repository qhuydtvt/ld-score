from models.score import Score
from mlab import mlab_connect

if __name__ == "__main__":
    mlab_connect()
    pipeline_by_user = [
        {
            '$sort': {'name': -1}
        },
        {
            '$limit' : 1000
        }
    ]

    print(Score.objects(name='Shivur').count())

    records = Score.objects.aggregate(*pipeline_by_user)
    for record in records:
        print(record['name'])