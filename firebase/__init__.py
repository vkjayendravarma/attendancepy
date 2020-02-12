import pyrebase



# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("key.json")
# firebase_admin.initialize_app(cred)


config = {
  "apiKey": "AIzaSyACZ2HPtH6h_2zjBrttHLM9LI-oKqk94X8",
  "authDomain": "attendancex.firebaseapp.com",
  "databaseURL": "https://attendancex.firebaseio.com",
  "projectId": "attendancex",
  "storageBucket": "attendancex.appspot.com",
  "messagingSenderId": "612004485766",
  "appId": "1:612004485766:web:d4cc12a5a6b06a9f374f07",
  "measurementId": "G-P98R0K1M5N"
}



  
  
firebase = pyrebase.initialize_app(config)
