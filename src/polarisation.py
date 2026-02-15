#QUESTION 3

def calcul_dist_approbation(profil):
    n=len(profil)  #nombre de votants 
    m=len(profil[0]) #nombre de candidats
    distances={}
    #on parcourt les paires de candidats(k,l)
    for k in range(m):
        for l in range(k+1,m): #on commence à k+1 pour pas comparer un candidat avec lui-même
            n_kl=0 #nombre de prsn qui preferent k à l
            n_lk=0 #// l à k
            for v in range(n): #on analyse chaque bulletin 
                bulletin=profil[v]
                if bulletin[k]==1 and bulletin[l]==0: #si le votant approuve k et pas l
                    n_kl+=1
                elif bulletin[k]==0 and bulletin[l]==1: #// l et pas k
                    n_lk+=1
            d_kl=abs(n_kl-n_lk) 
            distances[(k,l)]=d_kl #on stocke la distance dans le dico associé au comparatif k et l
    return distances

def calcul_dist_ordres(profil):
    n=len(profil)  #nombre de votants 
    m=len(profil[0]) #nombre de candidats
    distances={}
    for k in range(m):
        for l in range(k+1,m): #on commence à k+1 pour pas comparer un candidat avec lui-même
            n_kl=0 #nombre de prsn qui preferent k à l
            n_lk=0 #// l à k
            for v in range(n): #on analyse chaque bulletin 
                bulletin=profil[v].tolist() #on convertit le tableau np en liste pour pouvoir utiliser .index() avec les candidats
                position_k=bulletin.index(k) #position de k dans le bulletin
                position_l=bulletin.index(l) #position de l dans le bulletin
                if position_k<position_l: #celui qui a le + petit index est le mieux classé 
                    n_kl+=1
                else: 
                    n_lk+=1
            d_kl=abs(n_kl-n_lk) 
            distances[(k,l)]=d_kl                       #même chose que méthode précédente 
    return distances

#QUESTION 5
def calcul_mesure_pola_approbation(p):
    n=len(p)  
    m=len(p[0])
    distances=calcul_dist_approbation(p) #on utilise la distance d'approbation 
    denominateur=((m*(m-1))/2)*n #2 parmis m=m!/(2!(m-2)!)=m(m-1)(m-2)!/(m-2)!2
    somme=0 
    for d_kl in distances.values():
        x=(n-d_kl)/denominateur #on applique la formule du poly pour chaque k,l  de notre dico 
        somme+=x # on somme tout pour avoir la formule 
    return somme


def calcul_mesure_pola_ordres(p):
    n=len(p)  
    m=len(p[0])
    distances=calcul_dist_ordres(p) #on utilise la distance d'ordre
    denominateur=((m*(m-1))/2)*n #2 parmis m=m!/(2!(m-2)!)=m(m-1)(m-2)!/(m-2)!2
    somme=0 
    for d_kl in distances.values():
        x=(n-d_kl)/denominateur #on applique la formule du poly pour chaque k,l  de notre dico 
        somme+=x # on somme tout pour avoir la formule 
    return somme