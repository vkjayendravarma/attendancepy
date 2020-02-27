import appcongif
import face_recognition
import os
import pickle

def match(unknown_images):
    attendance_list = []
    with open(appcongif.IMAGE_ENCODINGS + "/keyvalues.json"  , 'rb') as fp1:
        keyvalues1 = pickle.load(fp1)
    for images in unknown_images:
    #     p = subprocess.run('face_recognition --tolerance 0.5 --cpus 8 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, capture_output = True)
    #     s = p.stdout
    #     res = str(s).split(',')
    #     res[1] = str(res[1]).replace('\\r\\n\'' ,'')
    #     attendance_list.append(res[1])
    # return (attendance_list)
        # data = subprocess.Popen('face_recognition --tolerance 0.48 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, stdout = subprocess.PIPE)
        # output = data.communicate()
        # res = str(output).split(',')
        # res[1] = str(res[1]).replace('\\n\'' ,'')
        # attendance_list.append(res[1])
        # print(str(output))

        for filename in keyvalues1:
            
            unknown_image = face_recognition.load_image_file(appcongif.IMAGES_UNKNOWN + "/" + images)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([keyvalues1[filename]], unknown_encoding, tolerance= 0.5)
            if results[0]:
                res = str(filename).split('.')
                attendance_list.append(res[0])
                # print(filename + ' ' + images)
    
    # print(attendance_list)
    return (attendance_list)
        

