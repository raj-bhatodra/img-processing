from flask import Flask, request, render_template
import cv2 as cv
import numpy as np
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)
s3 = boto3.client('s3', aws_access_key_id='AKIAYGU4YK33OKDIIKPI',
                  aws_secret_access_key='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')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['image']
    img = cv.imdecode(np.frombuffer(file.read(), np.uint8), cv.IMREAD_COLOR)
    resized = rescaleframe(img)
    cv.imwrite('static/resized_image.jpg', resized)

    # Upload resized image to S3 bucket
    try:
        s3.upload_file('static/resized_image.jpg',
                       'raj-tf-bucket-project', 'resized_image.jpg')
    except NoCredentialsError:
        return 'AWS credentials not available'

    return render_template('index.html', image='static/resized_image.jpg')


def rescaleframe(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimension = (width, height)

    return cv.resize(frame, dimension, interpolation=cv.INTER_AREA)


if __name__ == '__main__':
    app.run(debug=True)
