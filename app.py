#imports to handle local files 
import os, errno

#imports to handle server 
from flask import Flask, request, render_template


#init flask
app = Flask(__name__)


# APP configs
app.config["IMAGES_TO_IDENTIFY"] = "static/processimages"
app.config["IMAGE_ID"] = 0

# Directory setup
storage_location = app.root_path + "/" + app.config["IMAGES_TO_IDENTIFY"] 
try:
    os.makedirs(storage_location)
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
    
    
# @app.route("process_images", methods=["POST"])
# def process_images():
#     return "hello"
    

# Server options 
if __name__ == "__main__":
    app.run(debug=True)