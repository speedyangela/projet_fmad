import numpy as np
from src.distances import distance_hamming, distance_spearman
from scipy.optimize import linear_sum_assignment

#QUESTION 12

def calcul_u1_approbation(p):
    n=len(p) 
    m=len(p[0])
    somme_col=np.sum(p, axis=0) #on compte le nbr de 1 par colonne(par candidat donc)
    a_consensus=[]
    for i in somme_col:
        if i>n/2: #si + de la moitié des votants approuvent le candidat on le met dans le bulletin consensus
            a_consensus.append(1)
        else: #sinon on met qu'on ne l'approuve pas 
            a_consensus.append(0)
    u1=0
    for i in range(n): #on ajoute la distance de chaque votant par rapport au consensus 
        u1+=distance_hamming(a_consensus, p[i])
    return u1


def calcul_u1_ordres(p):
    n=len(p) 
    m=len(p[0]) 
    matrice_opti=np.zeros((m,m)) #on initalise matrice où les lignes=les candidats et colonnes=les rangs possibles
    for i in range(m): #pour chaque candidat
        for rang_propose in range(m): #pour chaque rang possible
            cout_tot=0
            for j in range(n): #pour chaque votant
                rang_votant=p[j].tolist().index(i) #on trouve le rang du candidat i dans le bulletin du votant j
                cout_tot+=abs(rang_votant-rang_propose) #on ajoute la différence abs entre le rang du votant et le rang proposé
            matrice_opti[i][rang_propose]=cout_tot #on remplit la matrice avec les coûts totaux pour chaque candidat et chaque rang proposé
    row_ind,col_ind=linear_sum_assignment(matrice_opti) #on utilise l'algo scipy pour trouver le consensus. row_ind=les candidats et col_ind les positions optimales
    u1=matrice_opti[row_ind, col_ind].sum() #on va chercher les coeff de la matrice qui correspond à chaque (candidat,position)  et on les somme pour avoir u1
    return u1
#vidéo pour l'algo hongrois 