class JeuDeLaVie:

    def __init__(self, nblignes, nbcolonnes):
        self.__nblignes = nblignes
        self.__nbcolonnes = nbcolonnes
        self.__les_mat = []
        self.__mat = []
        for i in range(nblignes):
            ligne=[]
            for j in range(nbcolonnes):
                ligne.append(0)
            self.__mat.append(ligne)
        
    def add_one_at_i_j(self, i, j):
        '''Méthode qui met la valeur 1 aux coordonnées i,j de la matrice. Elle nous permet d'initialiser les valeurs quand l'utilisateur
        clique sur les cases de la grille de tkinter'''
        self.__mat[i][j] = 1
        
    def add_zero_at_i_j(self, i, j):
        '''Méthode qui met la valeur 0 aux coordonnées i,j de la matrice. Elle nous permet d'initialiser les valeurs quand l'utilisateur
        clique sur les cases de la grille de tkinter'''
        self.__mat[i][j] = 0
        
    def afficher(self):
        '''Méthode pour afficher la matrice actuel (pratique pour aider à résoudre des erreurs)'''
        print(self.__mat)
        
    def test_i_j(self, i, j):
        '''Méthode qui teste la matrice en i,j , elle renvoie True sur la valeur est 0 et False si la valeur est 1'''
        if self.__mat[i][j] == 0:
            return True
        else :
            return False
        
    def reinitialise_mat(self):
        '''Reinitialise toutes les valeurs de la matrice à 0'''
        for i in range(self.__nblignes):
            for j in range(self.__nbcolonnes):
                self.__mat[i][j] = 0
    
    def est_valide(self,i,j):
        return 0<=i<self.__nblignes and 0<=j<self.__nbcolonnes
    def nb_voisines_vivantes(self,i,j):
        cellules_vivantes = 0
        for l in range(i-1,i+2):
            for c in range(j-1,j+2):
                if self.est_valide(l,c) and (i,j) != (l,c) and self.__mat[l][c] == 1 :
                    cellules_vivantes+=1
        return cellules_vivantes

    def etape(self):
        self.__les_mat.append(self.__mat)
        new_mat = []
        for i in range(self.__nblignes):
            ligne =[]
            for j in range(self.__nbcolonnes):
                voisines_vivantes = self.nb_voisines_vivantes(i,j)
                if voisines_vivantes == 3 or (voisines_vivantes == 2 and self.__mat[i][j] == 1) :
                    ligne.append(1)
                else :
                    ligne.append(0)
            new_mat.append(ligne)
        self.__mat = new_mat
        
    def cherche_cycle(self,n):
        nombre_cycle = 0
        m = self.__mat
        while (nombre_cycle < n):
            nombre_cycle += 1
            self.etape()
            if m == self.__mat :
                return nombre_cycle
        return -1

