#imports to handle local files 
import os, errno

#imports to handle server 
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

#import database  config
import firebase
from datetime import date, datetime
import pytz

# Local imports
import appcongif
import brain




#init flask
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})


# init DB 
database = firebase.firebase.database()


# APP configs
app.config["IMAGES_TO_IDENTIFY"] = appcongif.IMAGES_TO_IDENTIFY
app.config["IMAGES_KNOWN"] = appcongif.IMAGES_KNOWN
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
        
        print(images_input)
            
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
    dateToPost = data["date"]
    sessionToPost = data["session"]
    
    identified = brain.pull(imageList) 
    
    dbRef = database.child(dateToPost)
    if(dbRef.child(sessionToPost).get().val()):
        print("yes")
    
      
    # database.child(date.today()).child(current_time).set(identified["identified"])

    print(identified["unidentified"])
    
    return identified


@app.route("/unidentified")
def unidentified():
    intruder = os.listdir(app.root_path +"/"+ appcongif.IMAGES_UNIDENTIFIED)    
    
    return {"intruders" : intruder}




# Web admin related routs 


# generate new profile
@app.route("/newuser", methods=["POST"])
def newuser():
    err = None
    userID = request.form["userId"]
    userName = request.form["userName"]
    # userImg = request.files["userImg"]
    
    
    # Changing file names
    # f_name, f_ext  = os.path.splitext(userImg.filename) 
    # f_name = userID           
    # filename = f_name + f_ext
        
    # Save images to local directory
    # newPath = app.root_path + "/" + app.config["IMAGES_KNOWN"] + "/" + filename
    # if(os.path.exists(newPath)):
    #     print("yes")
    # userImg.save(os.path.join())
    # print(request)
    
    
    # return {"res": filename, "err": err}
    print(userID +" "+ userName)
    return {
        "resp" : "yes"
    }


# Server options 
if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)