from google.cloud import firestore
from app.config import PROJECT_ID

print("PROJECT_ID:", PROJECT_ID)

db = firestore.Client(project=PROJECT_ID)

print("Client project:", db.project)

doc = db.collection("test").document("demo")

doc.set({
    "message": "Hello Firestore!"
})

print("Success!")