from PIL import Image
import sys
import face_recognition
import brain.deleteImages
import brain.facematch
import appcongif
import os , errno



location = appcongif.IMAGES_UNKNOWN
try:
    os.makedirs(location)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

def pull(imageList):
    cropped_image_list = [] 

    for static_image in imageList:
        image = face_recognition.load_image_file(appcongif.IMAGES_TO_IDENTIFY + "/" + static_image)
        face_locations = face_recognition.face_locations(image)#,model="cnn",number_of_times_to_upsample=0)
        

        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            # pil_image.show()
            appcongif.CROP_IMAGE_ID = appcongif.CROP_IMAGE_ID + 1
            temp_name = str(appcongif.CROP_IMAGE_ID) + ".jpeg" 
            cropped_image_list.append(temp_name)
            pil_image.save(appcongif.IMAGES_UNKNOWN+"/" + temp_name)

   

    brain.deleteImages.deleteImages( appcongif.IMAGES_TO_IDENTIFY, imageList)
    attendance_list = brain.facematch.match(cropped_image_list)
    brain.deleteImages.deleteImages(appcongif.IMAGES_UNKNOWN, cropped_image_list)
    
  

    

    return {"identified" : attendance_list}

    
    