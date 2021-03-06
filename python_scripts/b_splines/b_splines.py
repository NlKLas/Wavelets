import numpy as np
from scipy.sparse import lil_matrix
import scipy as sci
import scipy.sparse.linalg
import matplotlib.pyplot as plt

'''
An efficient evaluation of a specified B-spline curve.

Args:
x: (Array of) scalar value(s) that indicate where the spline is to be evaluated
t: knot vector of the B-spline; assumed to be sorted!
c: n x d matrix containing the controll points (d: dimension of the output-space)
p: degree of the B-Spline

The returned curve is defined by

S(x) =  sum_{i}(c[i,:]*B_{i,p}(x))

where B_{i,p} are the B-Spline basis functions of degree p.
The basis functions may thus be recovered by passing a one-hot-vector for c.
'''
def deBoor(x,t,c,p):
    #first figure out which intervalls the x-values belong to
    k = np.searchsorted(t,x)-1
    k[k == -1] = p
    
    ind = k + (np.arange(-p,1,1))[...,np.newaxis]
    d = c[ind,...]
    
    for r in range(1,p+1):
        for j in range(p, r-1, -1):
            temp = t[j-p+k]
            alpha = ((x - temp)/(t[j+1-r+k] - temp))[...,np.newaxis]
            d[j,...] = (1-alpha)*d[j-1,...] + alpha*d[j,...]
    
    return d[-1,...]


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
    
    P = P/16
    # TODO: convert the matrix format to whatever is fastest!
    return P.transpose()
        

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
    
    Q = lil_matrix((2**(j-1), 2**j+3))
    
    if j == 1:
        Q[0, 0:5] = [1,-2,3,-2,1]
        Q = Q/3
        #print(Q.transpose().toarray()) 
    elif j == 2:
        Q[0, 0:6] = [-1368,2064,-1793,1053,-691,240]
        Q[1, 1:7] = [240,-691,1053,-1793,2064,-1368]
        Q = Q/2064
        #print(Q.transpose().toarray())
    elif j == 3:
        Q[0, 0:8] = [-394762/574765,1,-33030599/41383080,633094403/1655323200,-19083341/137943699,4681957/165532320,-864187/413830800,27877/1655323200]
        Q[1, 1:9] = [-7166160/28124263,333497715/478112471,-881412943/956224942,1,-689203555/956224942,8833647/28124263,-74736797/956224942,6908335/478112471]
        Q[2, 2:10] = [6908335/478112471,-74736797/956224942,8833647/28124263,-689203555/956224942,1,-881412943/956224942,333497715/478112471,-7166160/28124263]
        Q[3, 3:11] = [27877/1655323200,-864187/413830800,4681957/165532320,-19083341/137943699,633094403/1655323200,-33030599/41383080,1,-394762/574765]
        #print(Q.transpose().toarray())
    else:
        Q[0, 0:8] = [-394762/574765,1,-33030599/41383080,633094403/1655323200,-19083341/137943699,4681957/165532320,-864187/413830800,27877/1655323200]
        Q[1, 1:10] = [-1050072320/4096633377,2096854390/2989435167,-11070246427/11957740998,1,-157389496903/221218202358,1732435193/5821531641,-27809640281/442436404716,171326708/36869700393,-1381667/36869700393]
        Q[2, 2:12] = [307090/19335989,-6643465/77343956,6646005/19335989,-29839177/38671978,1,-58651607/77343956,6261828/19335989,-1328199/19335989,98208/19335989,-792/19335989]
        
        i = 3
        k = 3
        while i < 2**(j-1)-3:
            Q[i, k:(k+11)] = [-1/24264,31/6066,-559/8088,988/3033,-9241/12132,1,-9241/12132,988/3033,-559/8088,31/6066,-1/24264]
            i = i+1
            k = k+2
        
        Q[i, k:(k+10)] = [-792/19335989,98208/19335989,-1328199/19335989,6261828/19335989,-58651607/77343956,1,-29839177/38671978,6646005/19335989,-6643465/77343956,307090/19335989]
        i = i+1
        k = k+2
        Q[i, k:(k+9)] = [-1381667/36869700393,171326708/36869700393,-27809640281/442436404716,1732435193/5821531641,-157389496903/221218202358,1,-11070246427/11957740998,2096854390/2989435167,-1050072320/4096633377]
        i = i+1
        k = k+2
        Q[i, k:(k+8)] = [27877/1655323200,-864187/413830800,4681957/165532320,-19083341/137943699,633094403/1655323200,-33030599/41383080,1,-394762/574765]
        #print(Q.transpose().toarray())
    
    # TODO: convert the matrix format to whatever is fastest!
    return Q.transpose()


