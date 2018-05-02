import PIL
import numpy as np
import matplotlib.pyplot as plt



def DecompositionStep(C):
    #print('\t'+str(C))
    h = C.size
    C_prime = np.empty_like(C)
    for i in range(0,h//2):
        # sqrt(2) * [Mittelwert von C[2*i-1] und C[2*i]]
        C_prime[i] = (C[2*i]+C[2*i+1])/(np.sqrt(2))
        # sqrt(2) * [Abstand von C[2*i-1] bzw. C[2*i] vom Mittelwert]
        C_prime[h//2+i] = (C[2*i]-C[2*i+1])/(np.sqrt(2))
    
    #print('\t'+str(C_prime))
    return C_prime


def Decomposition(C):
    #print(C)
    h = C.size
    # Multipliziere Alles mit 2^{-j/2} = 1/sqrt(2^j) = 1/sqrt(h)
    C = C/np.sqrt(h)
    while h > 1:
        #print(C)
        C[0:h] = DecompositionStep(C[0:h])
        h = h//2
    
    #print(C)
    return C


def SynthesisStep(C):
    h = C.size
    C_prime = np.empty_like(C)
    for i in range(0, h//2):
        C_prime[2*i] = C[i]+C[h//2+i]
        C_prime[2*i+1] = C[i]-C[h//2+i]
    
    return C_prime



def Synthesis(C):
    h = C.size
    
    i = 2
    while i <= h:
        C[0:i] = SynthesisStep(C[0:i])
        C[i:h] = np.sqrt(2)*C[i:h]
        i = 2*i
    
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
    C = C/np.sqrt(h)
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
    C = C/np.sqrt(h)
    while h > 1:
        C[0:h,:] = DecompositionStepY(C[0:h,:])
        h = h//2
    return C

def SynthesisStepX(C):
    h = C.shape[1]
    C_prime = np.empty_like(C)
    for i in range(0, h//2):
        C_prime[:,2*i] = C[:,i]+C[:,h//2+i]
        C_prime[:,2*i+1] = C[:,i]-C[:,h//2+i]
    return C_prime

def SynthesisX(C):
    h = C.shape[1]
    i = 2
    while i <= h:
        C[:,0:i] = SynthesisStepX(C[:,0:i])
        C[:,i:h] = np.sqrt(2)*C[:,i:h]
        i = 2*i
    return C

def SynthesisStepY(C):
    h = C.shape[0]
    C_prime = np.empty_like(C)
    for i in range(0, h//2):
        C_prime[2*i,:] = C[i,:]+C[h//2+i,:]
        C_prime[2*i+1,:] = C[i,:]-C[h//2+i,:]
    return C_prime

def SynthesisY(C):
    h = C.shape[0]
    i = 2
    while i <= h:
        C[0:i,:] = SynthesisStepY(C[0:i,:])
        C[i:h,:] = np.sqrt(2)*C[i:h,:]
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
    
#TODO: Implement the non-standard decompostition and synthesis
'''
I will assume a square image (if in doubt, add padding...)
'''
def NonstandardDecomposition(img):
    C = img.copy()
    
    h = C.shape[0]
    C = C/h
    while h > 1:
        C[0:h,0:h] = DecompositionStepX(C[0:h,0:h])
        C[0:h,0:h] = DecompositionStepY(C[0:h,0:h])
        plt.imshow(C, cmap='gray')
        plt.show()
        h = h//2
    return C

def NonstandardSynthesis(C):
    img = C.copy()
    
    h = img.shape[0]
    i = 2
    while i <= h:
        img[0:i,0:i] = SynthesisStepY(img[0:i,0:i])
        
        img[0:i,0:i] = SynthesisStepX(img[0:i,0:i])
        
        img[i:h,0:i] = 2*img[i:h,0:i]
        img[i:h,i:h] = 2*img[i:h,i:h]
        img[0:i,i:h] = 2*img[0:i,i:h]
        
        plt.imshow(img, cmap='gray')
        plt.show()
        i = 2*i
    return img

if __name__ == "__main__":
    np.set_printoptions(linewidth=200)
    C = np.array([9.0,7,3,5,7,4,9,0])
    
    print(C)    
    
    print(Decomposition(C))
    
    print(Synthesis(Decomposition(C)))
    
    lena = np.asarray(PIL.Image.open('lena.ppm'))    
    lena = np.mean(lena, axis=2)
    plt.imshow(lena, cmap='gray')
    plt.show()
    '''
    plt.imshow(StandardDecomposition(lena), cmap='gray')
    plt.show()
    
    plt.imshow(StandardSynthesis(StandardDecomposition(lena)), cmap='gray')
    plt.show()
    '''
    plt.imshow(NonstandardDecomposition(lena), cmap='gray')
    plt.show()
    
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
    
    
    
    
