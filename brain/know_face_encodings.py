import face_recognition
import os
import appcongif
import pickle

keyvalues = {}
def en ():
    for filename in os.listdir(appcongif.IMAGES_KNOWN):
        known_image = face_recognition.load_image_file(appcongif.IMAGES_KNOWN + "/" + filename )
        height, width, _ = known_image.shape
        # location is in css order - top, right, bottom, left
        face_location = (0, width, height, 0)

        encodings = face_recognition.face_encodings(known_image, known_face_locations=[face_location])[0]
        
        print(encodings)
        # print(face_recognition.face_encodings(known_image)[0])
        keyvalues.update({filename : encodings})

    with open(appcongif.IMAGE_ENCODINGS + "/keyvalues.json"  , 'wb') as fp:
        pickle.dump(keyvalues, fp)   
    
    # print (known_encoding)
    # print(keyvalues)
    
        