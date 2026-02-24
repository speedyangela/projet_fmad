
import numpy as np
import random

#QUESTION 1

def generer_profil_approbation(n,m,p): 
    #n: Nombre de votants (doit être pair)
    #m: Nombre de candidats 
    #p: Niveau de polarisation de l'élection (doit être entre 0 et 1)
    if n % 2 != 0:
        raise ValueError("Le nombre de votants doit être pair")
    if p < 0 or p > 1:
        raise ValueError("Le niveau de polarisation doit être entre 0 et 1")
    a=np.random.randint(2,size=m)#on génère un bulletin de vote au hasard 
    a_oppose=1-a #on génère le bulletin de vote opposé à a
    profil=[] 
    nb_a_oppose=int(p*(n/2)) 
    #si p=1, il y a n/2 bulletins a et n/2 bulletins a_oppose
    #donc on fait une règle de trois pour trouver il y a combien de bulletins a_oppose avec la valeur de p
    #(quand p=0, on a bien n bulletins a et 0 a_oppose)
    nb_a=n-nb_a_oppose  
    for i in range(nb_a):
        profil.append(a)     #on ajoute au profil tout les bulletins a...
    for i in range(nb_a_oppose):
        profil.append(a_oppose)    #...et a_oppose
    np.random.shuffle(profil) #on mélange les bulletins pour éviter tout les a d'abord et tout les a_oppose à la suite 
    return np.array(profil) #on renvoie un tableau np car plus facile à manipuler 

#QUESTION 2

def generer_profil_ordres(n,m,p): #mêmes arguments que q1
    if n % 2 != 0:
        raise ValueError("Le nombre de votants doit être pair")
    if p < 0 or p > 1:
        raise ValueError("Le niveau de polarisation doit être entre 0 et 1")
    
    o=np.random.permutation(m) #on génère un ordre de préférence au hasard
    
    o_oppose=np.zeros(m, dtype=int) #on initialise o_oppose
    for i in range(m):  #on génère l'ordre de préférence opposé à o
        candidat=o[i] 
        i_oppose=(m-1)-i    #on applique la formule du sujet, en python on commence l'indice à 0 à m-1 donc c normal le décalage par rapport à la formule du sujet  
        o_oppose[i_oppose]=candidat
    #sinon on aurait juste pu faire o_oppose=o[::-1] 
    profil=[]
    nb_o_oppose=int(p*(n/2)) #même règle de trois que q1 pour trouver le nombre de bulletins o_oppose
    nb_o=n-nb_o_oppose
    for i in range(nb_o):
        profil.append(o)
    for i in range(nb_o_oppose):                         #même chose que q1
        profil.append(o_oppose)
    np.random.shuffle(profil)
    return np.array(profil)


#VERSIONS AVEC BRUIT (pour avoir + de 2 bulletins distincts)

#question 1
#VERSIONS AVEC BRUIT (pour avoir + de 2 bulletins distincts)

def generer_profil_approbation_bruit(n,m,p,bruit=0.1): 
    #mêmes arguments que generer_profil_approbation + bruit=proba de changer un 0 ou 1
    if n % 2 != 0:
        raise ValueError("Le nombre de votants doit être pair")
    if p < 0 or p > 1:
        raise ValueError("Le niveau de polarisation doit être entre 0 et 1")
    a=np.random.randint(2,size=m) #on génère un bulletin de vote au hasard 
    a_oppose=1-a #on génère le bulletin opposé à a
    profil=[] 
    nb_a_oppose=int(p*(n/2)) #même règle de trois que q1
    nb_a=n-nb_a_oppose  
    for i in range(nb_a):
        bulletin=a.copy() #on part du bulletin a , on copy pour bien que ça pointe bien vers deux tableaux différents 
        for j in range(m): #pour chaque candidat
            if random.random()<bruit: #avec proba bruit  (0 devient 1 et inversement)
                bulletin[j]=1-bulletin[j]
        profil.append(bulletin) #on ajoute ce bulletin légèrement modifié
    for i in range(nb_a_oppose):
        bulletin=a_oppose.copy() #on part du bulletin opposé
        for j in range(m):
            if random.random()<bruit:
                bulletin[j]=1-bulletin[j]
        profil.append(bulletin)
    np.random.shuffle(profil) #on mélange comme en q1
    return np.array(profil)

def generer_profil_ordres_bruit(n,m,p,nb_swaps=2):
    #mêmes arguments que generer_profil_ordres + nb_swaps=nb de swaps aléatoires par bulletin
    if n % 2 != 0:
        raise ValueError("Le nombre de votants doit être pair")
    if p < 0 or p > 1:
        raise ValueError("Le niveau de polarisation doit être entre 0 et 1")
    o=np.random.permutation(m) #on génère un ordre de préférence au hasard
    o_oppose=np.zeros(m, dtype=int)
    for i in range(m): #on génère l'ordre opposé à o (comme en q2)
        candidat=o[i] 
        i_oppose=(m-1)-i
        o_oppose[i_oppose]=candidat
    profil=[]
    nb_o_oppose=int(p*(n/2)) #même règle de trois que q1
    nb_o=n-nb_o_oppose
    for i in range(nb_o):
        bulletin=o.copy() #on part de l'ordre o
        for _ in range(nb_swaps): #on fait nb_swaps échanges de 2 candidats pour ajouter du bruit
            pos1=random.randint(0,m-1) #on choisit 2 positions au hasard
            pos2=random.randint(0,m-1)
            bulletin[pos1],bulletin[pos2]=bulletin[pos2],bulletin[pos1] #on échange les candidats à ces positions
        profil.append(bulletin)
    for i in range(nb_o_oppose):
        bulletin=o_oppose.copy() #on part de l'ordre opposé
        for _ in range(nb_swaps):
            pos1=random.randint(0,m-1)
            pos2=random.randint(0,m-1)
            bulletin[pos1],bulletin[pos2]=bulletin[pos2],bulletin[pos1]
        profil.append(bulletin)
    np.random.shuffle(profil)
    return np.array(profil)