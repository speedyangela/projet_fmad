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


#QUESTION 13
#On utilise l'algorithme k-means avec k=2 du sujet pour estimer u*2(p)
#On le lance plusieurs fois et on garde le meilleur résultat (car k-means converge vers un optimum local)

def trouve_centroide_approbation(cluster):
    #on reprend le même code que calcul_u1_approbation juste on retourne le consensus (donc ici le centroide) et pas u1
    if len(cluster)==0:
        return None
    cluster_arr=np.array(cluster)
    m=len(cluster[0])
    somme_col=np.sum(cluster_arr, axis=0)
    centroide=[]
    for i in somme_col:
        if i>len(cluster)/2:
            centroide.append(1)
        else:
            centroide.append(0)
    return np.array(centroide)
    

def trouve_centroide_ordres(cluster):
    #on reprend le même code que calcul_u1_ordres juste on retourne le consensus (donc ici le centroide) et pas u1
    if len(cluster)==0:
        return None
    n_cluster=len(cluster)
    m=len(cluster[0])
    matrice_opti=np.zeros((m,m))
    for i in range(m):
        for rang_propose in range(m):
            cout_tot=0
            for j in range(n_cluster):
                rang_votant=cluster[j].tolist().index(i)
                cout_tot+=abs(rang_votant-rang_propose)
            matrice_opti[i][rang_propose]=cout_tot
    row_ind,col_ind=linear_sum_assignment(matrice_opti)
    #On reconstruit le bulletin consensus: à la position col_ind[i] on met le candidat row_ind[i]
    centroide=np.zeros(m, dtype=int)
    for i in range(m):
        centroide[col_ind[i]]=row_ind[i]
    return centroide



def calcul_u2_kmeans_approbation(p, nb_lancements=10):
    n=len(p)
    m=len(p[0])
    u2=float('inf') #on met infini pour trouver mieux dès la premiere itération 
    for _ in range(nb_lancements):
        #initialiser deux centroïdes aléatoirement
        centroide1=np.random.randint(2, size=m)
        centroide2=np.random.randint(2, size=m)
        #On évite que les deux centroïdes soient identiques (sinon tout le monde va dans le même cluster)
        while np.array_equal(centroide1, centroide2): #surtout si on a des pas beaucoup de candidats 
            centroide2=np.random.randint(2, size=m)
        changement=True
        while changement:
            #Étape 4: affecter chaque bulletin au cluster dont le centroïde est le plus proche
            cluster1=[] #pr centroide1
            cluster2=[] #pr centroide2
            for i in range(n):
                d1=distance_hamming(centroide1, p[i]) #on calcule la distance entre chaque bulletin et les 2 centroides
                d2=distance_hamming(centroide2, p[i])
                if d1<=d2:
                    cluster1.append(p[i])              #et on les ajoute dans le cluster le + proche 
                else:
                    cluster2.append(p[i])
            
            
            if len(cluster1)>0:
                nouveau_c1=trouve_centroide_approbation(cluster1)
            else:
                nouveau_c1=centroide1   #car si le cluster est vide ça va planter 
            if len(cluster2)>0:
                nouveau_c2=trouve_centroide_approbation(cluster2)
            else:
                nouveau_c2=centroide2
            if np.array_equal(nouveau_c1, centroide1) and np.array_equal(nouveau_c2, centroide2): #si il n'y a pas de changement entre le nv centroide et l'ancien alors c'est bon on a fini 
                changement=False
            else:
                centroide1=nouveau_c1 #sinon on continue 
                centroide2=nouveau_c2
        cout=0
        for bulletin in cluster1:
            cout+=distance_hamming(centroide1, bulletin)
        for bulletin in cluster2:
            cout+=distance_hamming(centroide2, bulletin)     # on somme tt les distances pour avoir notre u2
        if cout<u2:
            u2=cout
    return u2

#globalement la même chose que pour les approbations juste il faut permuter et utiliser la distance de Spearman 
def calcul_u2_kmeans_ordres(p, nb_lancements=10):
    n=len(p)
    m=len(p[0])
    u2=float('inf') #on met infini pour trouver mieux dès la premiere itération 
    for _ in range(nb_lancements):
        #initialiser deux centroïdes aléatoirement
        centroide1=np.random.permutation(2, size=m)
        centroide2=np.random.permutation(2, size=m)
        #On évite que les deux centroïdes soient identiques (sinon tout le monde va dans le même cluster)
        while np.array_equal(centroide1, centroide2): #surtout si on a des pas beaucoup de candidats 
            centroide2=np.random.permutation(2, size=m)
        changement=True
        while changement:
            #Étape 4: affecter chaque bulletin au cluster dont le centroïde est le plus proche
            cluster1=[] #pr centroide1
            cluster2=[] #pr centroide2
            for i in range(n):
                d1=distance_spearman(centroide1, p[i]) #on calcule la distance entre chaque bulletin et les 2 centroides
                d2=distance_spearman(centroide2, p[i])
                if d1<=d2:
                    cluster1.append(p[i])              #et on les ajoute dans le cluster le + proche 
                else:
                    cluster2.append(p[i])
            
            
            if len(cluster1)>0:
                nouveau_c1=trouve_centroide_ordres(cluster1)
            else:
                nouveau_c1=centroide1   #car si le cluster est vide ça va planter 
            if len(cluster2)>0:
                nouveau_c2=trouve_centroide_ordres(cluster2)
            else:
                nouveau_c2=centroide2
            if np.array_equal(nouveau_c1, centroide1) and np.array_equal(nouveau_c2, centroide2): #si il n'y a pas de changement entre le nv centroide et l'ancien alors c'est bon on a fini 
                changement=False
            else:
                centroide1=nouveau_c1 #sinon on continue 
                centroide2=nouveau_c2
        cout=0
        for bulletin in cluster1:
            cout+=distance_spearman(centroide1, bulletin)
        for bulletin in cluster2:
            cout+=distance_spearman(centroide2, bulletin)     # on somme tt les distances pour avoir notre u2
        if cout<u2:
            u2=cout
    return u2