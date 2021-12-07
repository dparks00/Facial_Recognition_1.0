

import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.io


""" Create display of 36 people """
"""
This snippet of code (lines 17 to 39) was taken from Chapter 1 of:
'Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control'
by Brunton and Kutz

Will only work using allFaces.mat
"""
plt.rcParams['figure.figsize']=[5,5]
plt.rcParams.update({'font.size':18})

'''
mat_contents = scipy.io.loadmat(os.path.join('..', 'data', 'allFaces.mat'))
faces = mat_contents['faces']
m = int(mat_contents['m'])
n = int(mat_contents['n'])
nfaces = np.ndarray.flatten(mat_contents['nfaces'])

allPersons = np.zeros((n*6, m*6))
count = 0
for j in range(6):
    for k in range(6):
        allPersons[j*n : (j+1)*n, k*m : (k+1)*m] = np.reshape(faces[:,np.sum(nfaces[:count])], (m,n)).T
        count += 1


img = plt.imshow(allPersons)
img.set_cmap('gray')
plt.axis('off')
#plt.show()
'''
""" end """

mat_contents = scipy.io.loadmat(os.path.join('..','data','allFaces.mat'))
faces = mat_contents['faces']
m = int(mat_contents['m'])
n = int(mat_contents['n'])


""" Conduct PCA  """
def main():
    avgFace = np.mean(faces, axis=1)

    X = faces - np.tile(avgFace, (faces.shape[1],1)).T
    U, S, VT = np.linalg.svd(X, full_matrices=0)

    r = 800

    d = plt.imshow(np.reshape(avgFace, (m,n)).T)
    d.set_cmap('gray')
    plt.axis('off')
    plt.show()

    Ur = U[:, :r]
    print(np.shape(avgFace))
    np.save("U.npy", U)
    np.save("Ur.npy", Ur)
    np.save("avgFace.npy", avgFace)

if __name__ == "__main__":
    main()
