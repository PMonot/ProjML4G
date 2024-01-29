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

def mat_A(G):
    """
    Computes the matrix A as in the article
    """
    N = len(G.nodes()) + 1
    A = np.zeros((N-1,N-1))
    S0_index = 0
    S2_index = 0
    for i in range(1,N):
        for j in range(1,N):
            if i != j :
                if G.nodes[i]['status'] == 0 :
                    S0_index = 1
                elif G.nodes[i]['status'] == 2 :
                    S2_index = 1
                else :
                    S0_index = 0
                    S2_index = 0
                if G.has_edge(i,j) :
                    A[i-1][j-1] = (1 - S0_index) * (1 - S2_index * G.nodes[i]['alpha']) * G[i][j]['weight']
    return(A)

def mat_H(G):
    N = len(G.nodes())
    H = np.zeros((N,1))
    for node in G.nodes():
        if G.nodes[node]['status'] == 0:
            H[node-1] = G.nodes[node]['opinion']
    return(H)

def mat_WS0(G):
    N = len(G.nodes()) + 1
    W = np.zeros((N-1,1))
    S0_index = 0
    H = mat_H(G)
    for i in range(1,N):
        if G.nodes[i]['status'] == 0 :
            S0_index = 1
        else :
            S0_index = 0
        W[i-1] = S0_index * H[i-1]
    return(W)

def mat_WS2(G):
    N = len(G.nodes()) + 1
    W = np.zeros((N-1,1))
    S2_index = 0
    for i in range(1,N):
        if G.nodes[i]['status'] == 2 :
            S2_index = 1
        else :
            S2_index = 0
        W[i-1] = S2_index * G.nodes[i]['alpha']
    return(W)
