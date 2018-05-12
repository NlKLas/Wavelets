import PIL
import numpy as np
import matplotlib.pyplot as plt



def DecompositionStep(C):
    C_prime = np.empty_like(C)
    h = C.size
    for i in range(0,h//2):
        C_prime[i] = (C[2*i]+C[2*i+1])/(np.sqrt(2))
        C_prime[h//2+i] = (C[2*i]-C[2*i+1])/(np.sqrt(2))
    
    return C_prime

# C is assumed to be an array of coefficients corresponding to the normalized (!) basis
def Decomposition(C):
    C_prime = C.copy()
    h = C.size
    while h > 1:
        C_prime[0:h] = DecompositionStep(C_prime[0:h])
        h = h//2
    
    return C_prime


def SynthesisStep(C_prime):
    C = np.empty_like(C_prime)
    h = C_prime.size // 2
    for i in range(0, h):
        C[2*i] = (C_prime[i]+C_prime[h+i])/(np.sqrt(2))
        C[2*i+1] = (C_prime[i]-C_prime[h+i])/(np.sqrt(2))
    
    return C


def Synthesis(C_prime):
    C = C_prime.copy()
    h = 1
    while h < C_prime.size:
        h = 2*h
        C[0:h] = SynthesisStep(C[0:h])
    
    return C

'''
What follows are versions of the above functions optimized for use with images. It's a bit tedious, but I couldn't figure out a way to do this more efficiently. The main issue is that I want to vectorize the operations. Otherwise I could just use the functions above (I just don't like python loops...).
'''

def DecompositionStepX(C):
    h = C.shape[1]
    C_prime = np.empty_like(C)
    for i in range(0,h//2):
        C_prime[:,i] = (C[:,2*i]+C[:,2*i+1])/(np.sqrt(2))
        C_prime[:,h//2+i] = (C[:,2*i]-C[:,2*i+1])/(np.sqrt(2))
    return C_prime

def DecompositionX(C):
    h = C.shape[1]
    while h > 1:
        C[:,0:h] = DecompositionStepX(C[:,0:h])
        h = h//2
    return C

def DecompositionStepY(C):
    h = C.shape[0]
    C_prime = np.empty_like(C)
    for i in range(0,h//2):
        C_prime[i,:] = (C[2*i,:]+C[2*i+1,:])/(np.sqrt(2))
        C_prime[h//2+i,:] = (C[2*i,:]-C[2*i+1,:])/(np.sqrt(2))
    return C_prime

def DecompositionY(C):
    h = C.shape[0]
    while h > 1:
        C[0:h,:] = DecompositionStepY(C[0:h,:])
        h = h//2
    return C

def SynthesisStepX(C):
    h = C.shape[1] // 2
    C_prime = np.empty_like(C)
    for i in range(0, h):
        C_prime[:,2*i] = (C[:,i]+C[:,h+i])/np.sqrt(2)
        C_prime[:,2*i+1] = (C[:,i]-C[:,h+i])/np.sqrt(2)
    return C_prime

def SynthesisX(C):
    h = C.shape[1]
    i = 2
    while i <= h:
        C[:,0:i] = SynthesisStepX(C[:,0:i])
        i = 2*i
    return C

def SynthesisStepY(C):
    h = C.shape[0] // 2
    C_prime = np.empty_like(C)
    for i in range(0, h):
        C_prime[2*i,:] = (C[i,:]+C[h+i,:])/np.sqrt(2)
        C_prime[2*i+1,:] = (C[i,:]-C[h+i,:])/np.sqrt(2)
    return C_prime

def SynthesisY(C):
    h = C.shape[0]
    i = 2
    while i <= h:
        C[0:i,:] = SynthesisStepY(C[0:i,:])
        i = 2*i
    return C

def StandardDecomposition(img):
    C = img.copy()
    C = DecompositionX(C)
    C = DecompositionY(C)
    return C

def StandardSynthesis(C, copy=True):
    img = None
    if copy:
        img = C.copy()
    else:
        img = C
    
    img = SynthesisY(img)
    img = SynthesisX(img)
    return img
    

'''
I will assume a square image (if in doubt, add padding...)
'''
def NonstandardDecomposition(img):
    C = img.copy()
    
    h = C.shape[0]
    while h > 1:
        C[0:h,0:h] = DecompositionStepX(C[0:h,0:h])
        C[0:h,0:h] = DecompositionStepY(C[0:h,0:h])
        #plt.imshow(C, cmap='gray')
        #plt.show()
        h = h//2
    return C

def NonstandardSynthesis(C, copy=True):
    img = None
    if copy:
        img = C.copy()
    else:
        img = C
    
    h = 1
    while h < C.shape[0]:
        h = 2*h
        img[0:h,0:h] = SynthesisStepY(img[0:h,0:h])
        img[0:h,0:h] = SynthesisStepX(img[0:h,0:h])
        #plt.imshow(img, cmap='gray')
        #plt.show()
    return img



'''
Decompose an image (square format, width=height=2^k for some k) into its haar wavelet transform.
Also return an array of indices, which sorts the transform coefficients by value.

Args:
img: (2^k, 2^k) numpy array
nonstandard: boolean; if True nonstandard decomposition is used, standard otherwise; defaults to True

Returns:
(transform, sort_indices) -- sort indices is a tuple of two index arrays, one for each axis;
transform[sort_indices] would be sorted by absolute value ascendingly
'''
def decompose_sort(img, nonstandard=True):
    if nonstandard:
        transform = NonstandardDecomposition(img)
        
        sort_indices = np.unravel_index(np.argsort(np.abs(transform), axis=None),transform.shape)
        
        return (transform, sort_indices)
    
    else:
        transform = StandardDecomposition(img)
        
        sort_indices = np.unravel_index(np.argsort(np.abs(transform), axis=None),transform.shape)
        
        return (transform, sort_indices)

'''
Partially reconstruct an  image from its haar wavelet transform only using the num_coefficients
largest transform coefficients.

Args:
transform
sort_indices
num_coefficients: the number of coefficients to use for reconstruction
nonstandard: boolean; if True nonstandard decomposition is used, standard otherwise; defaults to True

Returns:
img -- a reconstruction of the original image
'''
def partially_reconstruct_img(transform, sort_indices, num_coefficients, nonstandard=True):
    img = transform.copy()
    
    num_discard = transform.size - num_coefficients
    img[(sort_indices[0])[:num_discard], (sort_indices[1])[:num_discard]] = 0
    
    
    if nonstandard:
        img = NonstandardSynthesis(img, copy=False)
    
    else:
        img = StandardSynthesis(img, copy=False)
    
    return img


'''
Compute the L2 distance of two vectors (images!) which are represented with respect to the same
orthonormal basis.
'''
def l2_distance(v, w):
    return np.linalg.norm(v-w, ord='fro')

def l2_norm(v):
    return np.linalg.norm(v, ord='fro')


'''
Computes the cumulative sum of squared coefficients, which is a measure for the l2_error 
introduced by leaving out the smallest coefficients.

Args:
transform
sort_indices

Returns:
cum_err2 -- cumulative squared error
'''
def cumulative_squared_error(transform, sort_indices):
    temp = transform*transform
    cum_err2 = np.empty(transform.size+1, dtype=float)
    cum_err2[0] = 0
    cum_err2[1:] = np.cumsum(temp[sort_indices])
    
    return cum_err2


'''
Given a maximum relative error, returns the number of coefficients to use to stay just below that
threshold.

Args:
cum_err2: see cumulative_squared_error
relative_error: number between 0 and 1; ~ l2_norm(original - approximation)/l2_norm(original)

Returns:
num_coefficients --> number of coefficients required to stay below the supplied error bound 
'''
def num_coefficients_for_rel_error(cum_err2, relative_error):
    err2 = cum_err2[-1]*relative_error*relative_error
    # ind-1 --> number of elements less than or equal to err2 in cum_err2 --> leave out that many
    ind = np.searchsorted(cum_err2, err2 , side='right')
    
    return cum_err2.size - (ind-1)


'''
Helper for obtaining a parametrization by arc length of a piecewise linear function.

Args:
data: a (n,d) array of n points, where d is the dimension of th input space

Returns:
An asending sequence of n values corresponding to the arc length up to the corresponding vertex.
'''
def get_arc_length_seq(data):
    arc_length_seq = np.empty(data.shape[0], dtype=float)
    arc_length_seq[0] = 0
    arc_length_seq[1:] = np.linalg.norm(data[:-1,:]-data[1:,:], ord=2, axis=1)
    arc_length_seq = np.cumsum(arc_length_seq)
    
    return arc_length_seq


'''
Evaluate a piecewise linear curve parametrized by arc length given by data.

Args:
t: an array of shape (k) of arc lengths where the curve is to be evaluated
data: (n, d) array of the curves vertecies
arc_length_seq: a precomputed sequence of arc lengths corresponding to the points; see get_arc_length_seq

Returns:
An array of shape (k, d) containing the curve's values at the arc lengths specified by t
'''
def eval_piecewise_linear(t, data, arc_length_seq):
    # array of shape (k) containing the number of points encountered at smaller arc lengths than t
    ind = np.searchsorted(arc_length_seq, t)
    
    temp1 = data[ind-1,:]
    temp2 = data[ind,:]
    
    t1 = arc_length_seq[ind-1]
    t2 = arc_length_seq[ind]
    
    s = (t - t1)/(t2-t1)
    val = (1-s[:,np.newaxis])*temp1 + s[:,np.newaxis]*temp2
    
    return val


if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    C = np.array([9.0,7,3,5,7,4,9,0])
    '''
    #normalize:
    #C = C/np.sqrt(C.size)
    print(C)    
    
    B = Decomposition(C)
    print(B)
    
    A = Synthesis(B)
    print(A)
    '''
    lena = np.asarray(PIL.Image.open('mona.jpg'))    
    lena = np.mean(lena, axis=2)
    #lena = np.random.randint(0, 256, (256,256))
    
    plt.imshow(lena, cmap='gray')
    plt.show()
    
    
    transform, sort_indices = decompose_sort(lena, nonstandard=True)
    
    cum_err2 = cumulative_squared_error(transform, sort_indices)
    
    print(transform.size)
    print(cum_err2.size)
    print(l2_norm(lena))
    print(l2_norm(transform))
    print(np.sqrt(cum_err2[-1]))
    
    x = np.linspace(1,0, len(cum_err2))
    y = np.sqrt(cum_err2/cum_err2[-1])
    
    print(x[-1])
    print(y[-1])
    
    data = np.hstack((x.reshape((-1,1)),y.reshape((-1,1))))
    print(data.shape)
    arc_length_seq = get_arc_length_seq(data)
    
    t = np.linspace(0, arc_length_seq[-1], 1000)
    c = eval_piecewise_linear(t, data, arc_length_seq)
    
    plt.plot(x,y)
    plt.scatter(c[:,0], c[:,1])
    plt.xlabel('Fraction of Coefficients Used')
    plt.ylabel('Relative $L^2$-Error')
    plt.grid()
    plt.show()
    
    #plt.imshow(NonstandardSynthesis(transform), cmap='gray')
    #plt.show()
    
    
    fractions = [0.05]#[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    for frac in fractions:
        plt.imshow(partially_reconstruct_img(transform, sort_indices, int(frac*lena.size), nonstandard=True), cmap='gray')
        plt.title(str(int(frac*lena.size))+'/'+str(lena.size)+'='+str(int(frac*lena.size)/lena.size)+'%')
        plt.show()
    
    #plt.imshow(lena, cmap='gray')
    #plt.show()
    #currently unnormalized...
    
    
    '''
    plt.imshow(StandardDecomposition(lena), cmap='gray')
    plt.show()
    
    plt.imshow(StandardSynthesis(StandardDecomposition(lena)), cmap='gray')
    plt.show()
    
    plt.imshow(NonstandardDecomposition(lena), cmap='gray')
    plt.show()
    
    plt.imshow(NonstandardSynthesis(NonstandardDecomposition(lena)), cmap='gray')
    plt.show()
    '''
    
    '''
    mona = np.asarray(PIL.Image.open('mona.jpg'))
    mona = np.mean(mona, axis=2)
    plt.imshow(mona, cmap='gray')
    plt.show()
    
    plt.imshow(StandardDecomposition(mona), cmap='gray')
    plt.show()
    
    plt.imshow(StandardSynthesis(StandardDecomposition(mona)), cmap='gray')
    plt.show()
    
    plt.imshow(NonstandardDecomposition(mona), cmap='gray')
    plt.show()
    
    plt.imshow(NonstandardSynthesis(NonstandardDecomposition(mona)), cmap='gray')
    plt.show()
    '''
    
    
    
    
