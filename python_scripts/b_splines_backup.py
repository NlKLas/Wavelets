import numpy as np
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt

'''
An efficient evaluation of a specified B-spline curve.

Args:
x: (Array of) scalar value(s) that indicate where the spline is to be evaluated
t: knot vector of the B-spline; assumed to be sorted!
c: d x n matrix containing the controll points (d: dimension of the output-space)
p: degree of the B-Spline

The returned curve is defined by

S(x) =  sum_{i}(c[:,i]*B_{i,p}(x))

where B_{i,p} are the B-Spline basis functions of degree p.
The basis functions may thus be recovered by passing a one-hot-vector for c.
'''
def deBoor(x,t,c,p):
    #first figure out which intervalls the x-values belong to
    k = np.searchsorted(t,x)-1
    k[k == -1] = p
    
    ind = np.arange(-p,1,1) + k[...,np.newaxis]
    d = c[...,ind]
    
    for r in range(1,p+1):
        for j in range(p, r-1, -1):
            temp = t[j-p+k]
            alpha = (x - temp)/(t[j+1-r+k] - temp)
            d[...,j] = (1-alpha)*d[...,j-1] + alpha*d[...,j]
    
    return d[...,-1]


'''
Return the projection matrix P for cubic uniform endpoint interpolaing b-splines for level j
This matrix basically encodes the two scale relation.
For details refer to Finkelstein et al..

Args:
j: level of detail -> j=1,2,3,...
'''
def projectionPcubic(j):
    if j <= 0:
        raise Exception('The specified level of detail must be strictly positive!')
    
    P = lil_matrix((2**(j-1)+3, 2**j+3))
    
    if j == 1:
        P[0, 0:2] = [16, 8]
        P[1, 1:3] = [8,8]
        P[2, 2:4] = [8,8]
        P[3, 3:5] = [8,16]
        #print(P.transpose().toarray())
    elif j == 2:
        P[0, 0:2] = [16,8]
        P[1, 1:4] = [8,12,3]
        P[2, 2:5] = [4,10,4]
        P[3, 3:6] = [3,12,8]
        P[4, 5:7] = [8,16]
        #print(P.transpose().toarray())
    else:
        P[0, 0:2] = [16,8]
        P[1, 1:4] = [8,12,3]
        P[2, 2:6] = [4,11,8,2]
        
        i = 3
        k = 3
        while i < 2**(j-1):
            P[i, k:(k+5)] = [2,8,12,8,2]
            i = i+1
            k = k+2
        
        P[i, k:(k+4)] = [2,8,11,4]
        i = i+1
        k = k+2
        P[i, k:(k+3)] = [3,12,8]
        i = i+1
        k = k+2
        P[i, k:(k+2)] = [8,16]
        #print(P.transpose().toarray())
    
    # TODO: convert the matrix format to whatever is fastest!
    return P.transpose()/16
        

