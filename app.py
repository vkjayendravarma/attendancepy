#imports to handle local files 
import os, errno
import shutil

#imports to handle server 
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

#import database  config
import firebase
from datetime import date, datetime
import pytz

# Local imports
import appconfig
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
db = firebase.firebase.database()


# APP configs
app.config["IMAGES_TO_IDENTIFY"] = appconfig.IMAGES_TO_IDENTIFY
app.config["IMAGES_KNOWN"] = appconfig.IMAGES_KNOWN
app.config["IMAGE_ID"] = appconfig.IMAGE_ID

# Directory setup
storage_location = app.root_path + "/" + app.config["IMAGES_TO_IDENTIFY"] 

location = app.root_path + "/" + appconfig.IMAGES_UNKNOWN
location1 = app.root_path + "/" + appconfig.IMAGES_UNIDENTIFIED
location2 = app.root_path + "/" + appconfig.IMAGE_ENCODINGS

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
try:
    os.makedirs(location2)
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
    
# generate encodings

@app.route("/encodings", methods=["GET"])
def encodings():
    print("enc")
    brain.know_face_encodings.en()
    
    return {"res": "Encodings generated"}

# process and posting attendance
  
@app.route("/process_images", methods=["POST"])
def process_images():
    data = request.get_json()
    
    imageList = data["img"]
    dateToPost = data["date"]
    sessionToPost = data["session"]
    
    
   # Generate session if dosent exists
    if(db.child('attendance').child(dateToPost).child(sessionToPost).get().val() == None):
        userRef  = db.child('users').get()
        for user in userRef.each():
            print (user.key())
            db.child('attendance').child(dateToPost).child(sessionToPost).child(user.key()).set(0)
    identified = brain.pull(imageList) 
    # Set attendace for identified 
    for id in identified['identified']:
        db.child('attendance').child(dateToPost).child(sessionToPost).child(id).set(1)
    for id in identified["unidentified"]:
        db.child("unidentified").push({
            "date": dateToPost,
            "imgID": id,
            "session": sessionToPost
        })
       
    return identified


@app.route("/unidentified", methods=["GET", "POST"])
def unidentified():
    res=[]
    err=''
    intruderdb = db.child('unidentified').get()
    
    #get all unidentified people
    if( request.method == "GET"):
    
        if(intruderdb.val()):
            for record in intruderdb.each():
                data = record.val()
                setRecord = {
                    'id': record.key(),
                    'date': data['date'],
                    'session': data['session'],
                    'imgUrl': "http://localhost:8080/static/unidentified/" + data["imgID"] + ".jpeg"
                }
                res.append(setRecord)
        else:
            err = "No unidentified people" 
            
    # send data for updating unidentified person to known 
    if(request.method == "POST"):
        requestid = request.get_json()['id']
        print(requestid)
        data = db.child('unidentified').child(requestid).get().val()
        if(data):
            res = {
                'id': requestid,
                'date': data['date'],
                'session': data['session'],
                'imgID': data["imgID"],
                'imgUrl': "http://localhost:8080/static/unidentified/" + data["imgID"] + ".jpeg"
            }
        else:
            err = 'No data. Guest might be updated by someone'
    
    return {"res" : res,"err" : err}




# Web admin related routs 
   


# generate new profile
@app.route("/newuser", methods=["POST"])
def newuser():
    err = None
    res = None
    userID = request.form["userId"]
    userName = request.form["userName"]
    
    if(request.files): 
        # Changing file names
        userImg = request.files["userImg"] 
        f_name, f_ext  = os.path.splitext(userImg.filename) 
        f_name = userID           
        filename = f_name + f_ext        
        newPath = app.root_path + "/" + app.config["IMAGES_KNOWN"] + "/" + filename

        # Save images to local directory
        if(request.form["force_override"] == 'true'):        
            userImg.save(os.path.join(newPath))
            res = userID
            db.child("users").child(userID).set(userName)
        else:
            if(os.path.exists(newPath)):
                err = 'file exists'
            else:
                userImg.save(os.path.join(newPath))
                res = userID
                db.child("users").child(userID).set(userName)
    
    # If it is to update unidentified peson 
    elif (request.form["existingID"]):
        newfile = appconfig.IMAGES_KNOWN + "/" + str(userID) + ".jpeg"        
        guest = db.child("unidentified").child(request.form["existingID"]).get().val()
        
        if(request.form["force_override"] == 'true'):        
            shutil.move(appconfig.IMAGES_UNIDENTIFIED + "/" + str(guest["imgID"]) + ".jpeg" ,appconfig.IMAGES_KNOWN + "/" + str(userID) + ".jpeg")
            db.child("users").child(userID).set(userName)
            db.child('attendance').child(guest["date"]).child(guest["session"]).child(userID).set(1)        
            db.child("unidentified").child(request.form["existingID"]).remove()  
        else:
            if(os.path.exists(newfile)):
                err = 'file exists'
            else:
                shutil.move(appconfig.IMAGES_UNIDENTIFIED + "/" + str(guest["imgID"]) + ".jpeg" ,appconfig.IMAGES_KNOWN + "/" + str(userID) + ".jpeg")
                db.child("users").child(userID).set(userName)
                db.child('attendance').child(guest["date"]).child(guest["session"]).child(userID).set(1)        
                db.child("unidentified").child(request.form["existingID"]).remove()  
        
          
        res = userID
        print("Updating user")
    else:
        err: "No File choosen"
    
    return {"userId": res, "err": err}
    
# get selected date and session attendance 
@app.route("/getattendance", methods=['POST'])
def getAttendance():
    req = request.get_json()
    err = None
    date = req['date']
    session = req['session']
    
    attendace = []
    
    print(req)
    
    data = db.child('attendance').child(date).child(session).get()
    if(data.val()):
        for record in data.each():
            print(record.key() + ":" + str(record.val()))
            
            if(record.val()):
                PorA = 'Present'
            else: 
                PorA = 'Absent'
            
            ID = record.key()        
        
            setRecord = {
                'ID': ID,
                'name': db.child("users").child(ID).get().val(),
                'PorA': PorA            
            }
            attendace.append(setRecord)
    
    else:
        err = 'No data available'
        
    return {"res": attendace, 'err': err}

# Delete unidentified person
@app.route("/delete", methods=["POST"])
def delete():
    data = request.get_json()
    print(data)
    requestid = data["imgID"]
    dbr = db.child('unidentified').child(requestid).get().val()
    imref = dbr["imgID"]
    pathref = app.root_path + "/" + appconfig.IMAGES_UNIDENTIFIED + "/" + imref + ".jpeg"
    os.remove(pathref)
    db.child('unidentified').child(requestid).remove()  
    res = True             
    return {"res" : res}

# Server options 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)