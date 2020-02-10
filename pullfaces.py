from PIL import Image
import sys
import face_recognition
# import deleteGroupies
# import facematch
# import deleteUnknown
from app import app

def pull(imageList):
    for static_image in imageList:
        image = face_recognition.load_image_file(app.root_path+"/"+ app.config["IMAGES_TO_IDENTIFY"]+"/" + static_image)
        face_locations = face_recognition.face_locations(image)#,model="cnn",number_of_times_to_upsample=0)

        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            # pil_image.show()
            pil_image.save("static/unknown/" + f'{top}.jpg')


    #deleteGroupies.deleteImages()
    #facematch.match()
    #deleteUnknown.deleteImages()

imageList = ["1.jpeg","2.jpg"]
pull(imageList)