'''
Return the combined projection matrix (P|Q) for cubic uniform endpoint interpolaing b-splines for level j
To be used as a first step for generating the (permutated) filter bank matrix (P|Q)*ColPerm
Solve
(P|Q)*ColPerm*ColPerm^{-1}*(C^j/D^j) = C^{j+1}
for (C^j/D^j).
ColPerm will be chosen such that (P|Q)*ColPerm is a banded diagonal matrix

Args:
j: level of detail -> j=1,2,3,...
'''
def projectionPQcubic(j):
    return sci.sparse.hstack((projectionPcubic(j), projectionQcubic(j)), format='csc')


'''
Return a permutation for interspercing the columns of P and Q of a given level j.
For every j P has precisely 3 additional columns compared to Q. I propose the following interspercing scheme:
P0 P1 Q0 P2 Q1 P3 Q2 P4 ... Qn-1 Pn+1 Pn+2
where n = 2^{j-1}.
The result will be a permutation intended to be used to index the columns of (P|Q)

The inverse permutation has the following shape (that is (P|Q) expressed in columns of A:=(P|Q)[perm]):
A0 A1 A3 A5 A7 ... A2n-1 A2n+1 A2n+2 A2 A4 A6 ... A2n

If the permutation \pi encodes a column permutation matrix, that same matix is encoded by the row permutation \tau = \pi^{-1}

Args:
j: level of detail -> j=1,2,3,...
'''
def permCubic(j):
    n = 2**(j-1)
    perm = np.empty(2*n + 3, dtype=int)
    perm[0] = 0
    perm[-2:] = [n+1, n+2]
    temp = np.arange(0,n)
    perm[2*temp+1] = temp+1
    perm[2*temp+2] = temp + n+3
    
    inv = np.empty(2*n + 3, dtype=int)
    inv[0] = 0
    inv[1:(n+1)] = 2*temp+1
    inv[(n+1):(n+3)] = [2*n+1,2*n+2]
    inv[(n+3):] = 2*(temp+1)
    return (perm,inv)
    

'''
The filter bank equation has the form
(P|Q)*(C^j/D^j) = C^{j+1}
and is to be solved for (C^j/D^j).
This is equivalent to the equation
(P|Q)*Perm*Perm^{-1}*(C^j/D^j) = C^{j+1}
where Perm is an arbitrary permutation matrix represented by the column permutation \pi.
Introduce X := Perm^{-1}*(C^j/D^j) and W := (P|Q)*Perm. The equation thus becomes:
W*X = C^{j+1}.
After solving this equation for X, (C^j/D^j) can be recovered as
(C^j/D^j) = Perm*X.
Note that if Perm is represented by the column permutation \pi, its representation as a row permutation is \tau = \pi^{-1}.
If \pi and \pi^{-1} are known, the multiplication with Perm can be realized by proper indexing.
Following this stategy, it is possible to efficiently solve the problem at hand since Perm can be chosen such that W is a banded matrix while (P|Q) isn't.
LU decomposition can be applied to the later problem in linear time (or so I have read; I am not super confident about this however).

The LU decomposition can be precomputed as soon as (P|Q) is available (i.e. on startup).
A single stage of the filter bank can later be efficiently solved with the precomputed decomposition and the permutation \pi^{-1}.

This routine precomputes the LU decomposition for a given level of detail j.

Args:
j: level of detail -> j=1,2,3,...
'''
def createFilterCubic(j):
    perm, inv_perm = permCubic(j)
    W = (projectionPQcubic(j))[:,perm]
    AB = sci.sparse.linalg.splu(W, permc_spec='NATURAL')
    return (lambda cd: (AB.solve(cd))[inv_perm,...])


'''
Return a 'vector' of control points, which define an endpoint interpolating uniform cubic b-spline, which interpolates the given set of points. n+1 points yield n+3 control points.
This is usefull for generating a curve.
The reverse transform is also easyly implemented.

Args:
D: a numpy array of shape (n+1,d) containing the data points to be interpolated as row vectors 
Returns:
P: a numpy array of shape (n+3,d) containing the control points of the resuling b-spline curve.
'''
def interpolateCubic(D):
    #print(D)
    n,d = D.shape
    n = n-1
    
    entries = np.empty((3,n+1))
    entries[0,0:2] = [0,-1]
    entries[0,2:-1] = 1/6
    entries[0,-1] = 1/4
    
    entries[1,0:2] = [3,7/12]
    entries[1,2:-2] = 2/3
    entries[1,-2:] = [7/12,3]
    
    entries[2,0] = 1/4
    entries[2,1:-2] = 1/6
    entries[2,-2:] = [-1,0]
    
    offsets = [1,0,-1]
    M = sci.sparse.spdiags(entries, offsets, n+1, n+1, format='csc')
    #print(M.toarray())
    
    M_inv = sci.sparse.linalg.splu(M, permc_spec='NATURAL')
    
    P = np.empty((n+3,d))
    P[0,...] = D[0,...]
    P[1,...] = 2*D[0,...]
    P[2:-2,...] = D[1:-1,...]
    P[-2,...] = 2*D[-1,...]
    P[-1,...] = D[-1,...]
    #print(P)
    
    P[1:-1,...] = M_inv.solve(P[1:-1,...])
    #print(P)
    
    #print(M.dot(P[1:-1,...]))
    
    return P


