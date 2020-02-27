import face_recognition
import os
import appcongif
import pickle

keyvalues = {}
def en ():
    for filename in os.listdir(appcongif.IMAGES_KNOWN):
        known_image = face_recognition.load_image_file(appcongif.IMAGES_KNOWN + "/" + filename )
        known_encoding = face_recognition.face_encodings(known_image , model = "small")[0]
        keyvalues.update({filename : known_encoding})

    with open(appcongif.IMAGE_ENCODINGS + "/keyvalues.json"  , 'wb') as fp:
        pickle.dump(keyvalues, fp)   
    
    # print (len(known_encoding))
    # print(keyvalues)
    
        