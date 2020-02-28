from PIL import Image
import sys
import face_recognition
import brain.deleteImages
import brain.know_face_encodings
import appconfig
import shutil
import os , errno
import brain.facematch





def pull(imageList):
    cropped_image_list = [] 

    for static_image in imageList:
        image = face_recognition.load_image_file(appconfig.IMAGES_TO_IDENTIFY + "/" + static_image)
        face_locations = face_recognition.face_locations(image)#,model="cnn",number_of_times_to_upsample=0)
        

        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            # pil_image.show()
            appconfig.CROP_IMAGE_ID = appconfig.CROP_IMAGE_ID + 1
            temp_name = str(appconfig.CROP_IMAGE_ID) + ".jpeg" 
            cropped_image_list.append(temp_name)
            pil_image.save(appconfig.IMAGES_UNKNOWN + "/" + temp_name)

   

    brain.deleteImages.deleteImages( appconfig.IMAGES_TO_IDENTIFY, imageList)
    # brain.know_face_encodings.en()
    attendance_list = brain.facematch.match(cropped_image_list)

    return  attendance_list
