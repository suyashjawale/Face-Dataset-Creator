import cv2
import requests
import face_recognition
from google.colab.patches import cv2_imshow
import json
import time
from unidecode import unidecode
import base64

f=open("/content/sample_data/allimageurls.json") #path to file
data=f.read()
f.close()
data=json.loads(data)

j=0
newdict=dict()
for key,value in data.items():
  try:
    j+=1
    time.sleep(2)
    try:
      if "base64" in value:
        z = value[value.find(","):]
        with open("elon3.png", "wb") as fh:
          fh.write(base64.b64decode(z))
      else:
        res=requests.get(value)
        with open("elon3.jpg", "wb") as f:
          f.write(res.content)
    except Exception as e:
      print("")
    
    imgElon = face_recognition.load_image_file('elon3.jpg')
    imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
    faceLoc = face_recognition.face_locations(imgElon)
    if len(faceLoc)==1:
      newdict[j]=value

  	'''IF you want to know what's happening you can...uncomment this'''
    # for (x, y, w, h) in faceLoc:
    #     print(x,y,w,h)
    #     cv2.rectangle(imgElon, (h, x), (y,w), (0,255,0), 2)
    # cv2_imshow(imgElon)
    
  except:
    pass

datas= json.dumps(newdict, indent = 4)
with open("urls.json", "w") as outfile:
    outfile.write(datas)
