#imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def Kmeans(X, k):
	n = X.shape[0]
	centers = X[np.random.choice(n, k, replace = False)] #Choix de trois points aléatoires de référence
	plus_proche = np.zeros(n).astype(int) #Créer une liste de 0 de la taille de notre jeu de données

	while True:
		#Stocker la valeur de notre précédente liste pour la comparer avec la nouvelle qui sera générée en sortie
		ancienne_plus_proche = plus_proche.copy() 
		print(plus_proche)
		#Récupération de la distance entre les coordonnées des donnérd et celles des points de référence avec la méthode cdist
		distances = cdist(X, centers) 
		#Lister les points de référence les plus proches pour chaque donnée
		plus_proche = np.argmin(distances, axis = 1) 

		for i in range(k):
			#Changer ses coordonnées à celles de la moyenne des coordonnées des données les plus proches
			centers[i, :] = X[plus_proche == i].mean(axis = 0)
    
    	#Si les coordonnées de la nouvelle liste est identique à celle de la précédente itération, quitter la boucle
		if all(plus_proche == ancienne_plus_proche):
			break
	return(plus_proche, centers)

#Test de la fonction
X = np.random.random((20 , 2)) #Génération d'un jeu de données aléatoire
labels, centers = Kmeans(X, 4)
print(labels)
print(centers)
plt.scatter(X[: , 0], X[: , 1]) #Visualisation des données