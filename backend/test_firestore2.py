from google.cloud import firestore_v1

db = firestore_v1.Client(
    project="project-b154fb9d-0640-4e41-bae",
    database="default",
)

doc = db.collection("test").document("demo")
doc.set({"hello": "world"})

print("Success")