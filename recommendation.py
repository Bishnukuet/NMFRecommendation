from os.path import dirname, abspath
from os.path import join
from warnings import warn

import numpy as np

import nimfa
import pickle
import os
try:
    import matplotlib.pylab as plb
except ImportError as exc:
    warn("Matplotlib must be installed to run Recommendations example.")
'''

User Ui is interested in a item Vj and rated it with Rij stars
therefore, items with rating >= (Rij-th) will be feltched as recommendation.

THe questions that I am interested to answer are:
    1. Give me top 10 similar items to item j
    2. Give me top 10 similar users who bought this rated this item higher than threshold
    3. Give me top 10  similar item that is rated high by this user
    4. Give me users like the current user i


'''

#nimfa.examples.recommendations.run()
#nimfa.examples.documents.run()

#data_set='.//Datasets//Trainset//test.txt'
data_set='.//Datasets//Trainset//user_artist.dat'


def save_object(obj,filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','wb') as ObjFile:
        pickle.dump(obj,ObjFile,protocol=2)
def load_object(filename):
    path=os.curdir
    with open(path+'\\'+filename+'.pkl','rb') as ObjFile:
        return pickle.load(ObjFile)





def run():
    """
    Run SNMF/R on the MovieLens data set.

    Factorization is run on `ua.base`, `ua.test` and `ub.base`, `ub.test` data set. This is MovieLens's data set split
    of the data into training and test set. Both test data sets are disjoint and with exactly 10 ratings per user
    in the test set.
    """

    V = read(data_set)
    print V.shape
    print 'reading finished\n'
    W, H = factorize(V)
    save_object(W,'Results/artist_W')
    save_object(H,'Results/artist_H')
    print W.shape, H.shape



def factorize(V):
    """
    Perform SNMF/R factorization on the sparse MovieLens data matrix.

    Return basis and mixture matrices of the fitted factorization model.

    :param V: The MovieLens data matrix.
    :type V: `numpy.matrix`
    """
    snmf = nimfa.Snmf(V, seed="random_vcol", rank=30, max_iter=70, version='r', eta=1.,
                      beta=1e-4, i_conv=10, w_min_change=0)
    print("Algorithm: %s\nInitialization: %s\nRank: %d" % (snmf, snmf.seed, snmf.rank))
    fit = snmf()
    sparse_w, sparse_h = fit.fit.sparseness()
    print("""Stats:
            - iterations: %d
            - Euclidean distance: %5.3f
            - Sparseness basis: %5.3f, mixture: %5.3f""" % (fit.fit.n_iter,
                                                            fit.distance(metric='euclidean'),
                                                            sparse_w, sparse_h))
    #del sparse_h,sparse_w
    return fit.basis(), fit.coef()


def read(data_set):
    """
    Read movies' ratings data from MovieLens data set.

    :param data_set: Name of the split data set to be read.
    :type data_set: `str`
    """
    print("Read MovieLens data set")
    fname =data_set #'/Datasets/Trainset/%s.base'%data_set#join(dirname(dirname(abspath(__file__))), "datasets", "MovieLens", "%s.base" % data_set)
    #V = np.ones((15, 938)) * 2.5
    V=np.ones((17,704))*20
    for line in open(fname):
        u, i, r= list(map(int, line.split()))
        V[u - 1, i - 1] = r
        print 'Reading\n'

    return V


def rmse(W, H, data_set):
    """
    Compute the RMSE error rate on MovieLens data set.

    :param W: Basis matrix of the fitted factorization model.
    :type W: `numpy.matrix`
    :param H: Mixture matrix of the fitted factorization model.
    :type H: `numpy.matrix`
    :param data_set: Name of the split data set to be read.
    :type data_set: `str`
    """
    fname =  '/Datasets/Testset/%s.test'%data_set#join(dirname(dirname(abspath(__file__))), "datasets", "MovieLens", "%s.test" % data_set)
    rmse = []
    for line in open(fname):
        u, i, r, _ = list(map(int, line.split()))
        sc = max(min((W[u - 1, :] * H[:, i - 1])[0, 0], 5), 1)
        rmse.append((sc - r) ** 2)
    print("RMSE: %5.3f" % np.mean(rmse))


if __name__ == "__main__":
    """Run the Recommendations example."""
    run()