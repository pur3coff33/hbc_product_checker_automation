from operator import eq
import pandas as pd

import requests
from PIL import Image
from io import BytesIO
import numpy as np

import sys

import csv

def load_image_bytes(url):
    headers = {
    'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    return requests.get(url, headers=headers).content


def content_to_ndarray(im_bytes):
    bytes_io = bytearray(im_bytes)
    img = Image.open(BytesIO(bytes_io))
    return np.array(img)


def load_image_from_url(url):
    return content_to_ndarray(load_image_bytes(url))

def checkIMG(img_input, images):
    for img in images:
        if np.array_equal(img_input,img):
            return True
    return False
   


### MAIN



#read hbc product catalog
products = pd.read_csv('hbc.csv', delimiter=';')
products_with_no_photo = []

urls = ['http://hallbrookcomponents.com/img/p/0.jpg',
    'http://hallbrookcomponents.com/img/p/4/8/1/3/4813.jpg',
    'http://hallbrookcomponents.com/img/p/1/5/9/3/5/15935.jpg',
    'http://hallbrookcomponents.com/img/p/9/9/1/3/9913.jpg',
    'http://hallbrookcomponents.com/img/p/1/0/1/3/5/10135.jpg']

images = []

for url in urls:
    images.append(load_image_from_url(url))


index = 0
startIndex = 0
countWithImg = 0
countWithoutImg = 0
countWithError = 0
for url in products['Image']:

    fileName = 'with_image.csv'

    try:

        if index <= startIndex:
            print('SKipping ', url, ' at index ', index)
            index += 1
            continue

        print("#################")
        print("#### INDEX " , index , " ########")

        img = load_image_from_url(url)
        data = [products['id'][index],products['Image'][index], products['Name'][index], products['Reference'][index], products['Category'][index],
            products['Base price'][index], products['Final price'][index],products['Quantity'][index],products['Status'][index]]


        print('CHECKING ', url, end='')
        countWithImg += 1

        if checkIMG(img, images):
            print(' --- no photo detected ...',end='')
            fileName = "no_image.csv"
            countWithImg -= 1
            countWithoutImg += 1
            
        with open(fileName, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(data)
    
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        fileName = 'with_error.csv'
        with open(fileName, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
        countWithError += 1
       
    index += 1
    print()



#print(products_with_no_photo)
print('DONE----------')


