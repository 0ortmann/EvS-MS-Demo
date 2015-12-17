#!/usr/bin/python

from flask import Flask, request, json, Response
from bildverarbeitung import *
from requests import post as send
from werkzeug import secure_filename

'''
Simple Flask-API for serving requests. API offers stuff for basic image processing.
'''

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extractImage(request):
    ''' Returns a file, if contained in the given request '''
    #print(request.files)
    #print(request.files['file'])
    file = request.files['file']
    filename = secure_filename(file.filename)
    #print(filename)
    return filename, file

def process(image, operation):
    ''' Process the given image with the given operation if possible. Unknown operation result in "None"-return. '''
    if (operation == 'roberts_cross'):
        return image.roberts_cross()
    elif (operation == 'sobel'):
        return image.sobel()
    elif (operation == 'scharr'):
        return image.scharr()
    elif (operation == 'prewitt'):
        return image.prewitt()
    #elif (operation == 'kirsch'):  // kirsch und laplace sind scheiße
    #    return image.kirsch()
    #elif (operation == 'laplacian'):
    #    return image.laplacian()
    else: return None

def sendToStorage(imagename, operation):
    ''' looks up the images by name and sends them to the persistency layer '''
    #print(imagename)
    name, format = imagename.split('.')


    images = [(operation + '_combined', open('img/' + operation + '_combined.' + format, 'rb')),
            (operation + '_directions', open('img/' + operation + '_directions.' + format, 'rb')),
            (operation + '_imag', open('img/' + operation + '_imag.' + format, 'rb')),
            (operation + '_magnitudes', open('img/' + operation + '_magnitudes.' + format, 'rb')),
            (operation + '_real', open('img/' + operation + '_real.' + format, 'rb')), 
            ('orig_file', open(imagename, 'rb'))]
    send('http://localhost:1337/images', files=images, data={'operator': operation, 'name': imagename})
    
@app.route('/process/<operation>', methods=['POST'])
def acceptImage(operation):
    ''' Basic image processing on the posted image '''
    name, posted = extractImage(request)
    image = Image.from_file(posted)
    process(image, operation) # stores everything in img/ folder
    sendToStorage(name, operation)
    return Response("Success", 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)