
import firebase_admin
from firebase_admin import firestore, auth, credentials, storage
from datetime import datetime

from AnalysisVideo import AnalysisVideo


class ConnectFirebase:
    def __init__(self,user, type_result, num_exercises, type_and_count, experience_num):
        cred = credentials.Certificate("reference_files/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"storageBucket": "wayspeack.appspot.com"})

        self.connect_user()
        image_normal_get = self.image_normal(user)
        image_best = self.read_best_result(user, type_result)
        video_exercises = self.read_exercises(user, num_exercises, type_and_count, experience_num)
        self.analysis_video = AnalysisVideo(image_normal_get, video_exercises, image_best, type_result)
        if 'tongue' in type_result:
            if self.analysis_video.progress_bool_comparison:
                self.update_best_result(user, type_result, "")
        else:
            if self.analysis_video.result_max_comparison != 0 and self.analysis_video.result_max_comparison != 10000000000:
                bucket_name = "gs://wayspeack.appspot.com"
                local_image_path = "output_image.png"
                destination_blob_name = "images/"+user+"/Exercises/"+num_exercises+"/Type/"+type_and_count+"/Experience/" \
                                    +experience_num+"/image.jpg"
                image_url = self.upload_image_to_storage(local_image_path, destination_blob_name)
                experience_num_re = self.remove_spaces(experience_num)
                image_url = "https://firebasestorage.googleapis.com/v0/b/wayspeack.appspot.com/o/images%2F"+user+"%2FExercises%2F"+num_exercises+"%2FType%2F"+type_and_count+"%2FExperience%2F"+experience_num_re+"%20%2Fimage.jpg?alt=media"
                self.update_exercises(user, num_exercises, type_and_count, experience_num, image_url, True, self.analysis_video.progress_bool_comparison)
                if self.analysis_video.progress_bool_comparison:
                    self.update_best_result(user, type_result, image_url)


        self.close_connect()

    def remove_spaces(self, input_string):
        return input_string.replace(" ", "")

    def connect_user(self):
        email = "jjjj@gmail.com"
        password = "123456"

        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            print("Successfully created user:", user.uid)
        except auth.EmailAlreadyExistsError:
            print("User with this email already exists.")
        except Exception as e:
            print("Error creating user:", str(e))

    def image_normal(self, user):
        return "https://firebasestorage.googleapis.com/v0/b/wayspeack.appspot.com/o/images%2F"+user+"%2Fcomparison%2Fimage.jpg?alt=media"

    def read_best_result(self,user, type_result):
        db = firestore.client()

        collection_name1 = "clinician"
        document_id1 = "clinic1"
        collection_name2 = "Patients"
        document_id2 = user
        collection_name3 = "BestResults"
        document_id3 = type_result
        doc_ref = db.collection(collection_name1).document(document_id1).collection(collection_name2).document(document_id2).collection(collection_name3).document(document_id3)

        try:
            snapshot = doc_ref.get()
            if snapshot.exists:
                data = snapshot.to_dict()
                print("Document data:", data)
                image_url = data.get("image")
                date_url = data.get("date")
                return image_url
            else:
                print("Document not found.")
        except Exception as e:
            print("Error getting document:", str(e))


    def get_formatted_date(self):
        now = datetime.now()
        formatted_date = now.strftime("%d/%m/%y_%H:%M")
        return formatted_date



    def update_best_result(self,user, type_result, new_image_url):
        db = firestore.client()

        collection_name1 = "clinician"
        document_id1 = "clinic1"
        collection_name2 = "Patients"
        document_id2 = user
        collection_name3 = "BestResults"
        document_id3 = type_result
        doc_ref = db.collection(collection_name1).document(document_id1).collection(collection_name2).document(
            document_id2).collection(collection_name3).document(document_id3)
        formatted_date = self.get_formatted_date()
        try:
            doc_ref.update({"image": new_image_url})
            doc_ref.update({"date": formatted_date})

            print("Image URL updated successfully.")
        except Exception as e:
            print("Error updating Image URL:", str(e))


    def read_exercises(self, user, num_exercises, type_and_count, experience_num):
        db = firestore.client()
        collection_name1 = "clinician"
        document_id1 = "clinic1"
        collection_name2 = "Patients"
        document_id2 = user
        collection_name3 = "Exercises"
        document_id3 = num_exercises
        collection_name4 = "Type"
        document_id4 = type_and_count
        collection_name5 = "Experience"
        document_id5 = experience_num

        doc_ref = db.collection(collection_name1).document(document_id1).collection(collection_name2)\
            .document(document_id2).collection(collection_name3).document(document_id3).collection(collection_name4)\
            .document(document_id4).collection(collection_name5).document(document_id5)

        try:
            snapshot = doc_ref.get()
            if snapshot.exists:
                data = snapshot.to_dict()
                print("Document data:", data)
                image_url = data.get("Image")
                date_url = data.get("date")
                progress_url = data.get("progress")
                success_url = data.get("success")
                video_url = data.get("video")
                return video_url
            else:
                print("Document not found.")
        except Exception as e:
            print("Error getting document:", str(e))

    def update_exercises(self, user, num_exercises, type_and_count, experience_num, new_image_url, new_success, new_progress):
        db = firestore.client()
        collection_name1 = "clinician"
        document_id1 = "clinic1"
        collection_name2 = "Patients"
        document_id2 = user
        collection_name3 = "Exercises"
        document_id3 = num_exercises
        collection_name4 = "Type"
        document_id4 = type_and_count
        collection_name5 = "Experience"
        document_id5 = experience_num

        doc_ref = db.collection(collection_name1).document(document_id1).collection(collection_name2) \
            .document(document_id2).collection(collection_name3).document(document_id3).collection(collection_name4) \
            .document(document_id4).collection(collection_name5).document(document_id5)

        try:
            doc_ref.update({"Image": new_image_url})
            doc_ref.update({"success": new_success})
            doc_ref.update({"progress": new_progress})
            print("Image URL updated successfully.")
        except Exception as e:
            print("Error updating Image URL:", str(e))


    def upload_image_to_storage(self, local_image_path, destination_blob_name):
        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_image_path)
        url = blob.generate_signed_url(expiration=300, method='GET', version='v4')
        return url


    def close_connect(self):
        firebase_admin.delete_app(firebase_admin.get_app())












