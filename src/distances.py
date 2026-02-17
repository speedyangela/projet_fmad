#QUESTION 8
def distance_hamming(a1,a2):  #pour approbation
    d=0
    m=len(a1) #nombre candidats 
    for i in range(m):
        if a1[i]!=a2[i]: #si les bulletins sont différents (un a mis un 0 et l'autre un 1) pour le candidat i
            d+=1 
    return d


def distance_spearman(b1,b2): #pour ordres 
    d=0
    m=len(b1) 
    l1=b1.tolist() #pour pouvoir utiliser .index() 
    l2=b2.tolist()
    for i in range(m): #on cherche la position du candidat dans chaque bulletin 
        rang1=l1.index(i)
        rang2=l2.index(i)
        d+=abs(rang1-rang2)
    return d