'''
Return the projection matrix Q for cubic uniform endpoint interpolaing b-splines for level j
For details refer to Finkelstein et al..

Args:
j: level of detail -> j=1,2,3,...

I NEVER want to do this again!!!!!!!!!!!!!
'''
def projectionQcubic(j):
    if j <= 0:
        raise Exception('The specified level of detail must be strictly positive!')
    
    P = lil_matrix((2**(j-1), 2**j+3))
    
    if j == 1:
        P[0, 0:5] = [1,-2,3,-2,1]
        P = P/3
        #print(P.transpose().toarray()) 
    elif j == 2:
        P[0, 0:6] = [-1368,2064,-1793,1053,-691,240]
        P[1, 1:7] = [240,-691,1053,-1793,2064,-1368]
        P = P/2064
        #print(P.transpose().toarray())
    elif j == 3:
        P[0, 0:8] = [-394762/574765,1,-33030599/41383080,633094403/1655323200,-19083341/137943699,4681957/165532320,-864187/413830800,27877/1655323200]
        P[1, 1:9] = [-7166160/28124263,333497715/478112471,-881412943/956224942,1,-689203555/956224942,8833647/28124263,-74736797/956224942,6908335/478112471]
        P[2, 2:10] = [6908335/478112471,-74736797/956224942,8833647/28124263,-689203555/956224942,1,-881412943/956224942,333497715/478112471,-7166160/28124263]
        P[3, 3:11] = [27877/1655323200,-864187/413830800,4681957/165532320,-19083341/137943699,633094403/1655323200,-33030599/41383080,1,-394762/574765]
        #print(P.transpose().toarray())
    else:
        P[0, 0:8] = [-394762/574765,1,-33030599/41383080,633094403/1655323200,-19083341/137943699,4681957/165532320,-864187/413830800,27877/1655323200]
        P[1, 1:10] = [-1050072320/4096633377,2096854390/2989435167,-11070246427/11957740998,1,-157389496903/221218202358,1732435193/5821531641,-27809640281/442436404716,171326708/36869700393,-1381667/36869700393]
        P[2, 2:12] = [307090/19335989,-6643465/77343956,6646005/19335989,-29839177/38671978,1,-58651607/77343956,6261828/19335989,-1328199/19335989,98208/19335989,-792/19335989]
        
        i = 3
        k = 3
        while i < 2**(j-1)-3:
            P[i, k:(k+11)] = [-1/24264,31/6066,-559/8088,988/3033,-9241/12132,1,-9241/12132,988/3033,-559/8088,31/6066,-1/24264]
            i = i+1
            k = k+2
        
        P[i, k:(k+10)] = [-792/19335989,98208/19335989,-1328199/19335989,6261828/19335989,-58651607/77343956,1,-29839177/38671978,6646005/19335989,-6643465/77343956,307090/19335989]
        i = i+1
        k = k+2
        P[i, k:(k+9)] = [-1381667/36869700393,171326708/36869700393,-27809640281/442436404716,1732435193/5821531641,-157389496903/221218202358,1,-11070246427/11957740998,2096854390/2989435167,-1050072320/4096633377]
        i = i+1
        k = k+2
        P[i, k:(k+8)] = [27877/1655323200,-864187/413830800,4681957/165532320,-19083341/137943699,633094403/1655323200,-33030599/41383080,1,-394762/574765]
        print(P.transpose().toarray())


if __name__ == '__main__':
    np.set_printoptions(linewidth=200)
    projectionQcubic(4)
    '''
    # funktioniert, wenn man mal davon absieht, dass die letzte Basisfunktion 
    # aus irgendwelchen Gründen bei 0 den Wert 1 hat....? ... sollte behoben sein!
    p = 1
    n = 10
    t = np.append(np.array([0]*p) ,np.arange(0,n-p+1,1))
    t = np.append(t, [t[-1]]*p)

    x = np.linspace(t[0],t[-1],500)

    for i in range(n):
        c = np.zeros(n)
        c[i] = 1
        
        plt.plot(x, deBoor(x,t,c,p))
        
        for j in t:
            plt.axvline(j)
        
        plt.grid()
        plt.show()


    
    # for some reason the program fails for p=3 and n=4, which should work...
    # --> fixed it ! (make sure to pass c as a floating point array......)
    p = 3
    n = 4
    t = np.append(np.array([0]*p) ,np.arange(0,n-p+1,1))
    t = np.append(t, [t[-1]]*p)

    x = np.linspace(t[0],t[-1],50)

    c = np.array([[0.0,1,1,0],[0,0,1,1]])

    data = deBoor(x,t,c,p)

    plt.scatter(c[0,:], c[1,:])
    #plt.scatter(deBoor(x,t,c[0,:],p),deBoor(x,t,c[1,:],p))
    plt.plot(data[0,:], data[1,:])

    #plt.plot(x,deBoor(x,t,c[0,:],p))

    plt.grid()
    plt.show()
    '''




