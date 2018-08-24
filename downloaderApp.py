from celery import Celery
import urllib.request
import os

# Where the downloaded files will be stored
BASEDIR="/home/celery/downloadedFiles"

# Create the app and set the broker location (RabbitMQ)
app = Celery('downloaderApp',
             backend='rpc://',
             broker='pyamqp://guest@localhost//')

@app.task
def download(url, filename):
    """
    Download a page and save it to the BASEDIR directory
      url: the url to download
      filename: the filename used to save the url in BASEDIR
    """
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(BASEDIR+"/"+filename,'wb') as file:
        file.write(data)
    file.close()

@app.task
def list():
    """ Return an array of all downloaded files """
    return os.listdir(BASEDIR)

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results