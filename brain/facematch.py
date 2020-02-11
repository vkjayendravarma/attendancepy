import subprocess
import appcongif

def match(unknown_images):
    for images in unknown_images:
        p = subprocess.run('face_recognition --tolerance 0.5 --cpus 8 ' + appcongif.IMAGES_KNOWN + " " + appcongif.IMAGES_UNKNOWN + "/" + images ,shell = True, capture_output = True)
        print (p.stdout)



