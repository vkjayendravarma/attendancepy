import subprocess

def match():
    p = subprocess.run('face_recognition --tolerance 0.5 --cpus 8 known unknown ',shell = True, capture_output = True)
    print (p.stdout)



