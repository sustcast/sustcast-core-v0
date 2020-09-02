import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

TAG="@FIREBASE>"


def initialize(FIREBASE_DB_URL, FIREBASE_CREDENTIAL_PATH):
    global songref
    global iceref

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })

    songref = db.reference('song/')
    iceref = db.reference("IcecastServer")





temp_dict = {"name": 'tananannanana', "artist": 'nazi'}


def put_artist_title(gDict):
    keys = list(gDict.keys())
    for i in keys:
        # firebase.put('song/',str(i),str(gDict.get(i)))
        songref.update({
            str(i): str(gDict.get(i))
        })
        print(TAG,i, "-------", gDict.get(i))


#put_artist_title(dict)
# print(result)


def read_firebase(param):
    if(param == 1):
        result = songref.get()
    elif (param == 2):
        result = iceref.get()

    return result


# read_firebase()

def update_listeners(url, numList):
    result = read_firebase(2)
    for p, c in result.items():
        if (c["url"] == url and c["limit"] > numList):
            print(p)
            print(c)
            iceref.child(str(p)).update({"numlisteners": numList})

        else:
            print("Invalid URL or numlisteners")


#update_listeners("facebook.com", 20)