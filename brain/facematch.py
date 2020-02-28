import appconfig
import face_recognition
import os
import pickle
import shutil

def match(unknown_images):
    attendance_list = []
    unidentified_list = []
    flag = 0
    with open(appconfig.IMAGE_ENCODINGS + "/keyvalues.json"  , 'rb') as fp1:
        keyvalues1 = pickle.load(fp1)
    for images in unknown_images:

        for filename in keyvalues1:
            
            unknown_image = face_recognition.load_image_file(appconfig.IMAGES_UNKNOWN + "/" + images)
            unknown_encoding = face_recognition.face_encodings(unknown_image  )[0]
            results = face_recognition.compare_faces([keyvalues1[filename]], unknown_encoding, tolerance= 0.48)
            if results[0]:
                res = str(filename).split('.')
                attendance_list.append(res[0])
                print(filename + ' ' + images)
                flag = 1
                break
        if (flag==0):
            shutil.copy(appconfig.IMAGES_UNKNOWN + "/" + images  ,appconfig.IMAGES_UNIDENTIFIED + "/" + images)
            res1 = str(images).split('.')
            unidentified_list.append(res1[0])
        flag = 0
    
    return {"identified" : attendance_list , "unidentified" : unidentified_list}
        

