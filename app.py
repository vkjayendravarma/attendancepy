#imports to handle local files 
import os, errno

#imports to handle server 
from flask import Flask, request, render_template

#import database  config
import firebase
from datetime import date, datetime
import pytz

# Local imports
import appcongif
import brain




#init flask
app = Flask(__name__)


# APP configs
app.config["IMAGES_TO_IDENTIFY"] = appcongif.IMAGES_TO_IDENTIFY
app.config["IMAGE_ID"] = appcongif.IMAGE_ID

# Directory setup
storage_location = app.root_path + "/" + app.config["IMAGES_TO_IDENTIFY"] 

location = app.root_path + "/" + appcongif.IMAGES_UNKNOWN
location1 = app.root_path + "/" + appcongif.IMAGES_UNIDENTIFIED

try:
    os.makedirs(storage_location)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.makedirs(location)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.makedirs(location1)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Index route
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle image uploads
@app.route("/uploadimage", methods=["POST"])
def uploadimage():
    
    if request.files :            
        images_input = request.files["images"] 
            
        # Changing file names
        app.config["IMAGE_ID"] = app.config["IMAGE_ID"] + 1
        f_name, f_ext  = os.path.splitext(images_input.filename) 
        f_name = str(app.config["IMAGE_ID"])            
        filename = f_name + f_ext
            
        #Save images to local directory
        images_input.save(os.path.join(app.root_path, app.config["IMAGES_TO_IDENTIFY"], filename))
            
        print("Image saved" + filename)
            
    
    return {"filename": filename}  #return filename as response 
    
    
@app.route("/process_images", methods=["POST"])
def process_images():
    data = request.get_json()
    
    imageList = data["img"]
    
    identified = brain.pull(imageList) 
    
    now = datetime.now()
    
    tz = pytz.timezone('Asia/Kolkata')
    current_time = now.astimezone(tz).strftime("%H:%M:%S")
    
    db = firebase.firebase.database()
    db.child(date.today()).child(current_time).set(identified["identified"])

    print(identified["unidentified"])
    
    return identified


@app.route("/unidentified")
def unidentified():
    intruder = os.listdir(app.root_path +"/"+ appcongif.IMAGES_UNIDENTIFIED)    
    
    return {"intruders" : intruder}

# Server options 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)