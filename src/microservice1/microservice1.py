#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, json, Response
from bildverarbeitung import *
from requests import post as send
from werkzeug import secure_filename

'''
Simple Flask-API for serving requests. API offers stuff for basic image processing.
'''

UPLOAD_FOLDER = './uploads'
DB_SERVER = 'localhost'
#DB_SERVER = 'ms2'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extractImage(request):
    """
    Returns a file, if contained in the given request
    """
    #print(request.files)
    #print(request.files['file'])
    file = request.files['file']
    filename = secure_filename(file.filename)
    #print(filename)
    return filename, file


def process(image, operation):
    """
    Process the given image with the given operation if possible. Unknown operation result in "None"-return.
    """
    if (operation == 'roberts_cross'):
        print("Apply Robert's Cross … "),
        return image.roberts_cross()
    elif (operation == 'sobel'):
        print("Apply Sobel … "),
        return image.sobel()
    elif (operation == 'scharr'):
        print("Apply Scharr … "),
        return image.scharr()
    elif (operation == 'prewitt'):
        print("Apply Prewitt … "),
        return image.prewitt()
    #elif (operation == 'kirsch'):  // kirsch und laplace sind scheiße
    #    return image.kirsch()
    #elif (operation == 'laplacian'):
    #    return image.laplacian()
    else: return None


def sendToStorage(image_name, operation):
    """
    :param str image_name: Name of the image which will be sent.
    :param operation: The applied operation.
    """

    ''' looks up the images by name and sends them to the persistency layer '''
    rindex = image_name.rindex('.')
    name = image_name[:rindex]
    format = image_name[rindex + 1:]
    print(image_name)
    print(name)
    print(format)

    images = [('combined', ('combined.png', open('img/' + operation + '_combined.png', 'rb'), 'image/png')),
              ('directions', ('directions.png', open('img/' + operation + '_directions.png', 'rb'), 'image/png')),
              ('imag', ('imag.png', open('img/' + operation + '_imag.png', 'rb'), 'image/png')),
              ('magnitudes', ('magnitudes.png', open('img/' + operation + '_magnitudes.png', 'rb'), 'image/png')),
              ('real', ('real.png', open('img/' + operation + '_real.png', 'rb'), 'image/png')),
              ('original_image', ('original_image', open("img/original.png", 'rb'), 'image/png'))]
    send('http://' + DB_SERVER + ':1339/images', files=images, data={'operator': operation, 'name': image_name})
    
@app.route('/process/<operation>', methods=['POST'])
def acceptImage(operation):
    ''' Basic image processing on the posted image '''
    name, posted = extractImage(request)
    image = Image.from_file(posted)
    image.save("img/original.png")
    process(image, operation) # stores everything in img/ folder
    sendToStorage(name, operation)
    return Response("Success", 200, headers={'Access-Control-Allow-Origin': '*'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1338)
