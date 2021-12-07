# Facial_Recognition_1.0
## Introduction:
Hello! Welcome to my first personal project that I will posting on GitHub! 

## Description:
A personal project that uses Principal Component Analysis (PCA) and Eigenfaces to identify whether or not a face belongs to Duke Parks (me).

## Walkthrough:

First, start in **precomp.py**.  In this script, we will perform principal component analysis on a the matrix **allFaces.mat** by computing the SVD on the mean-centered matrix of **allFaces.mat** and save the unitary matrix and its rank-800 approximation.

**allFaces.mat** is matrix where every column is the image data of a grayscaled face taken from *Yale Face Database B*. 

Next, we move on to **dukeAvg.m**.  In this script, we iterate through the images stored in ./data/duke which a series of cropped images of my face. In **dukeAvg.m**, we convert these images to grayscale, resize them to match the images from the *Yale Face Database B*, find the average of the image matrices, and reshape the average image matrix into a vector.

Now, in **isDuke.py**, we will take the average image vector found in **dukeAvg.m**, mean-center it, project it on the rank approximation of the unitary matrix found in **precomp.py**, and this gives us what we'll call *alpha*.  *alpha* can be thought of as the fingerprint of a face/image, in this case, my face. Faces that are like mine will have similiar *alphas*, so we can use *alpha* to distinguish other people from me.  Additionally, if we multiply *alpha* by the rank approximation of the unitary matrix from **precomp.py** and add back the average face, we will get an approximation of my average face.
>And we can do this for any *alpha* of any image using to same rank-approximated unitary matrix and average face matrix to produce the original image that was used to find *alpha* (we can also tweak our math to exclude the average face matrix).  This is a method of image compression since *alpha* is a lot smaller than the matrix used to make *alpha*, but perhaps more on that in another project.



## Results:


## Credit and Thanks:
While I developed this program independently, I would like to first thank the 'Yale Face Database' and 'Yale Face Database B'.  The images in these databases are what enabled to me create the Eigenfaces that my program relies on.  Additionally, I learned PCA in part from 'Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control' by Dr. Brunton and Dr. Kutz.  This book also very conviently provided me with a matrix of data computed from the 'Yale Face Database B' which I used in my program.  This matrix can be found in 'allFaces.mat' in the Data folder.
