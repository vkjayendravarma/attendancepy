import subprocess
import appcongif


def match(unknown_images):
    attendance_list = []
    for images in unknown_images:
    #     p = subprocess.run('face_recognition --tolerance 0.5 --cpus 8 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, capture_output = True)
    #     s = p.stdout
    #     res = str(s).split(',')
    #     res[1] = str(res[1]).replace('\\r\\n\'' ,'')
    #     attendance_list.append(res[1])
    # return (attendance_list)
        data = subprocess.Popen('face_recognition --tolerance 0.5 --cpus 8 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, stdout = subprocess.PIPE)
        output = data.communicate()
        res = str(output).split(',')
        res[1] = str(res[1]).replace('\\n\'' ,'')
        attendance_list.append(res[1])
    print(attendance_list)  
    return (attendance_list)