'''
For a knot vector with n+1 entries there are n+3 cubic b-spline basis functions. This means that n+3
control points are required to specify cubic b-spline curves for n+1 knots (NOT counting paddings).
B-spline interpolation of n+1 points yields n+3 control points.
Thus the amount of points to be interpolated is equal to the resulting number of knots.

For multiresolution analysis n=2^k is required. A given amount of points must therefore be upsampled 
such that the number of resulting points is equal to 2^k+1 for some k.

The idea is to linearly interpolate the given points and then resample 2^k+1 points from the resulting
curve.

Args:
D: a numpy array of shape (n+1,d) containing the data points to be upsampled
'''
def upsample(D):
    n = D.shape[0]-1
    m = np.around(np.power(2, np.ceil(np.log2(n)))).astype(int)
    
    t = unifSubdiv(n,1)
    
    x = np.arange(0,m+1)/m
    
    return deBoor(x,t,D,1)



'''
Return a uniform subdivision of [0,1] into n intervalls with d padding 0's and 1's (as needed for endpoint interpolating uniform b-splines).

Args:
n: amount of subdivisions
d: padding size (i.e. spline degree)

Returns:
np.array([0,...,0,0,1/n,2/n,...,n/n,1,...,1])
'''
def unifSubdiv(n,d):
    t = np.empty(n+1+2*d)
    t[:d] = 0
    t[d:-d] = np.arange(0,n+1)/n
    t[-d:] = 1
    
    return t


'''
Plot the uniform endpoint interpolating b-spline curve given by control_points of degree degree into ax using N sample points
'''
def plot_uniform_b_spline_curve(ax, control_points, degree=3, N=1000, **kwargs):
    n = control_points.shape[0]-degree
    
    x = np.linspace(0,1,N)
    t = unifSubdiv(n, degree)
    
    data = deBoor(x,t,control_points,degree)
    
    ax.plot(data[:,0], data[:,1], **kwargs)


'''
Completely decompose a cubic endpoint interpolating uniform b-spline curve given by
2^k+3 control points into its coarser representations C^j for j=k, k-1, ..., 1, 0

Args:
C: a numpy array of shape (n+3,d) containing control points, where n=2^k for some k
F: List of precomputed filters such that F[j-1](C^j) = (C^j-1 | D^j-1)

Returns:
A list L containing the approximations such that L[j] = C^j.
--> L = [C^0, C^1, ..., C^k-1, C^k] (note: C^k = C)
'''
def completeDecomposition(C, F=None):
    n = C.shape[0]-3
    k = np.around(np.log2(n)).astype(int)
    
    L = [None]*(k+1)
    L[k] = C
    
    if not F:
        while k>0:
            f = createFilterCubic(k)
            L[k-1] = (f(L[k]))[:(2**(k-1)+3),...]
            
            k = k-1
    
    else:
        while k>0:
            f = F[k-1]
            L[k-1] = (f(L[k]))[:(2**(k-1)+3),...]
            
            k = k-1
    
    return L


'''
Create and return the analysis filters as well as the P-projection matrices required for
multiresolution editing of an endpoint interpolating uniform cubic b-spline curve represented
by n=2^k+3 (for some k) control points

Args:
k: k such that n=2^k+3

Returns:
(P, F), where P is a list of P-projections such that P[j]=P^(j+1) for j=0, 1, ..., k-1 and
F is a list of analysis filters such that F[j]=f^(j+1) for j=0, 1, ..., k-1

note: C^j = P^j*C^(j-1) + Q^j*D^(j-1), f^j(C^j) = (C^(j-1) | D^(j-1)) 
'''
def createFiltersAndProjectionsForMLE(k):
    P = [None]*k
    F = [None]*k
    for j in range(k):
        P[j] = projectionPcubic(j+1)
        F[j] = createFilterCubic(j+1)
    
    return (P, F)

