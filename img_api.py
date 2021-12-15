from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import cv2
import numpy as np
import io
import base64
import os
import json
from PIL import Image, ImageOps
from process_image import listforindex, deletefiles, enh_contrast

app=Flask(__name__)
app.secret_key = "adina"
api = Api(app)


UPLOAD_FOLDER="/Users/adinaciubancan/Documents/How to API/IMAGE PROCESSING API"
SAVED_FOLDER="/Users/adinaciubancan/Documents/How to API/IMAGE PROCESSING API/Revert"



app=Flask(__name__)
app.secret_key = "adina"
api = Api(app)

updates=[]

hit_apply=0
hit_apply+=1



class ProcessImage(Resource):
  
    def post(self, name):
        if 'imageFile' in request.files:
            file = request.files['imageFile']
            name = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, name))
            return "File Uploaded Successfully"
        else:
            return "File Failed"

    def get(self,name):
        width, height = Image.open(name).size
        response = jsonify(width=width, height=height)
        r=jsonify(w=width , h=height)
        updates.append(r)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


    def delete(self, name):
        global updates
        updates = list(filter(lambda x: x['name'] != name, updates))
        return {'message': 'Reverted to previous state'}

class UpdatesList(Resource):
    def get(self):
        return {'changes': updates}

class ImageOp(Resource):
    def get(self, name, operation):
        image=Image.open(name)
        if operation == 'contrast':
            final=enh_contrast(image,5)
        elif operation=='bw':
            final=ImageOps.grayscale(image)
        else:
            pass
        mylist=listforindex()
        final.save(f"{SAVED_FOLDER}/imgstate_{mylist[-1]}.jpg","JPEG")
        if len(mylist)==3:
            print("they should be deleted now")
            deletefiles(SAVED_FOLDER, mylist[0]-1)
        return 'Changes saved'
    


api.add_resource(ProcessImage, '/file/<string:name>')
api.add_resource(UpdatesList, '/file/seeupdates')
api.add_resource(ImageOp, '/file/edit/<string:name>/<string:operation>')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(port=5000)
    