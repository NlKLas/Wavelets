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

def StandardSynthesis(C):
    img = C.copy()
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

def NonstandardSynthesis(C):
    img = C.copy()
    
    h = 1
    while h < C.shape[0]:
        h = 2*h
        img[0:h,0:h] = SynthesisStepY(img[0:h,0:h])
        img[0:h,0:h] = SynthesisStepX(img[0:h,0:h])
        #plt.imshow(img, cmap='gray')
        #plt.show()
    return img

if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    C = np.array([9.0,7,3,5,7,4,9,0])
    
    #normalize:
    C = C/np.sqrt(C.size)
    print(C)    
    
    B = Decomposition(C)
    print(B)
    
    A = Synthesis(B)
    print(A)
    
    lena = np.asarray(PIL.Image.open('lena.ppm'))    
    lena = np.mean(lena, axis=2)
    plt.imshow(lena, cmap='gray')
    plt.show()
    #currently unnormalized...
    '''
    plt.imshow(StandardDecomposition(lena), cmap='gray')
    plt.show()
    
    plt.imshow(StandardSynthesis(StandardDecomposition(lena)), cmap='gray')
    plt.show()
    
    plt.imshow(NonstandardDecomposition(lena), cmap='gray')
    plt.show()
    '''
    plt.imshow(NonstandardSynthesis(NonstandardDecomposition(lena)), cmap='gray')
    plt.show()
    
    
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
    
    
    
    
