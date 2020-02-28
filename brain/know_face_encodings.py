import face_recognition
import os
import appconfig
import pickle

keyvalues = {}
def en ():
    for filename in os.listdir(appconfig.IMAGES_KNOWN):
        
        known_image = face_recognition.load_image_file(appconfig.IMAGES_KNOWN + "/" + filename )
        known_face_encodings = face_recognition.face_encodings(known_image)

        if len(known_face_encodings) > 0:
            known_encoding = face_recognition.face_encodings(known_image )[0]
            keyvalues.update({filename : known_encoding})

    with open(appconfig.IMAGE_ENCODINGS + "/keyvalues.json"  , 'wb') as fp:
        pickle.dump(keyvalues, fp)   
    
    print (len(keyvalues))
    
        