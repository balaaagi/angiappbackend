# Angi App Backend

Flask based backend API services used for Face Detection

### API END Points
| End Point | Params | Type | Remarks |
| ------ | ------ | ------ | ------ | 
| /verifyalltrainingset |  | GET | Verify All training data Set Images from REST API provided |
|/verify | Image Url To Authenticate | GET | Verify if the passed image url is valid person from the training set
| /verifyfrommobile | Image URL of the captured image from Mobile App | GET | Verify if the image requested from image is authenticated or not |

![Screen Shots](Resources/Backend.JPG?raw=true )

## Steps to Execute
``` sh
$ clone the repo
$ cd to project folder
$ clone https://github.com/ffmmjj/kairos-face-sdk-python.git 
$ virtualenv flask
$ flask/bin/pip install flask
$ cd kairos-face-sdk-python
$ complete path of <flask/bin/pip> install .
$ chmod a+x anginbackendapp.py
$ ./anginbackendapp.py

```

* Please create Kairos API Keys
* Rename dummysetting.py settings.py
* Fill in with neccessary details of API

