#!/usr/bin/python

from flask import Flask, request, json, Response
from bildverarbeitung import *

'''
Simple Flask-API for serving requests. API offers stuff for basic image processing.
'''

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extractImage(request):
    #print(request.files)
    #print(request.files['file'])
    return request.files['file']


def process(image, operation):
    if (operation == 'roberts_cross'):
        return image.roberts_cross()
    elif (operation == 'sobel'):
        return image.sobel()
    elif (operation == 'scharr'):
        return image.scharr()
    elif (operation == 'prewitt'):
        return image.prewitt()
    elif (operation == 'kirsch'):
        return image.kirsch()
    elif (operation == 'laplacian'):
        return image.laplacian()
    else: return None




@app.route('/process/<operation>', methods=['POST'])
def acceptImage(operation):
    ''' Basic image processing on the posted image '''
    posted = extractImage(request)
    print(operation)
    image = Image.from_file(posted)
    process(image, operation)
    
    return Response("Hooray", 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)