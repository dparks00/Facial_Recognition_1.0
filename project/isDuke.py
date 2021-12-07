
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io

def main(pic=None):
    m = 168
    n = 192

    plt.rcParams['figure.figsize']=[8,8]
    plt.rcParams.update({'font.size':18})

    Ur = np.load('Ur.npy')
    avgFace = np.load('avgFace.npy')
    #avgFace originally (n*m,)
    avgFace = np.reshape(avgFace, (n*m,1))

    avgMat = os.path.join('.','dukeAvg.mat')
    dukeAvg = scipy.io.loadmat(avgMat)
    d_sum = dukeAvg['Sum']
    d_count = dukeAvg['count']
    d_avg = d_sum / d_count
    x = dukeAvg['x']
    #x = np.reshape(d_avg, (m*n,1),'F')


    #alpha_duke is the projection of dukeX onto Ur
    #alpha_duke is like duke's fingerprint
    alpha_duke = Ur.T @ (x-avgFace)
    fileFound = False
    while not fileFound:
        if(pic==None):
            print('What file would you like me to view?')
            file = input()
        else:
            file = pic
            pic = None
        inImages = './images/'+file
        if os.path.isfile(inImages):
            fileFound = True
            file = inImages
        if os.path.isfile(file):
            fileFound = True
        if not fileFound:
            print('Sorry, that doesn\'t exist.  Try again')
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    #cv2.imshow(file,img)
    cv2.waitKey(1)
    img = cv2.resize(img, (m,n))
    npImg = img
    '''
    cv2.imshow(file, img)

    cv2.waitKey(1)

    cv2.destroyAllWindows()
    '''
    img_vector = np.reshape(img, (m*n, 1), 'F')
    #d = plt.imshow(np.reshape(img_vector,(n,m)))


    alpha_image = np.matmul(Ur.T, img_vector-avgFace)

    about_x = avgFace + np.matmul(Ur, alpha_duke)
    about_img = avgFace + np.matmul(Ur, alpha_image)
    #print('about x shape', np.shape(about_x))
    #print('avgFace', np.shape(avgFace))
    #print('about img shape', np.shape(about_img))

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(141)
    avg = ax1.imshow(np.reshape(about_img, (m,n)).T)
    avg.set_cmap('gray')
    ax1.set_title('Approximation of\n input image', fontsize=10)
    plt.axis('off')

    ax2 = fig1.add_subplot(142)
    img = ax2.imshow(np.reshape(img_vector, (m,n)).T)
    img.set_cmap('gray')
    ax2.set_title('Input image',fontsize=10)
    plt.axis('off')

    ax3 = fig1.add_subplot(143)
    myAvg = ax3.imshow(np.reshape(x, (m,n)).T)
    myAvg.set_cmap('gray')
    ax3.set_title('Average Face\n of Duke', fontsize=10)
    plt.axis('off')

    ax4 = fig1.add_subplot(144)
    aboutAvg = ax4.imshow(np.reshape(about_x,(m,n)).T)
    aboutAvg.set_cmap('gray')
    ax4.set_title('Approximation of\n Average Face\n of Duke', fontsize=10)
    plt.axis('off')

    #plt.show()

    MAPE = getMAPE(alpha_image, alpha_duke)


    concludeFromMAPE(MAPE)
    

    #find euclidean distance
    dist = np.sqrt(np.sum(np.square(alpha_image[4:]-alpha_duke[4:])))
    print('Euclidean Distance:', dist)
    
    concludeFromEucDist(dist)

    #plt.show()
    
    return MAPE, dist

def concludeFromMAPE(MAPE):
    conclusion ='Based on MAPE, '
    if abs(MAPE) < 2:
        conclusion += 'I think this is Duke.'
    elif abs(MAPE) < 3:
        conclusion += 'I don\'t think this is Duke, but I\'m not certain.'
    else:
        conclusion +='this isn\'t Duke.'
    print(conclusion)

def concludeFromEucDist(dist):
    conclusion = 'Based on euclidean distance, '
    if dist < 6000:
        conclusion += 'I think this is Duke.'
    elif dist < 8000:
        conclusion+='I don\'t think this is Duke, I\'m not certain.'
    else:
        conclusion +='this isn\'t Duke.'
    print(conclusion)


def getMAPE(alpha_image, alpha_duke):
    MAPE = 0
    count = 0 
    #Results from trial-and-error:
    #Best to ID Duke as Duke: 5,11
    #Best to ID notDuke as notDuke: 6,30 with MAPE < 3 to ID Duke
    #Best overall: 7,13
    for i in range(7, 13):
        ai = alpha_image[i]
        ad = alpha_duke[i]
        MAPE += abs((ai-ad)/ad)
        count += 1
    MAPE = MAPE / count
    print('MAPE:', MAPE[0])
    return MAPE[0]

if __name__ =='__main__':
    main()

