from PIL import Image
import sys
import face_recognition
import brain.deleteImages
import brain.know_face_encodings
import appcongif
import shutil
import os , errno
import brain.facematch





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
            pil_image.save(appcongif.IMAGES_UNKNOWN + "/" + temp_name)

   

    # brain.deleteImages.deleteImages( appcongif.IMAGES_TO_IDENTIFY, imageList)
    # brain.know_face_encodings.en()
    attendance_list = brain.facematch.match(cropped_image_list)
    # return_list = []
    # unidentified_list = []
    
    # print(attendance_list)
    
    # for l in attendance_list:
    #     appcongif.COUNT = appcongif.COUNT + 1
        
    #     if(l == 'unknown_person' or l=='no_persons_found'):
    #         unknown_image = appcongif.IMAGES_UNIDENTIFIED +"/" + str(appcongif.COUNT) + ".jpeg"
    #         shutil.copy(appcongif.IMAGES_UNKNOWN + "/" + str(appcongif.COUNT) + ".jpeg" ,unknown_image)
    #         unidentified_list.append(str(appcongif.COUNT))

    #     else: 
    #         return_list.append(l)
            
    # brain.deleteImages.deleteImages(appcongif.IMAGES_UNKNOWN, cropped_image_list)
    # brain.deleteImages.deleteImages(appcongif.IMAGES_UNKNOWN, cropped_image_list)
    
    

    
    # return " "
    return {"identified" : attendance_list}

    
    # return {"identified" : return_list , "unidentified" : unidentified_list}