import appcongif
import face_recognition
import os
import pickle

def match(unknown_images):
    attendance_list = []
    with open(appcongif.IMAGE_ENCODINGS + "/keyvalues.json"  , 'rb') as fp1:
        keyvalues1 = pickle.load(fp1)
    for images in unknown_images:

        for filename in keyvalues1:
            
            unknown_image = face_recognition.load_image_file(appcongif.IMAGES_UNKNOWN + "/" + images)
            unknown_encoding = face_recognition.face_encodings(unknown_image  )[0]
            results = face_recognition.compare_faces([keyvalues1[filename]], unknown_encoding, tolerance= 0.493)
            if results[0]:
                res = str(filename).split('.')
                attendance_list.append(res[0])
                print(filename + ' ' + images)
                break
    
    # print(attendance_list)
    return (attendance_list)
        