'''
Propagate a change deltaC_j on some level 0 <= j <= k to all other levels.

Args:
deltaC_j: changes on level j
L: A list L containing the approximations such that L[j] = C^j.
    --> L = [C^0, C^1, ..., C^k-1, C^k] (note: C^k = C)
P: precomputed P-projections
F: precomputed filters

Returns:
an updated version of L
'''
def updateCompleteDecomposition(deltaC_j, L, P, F):
    j = np.around(np.log2(deltaC_j.shape[0]-3)).astype(int)
    k = len(L)-1
    
    L[j] = L[j] + deltaC_j
    
    temp = deltaC_j.copy()
    i = j
    while i > 0:
        f = F[i-1]
        temp = (f(temp))[:(2**(i-1)+3),...]
        L[i-1] = L[i-1] + temp
        i = i-1
    
    temp = deltaC_j.copy()
    i = j+1
    while i <= k:
        temp = P[i-1].dot(temp)
        L[i] = L[i] + temp
        i = i+1
    
    return L



if __name__ == '__main__':
    np.set_printoptions(linewidth=200)#,precision=1)
    '''
    D = np.array([[0.0,0],[1,0],[1,1],[0,1],[0.5,0.5],[1,1]])
    C = upsample(D)
    print(D)
    print(C)
    #plt.scatter(D[:,0], D[:,1], color='blue')
    #plt.plot(D[:,0], D[:,1], color='blue', ls='--')
    #plt.scatter(C[:,0], C[:,1], color='red')
    
    A = interpolateCubic(C)
    
    #plt.scatter(A[:,0], A[:,1], color='green')
    #plt.plot(A[:,0], A[:,1], color='green', ls='--')
    plot_uniform_b_spline_curve(plt.gca(), A, degree=3, N=1000, color='green')
    '''
    
    '''
    n = A.shape[0]-3
    k = np.around(np.log2(n)).astype(int)
    
    f = createFilterCubic(k)
    
    B = f(A)
    B_C = B[:(2**(k-1)+3),...]
    
    plt.scatter(B_C[:,0], B_C[:,1], color='red')
    plt.plot(B_C[:,0], B_C[:,1], color='red', ls='--')
    plot_uniform_b_spline_curve(plt.gca(), B_C, degree=3, N=1000, color='red')
    '''
    
    '''
    L = completeDecomposition(A)
    
    for G in L:
        #plt.scatter(G[:,0], G[:,1])
        #plt.plot(G[:,0], G[:,1], ls='--')
        plot_uniform_b_spline_curve(plt.gca(), G, degree=3, N=1000)
    
    plt.show()
    '''
    
    '''
    print((projectionPQcubic(4).toarray()!=0)*1)
    perm, inv = permCubic(4)
    print(perm)
    print(inv)
    print(((projectionPQcubic(4).toarray()!=0)*1)[:,perm])
    print(((projectionPQcubic(4)[:,perm]).toarray()!=0)*1)
    print((((projectionPQcubic(4)[:,perm]).toarray()!=0)*1)[:,inv])
    #print(((((np.arange(0,2**4+3))[perm])[inv])[inv])[perm])
    '''
    
    '''
    n = 10
    x = np.arange(0,n+1).reshape((n+1,1))
    interpolateCubic(np.hstack((x, np.sin(x))))
    '''
    
    #print(unifSubdiv(16,3))
    
    '''
    # funktioniert, wenn man mal davon absieht, dass die letzte Basisfunktion 
    # aus irgendwelchen Gründen bei 0 den Wert 1 hat....? ... sollte behoben sein!
    p = 1
    n = 10
    t = np.append(np.array([0]*p) ,np.arange(0,n-p+1,1))
    t = np.append(t, [t[-1]]*p)

    x = np.linspace(t[0],t[-1],500)

    for i in range(n):
        c = np.zeros(n).reshape((n,1))
        c[i,0] = 1
        
        plt.plot(x, deBoor(x,t,c,p))
        
        for j in t:
            plt.axvline(j)
        
        plt.grid()
        plt.show()
    
    '''
    
    '''
    # for some reason the program fails for p=3 and n=4, which should work...
    # --> fixed it ! (make sure to pass c as a floating point array......)
    p = 3
    n = 5
    t = np.append(np.array([0]*p) ,np.arange(0,n-p+1,1))
    t = np.append(t, [t[-1]]*p)

    x = np.linspace(t[0],t[-1],50)

    c = np.array([[0.0,0],[1,0],[1,1],[0,1],[0.5,0.5]])

    data = deBoor(x,t,c,p)

    plt.scatter(c[:,0], c[:,1])
    #plt.scatter(deBoor(x,t,c[0,:],p),deBoor(x,t,c[1,:],p))
    plt.plot(data[:,0], data[:,1])

    #plt.plot(x,deBoor(x,t,c[0,:],p))

    #plt.grid()
    plt.savefig('b_spline_curve.pdf')
    plt.show()
    '''
    




