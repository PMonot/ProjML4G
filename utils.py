import numpy as np


def w(u):
    """
    increasing convex positive function
    w(u) = u/(u+0.1)
    """
    return(1-np.exp(-u))

def dw(u):
    """
    gradient of w
    dw(u) = 0.1/(u+0.1)^2
    """
    return(np.exp(-u))

def a(k,A,C):
    """Computes coefficient a according to the article"""
    return(A/np.ceil((1+k*np.log(1+k))/C))

def b(k,B,C):
    """Computes coefficient b according to the article"""
    return(B/np.ceil((k+1)/C))

def Gamma(u,M,S2):
    """
    Computes the projection on the space H = {u in R+^n | sum(u) <= M}
    In the worst case, the complexity can be O(n), but in general 1 or 2 iterations will be enough
    """
    n = len(S2)
    a = np.zeros(u.size)
    a[np.array(S2)-1]+=1
    proj = u - ((sum(u)-M)/n)*a
    while any(proj<0):
        proj *= (proj >= 0)
        a = (proj > 0)
        proj -= ((sum(proj)-M)/sum(a))*a
    return(proj)

