import subprocess
import appcongif


def match(unknown_images):
    attendance_list = []
    for images in unknown_images:
        p = subprocess.run('face_recognition --tolerance 0.5 --cpus 8 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, capture_output = True)
<<<<<<< HEAD
        print (p.stdout)
=======
        s = p.stdout
        res = str(s).split(',')
        res[1] = str(res[1]).replace('\\r\\n\'' ,'')
        attendance_list.append(res[1])
    return (attendance_list)



>>>>>>> 9681ad82017f29e562d3bd0b5a291fd1171404cd
