import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds129946.mlab.com:29946/ld-score

host = "ds129946.mlab.com"
port = 29946
db_name = "ld-score"
user_name = "admin"
password = "codethechange123"


def mlab_connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())