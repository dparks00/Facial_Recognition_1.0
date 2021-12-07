import matplotlib.pyplot as plt
import os
import scipy.io
import cv2
import isDuke
import numpy as np
import io
import sys
from contextlib import contextmanager


@contextmanager
def nostdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def compare(value, filename, less, greater, image=None):
    counter = 0
    if less < greater:
        counter+=1
        if image is not None:
            img = cv2.imread(image,cv2.IMREAD_GRAYSCALE)
            cv2.imshow(filename,img)
            cv2.waitKey(100)
        print(filename+':', value)
    return counter



#if value < max, it will display the image and return 1
#else returns 0
def checkNotDuke(value, max, filename, image=None):
    return compare(value=value, image=image, filename=filename, less=value, greater=max)

#if min < value, it will display the image and return 1
#else returns 0
def checkDuke(value, min, filename, image=None):
    return compare(value=value, image=image, filename=filename, less=min, greater=value)


plt.rcParams['figure.figsize']=[8,8]
plt.rcParams.update({'font.size':18})

notDuke = os.path.join('.','images','notDuke')
duke = os.path.join('.','images','duke')
rob = os.path.join('.','images','RobPat')

notDukeMape = []
dukeMape = []
robMape = []
dukeDist = []
notDist = []
robDist = []
mistakedForDuke = 0
dukeMistaked = 0
robMistaked = 0
d_count = 0
notD_count = 0
rob_count = 0

for filename in os.listdir(notDuke):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        notD_count+=1
    else:
        continue
    image = os.path.join(notDuke, filename)
    with nostdout():
        mape, eucDist = isDuke.main(pic=image)
    notDukeMape.append(mape)
    notDist.append(eucDist)
    #checkNotDuke(value=mape, filename=filename, max=2)
    mistakedForDuke += checkNotDuke(value=eucDist, filename=filename,max=6000)

for filename in os.listdir(rob):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        rob_count+=1
    else:
        continue
    image = os.path.join(rob, filename)
    with nostdout():
        mape, eucDist = isDuke.main(pic=image)
    robDist.append(eucDist)
    robMape.append(mape)
    #checkNotDuke(value=mape, filename=filename, max=2)
    robMistaked += checkNotDuke(value=eucDist, filename=filename,max=6000)

for filename in os.listdir(duke):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        d_count +=1
    else:
        continue
    image = os.path.join(duke, filename)
    with nostdout():
        mape, eucDist = isDuke.main(pic=image)
    dukeMape.append(mape)
    dukeDist.append(eucDist)
    #checkDuke(value=mape, filename=filename, min=2)
    dukeMistaked += checkDuke(value=eucDist, filename=filename,min=6000)


plt.show(block=False)
plt.close('all')

#Graph MAPE
plt.axvline(x=2, ymin=0, ymax=1, color="black", linestyle="--")
plt.axvline(x=3, ymin=0, ymax=1, color="red", linestyle='--')
plt.axvline(x=4, ymin=0, ymax=1, color="blue", linestyle='--')
plt.scatter(notDukeMape, np.zeros_like(notDukeMape) + 0.1, label='Not Duke')
plt.scatter(dukeMape, np.zeros_like(dukeMape), label='Duke')
plt.scatter(robMape, np.zeros_like(robMape)-0.1, label='Robert Pattinson')
plt.legend()
plt.ylim((-0.2,0.2))
plt.xlabel('Mean Absolute Percent Error (MAPE)')
plt.yticks([])
plt.show(block=True)

#Graph Euclidean Distances
plt.axvline(x=6000, ymin=0,ymax=1, color='red', linestyle='--')
plt.axvline(x=8000, ymin=0,ymax=1, color='blue', linestyle='--')
plt.scatter(notDist, np.zeros_like(notDukeMape) + 0.1, label='Not Duke')
plt.scatter(dukeDist, np.zeros_like(dukeMape), label='Duke')
plt.scatter(robDist, np.zeros_like(robMape)-0.1, label='Robert Pattinson')
plt.legend()
plt.ylim((-0.2,0.2))
plt.xlabel('Euclidean Distance')
plt.yticks([])
plt.show(block=True)



failRateMsg ="You mistook {} of {}  people for Duke, and {} of {} Dukes for not Duke"
print(failRateMsg.format(mistakedForDuke, notD_count, dukeMistaked, d_count))

print("{} of {} images of RobP mistook for Duke.".format(robMistaked, rob_count))
plt.show(block=True)






