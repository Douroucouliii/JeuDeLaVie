import JeuDeLaVie
from tkinter import *
import time

lignes = 30
colonnes = 30

class VueJeuDeLaVie :
    
    def __init__(self, jeu):
        
        self.__jeu = jeu
        self.__lignes = lignes
        self.__colonnes = colonnes
        self.__isRunning = False
        self.__compteur = 0
        self.__stable = 0
        
        '''Création de la fenêtre'''
        
        self.__fenetre1 = Tk()
        self.__fenetre1.title("Options utilisateur")
        self.__fenetre1.geometry("500x100")
        
        '''On affiche l'interface utilisateur et on récupère le nombre de lignes et de colonnes entrées'''
        
        self.__label_ligne = Label(self.__fenetre1, text="Combien voulez-vous de lignes ? (max 30)")
        self.__label_ligne.grid(row=0,column=0)
        
        self.__saisie_ligne = Entry(self.__fenetre1,width=25)
        self.__saisie_ligne.grid(row=0,column=1)
        
        self.__label_colonne = Label(self.__fenetre1, text="Combien voulez-vous de colonnes ? (max 30)")
        self.__label_colonne.grid(row=1,column=0)
        
        self.__saisie_colonne = Entry(self.__fenetre1,width=25)
        self.__saisie_colonne.grid(row=1,column=1)    
        
        btn_valider = Button(self.__fenetre1, text="Valider", command=self.get_value)
        btn_valider.grid(row=2,column=0)
        
        self.__fenetre1.mainloop()
               
        '''Création de la deuxième fenêtre (celle avec le jeu)'''
        
        self.__fenetre2 = Tk()
        self.__fenetre2.title("Le jeu de la vie")
        self.__fenetre2.geometry("1920x1080")
        
        '''Création de la grille selon les valeurs inscrit par l'utilisateur'''
        
        self.__les_btns = []
        for i in range(self.__lignes) :
            une_ligne = []
            for j in range(self.__colonnes) :
                btn = Button(self.__fenetre2,width=4, height=1, bg="white")
                btn.grid(row=i,column=j)
                une_ligne.append(btn)
            self.__les_btns.append(une_ligne)
            '''On lance la boucle d'écoute des évenements'''
        self.lance()
                
        '''On crée les boutons et on les affiche à droite du jeu de la vie'''
        
        bouton_quitter = Button(self.__fenetre2, text='Quitter', command=self.quitter)
        bouton_quitter.grid(row=0,column=self.__colonnes)
        
        bouton_start = Button(self.__fenetre2, text='Start', command=lambda:self.mon_control(0))
        bouton_start.grid(row=1,column=self.__colonnes)
        
        boutton_stop = Button(self.__fenetre2, text='Stop', command=lambda:self.mon_control(1))
        boutton_stop.grid(row=2,column=self.__colonnes)
        
        boutton_clear = Button(self.__fenetre2, text='Clear', command=self.bouton_clear)
        boutton_clear.grid(row=3,column=self.__colonnes)   
        
        '''On crée le timer pour suivre les étapes'''
        
        self.__timer = Label(self.__fenetre2, text="Etape : "+str(self.__compteur))
        self.__timer.grid(row=4,column=self.__colonnes)
        
        self.__fenetre2.mainloop()
        
    def get_value(self):
        '''Méthode qui va récupérer les valeurs entrées par l'utilisateur et détruire la fenêtre d'utilisateur
        quand le bouton valider est appuyé.'''      
        self.__lignes = int(self.__saisie_ligne.get())
        self.__colonnes = int(self.__saisie_colonne.get())
        if self.__lignes > 30 :
            self.__lignes = 30
        if self.__colonnes > 30 :
            self.__colonnes = 30
        self.__fenetre1.destroy()
        
    def lance(self):
        '''Méthode qui ajoute une configuration à chaque boutons pour changer les valeurs dans la matrice et le background des boutons sur la grille tkinter'''
        for i in range(self.__lignes) :
            for j in range(self.__colonnes) : 
                self.__les_btns[i][j].config(command=self.change_bg_btns(i,j))
                
    def change_bg_btns(self, i, j):
        def change_bg():
            if self.__les_btns[i][j]['bg']=="white":
                self.__jeu.add_one_at_i_j(i,j)
                self.__les_btns[i][j].config(bg = "black")
            else :
                self.__jeu.add_zero_at_i_j(i,j)
                self.__les_btns[i][j].config(bg = "white")
        return change_bg
            
    def update_all_btns(self):
        '''Méthode qui change le background de touts les boutons selon les valeurs entrées dans la matrice'''
        for i in range(self.__lignes):
            for j in range(self.__colonnes):
                if self.__jeu.test_i_j(i,j):
                    self.__les_btns[i][j].config(bg = "white")
                else :
                    self.__les_btns[i][j].config(bg = "black")
                    
    def quitter(self):
        '''Méthode pour quitter l'application'''
        self.__isRunning = False
        self.__fenetre2.destroy()
    
    def mon_control(self, a):
        '''Méthode qui controle le changement d'état d'une variable afin de gérer les bouton start et stop'''
        if a==0 and not self.__isRunning:
            self.__isRunning = True
            self.bouton_start()
        elif a==1 and self.__isRunning:
            self.bouton_stop()
    
    def bouton_start(self):
        '''Tant que l'utilisateur ne demande pas de stopper la simulation, la matrice avance d'une étape, on actualise toutes les cases
        de la grilles sur tkinter, on demande au programme d'attendre 1 sec et on ajoute 1 au compteur timer'''
        while self.__isRunning :
            time.sleep(0.5)
            a = self.__jeu.cherche_cycle(1)
            self.update_all_btns()
            self.__compteur += 1
            self.__timer.config(text = "Etape : "+ str(self.__compteur))
            self.__fenetre2.update()
            if a == 1 and self.__stable == 0:
                '''Si la structure est stable, on fait appel à la fonction struct_stable() pour demander à l'utilisateur s'il souhaite stopper la simulation'''
                self.struct_stable()
    
    def struct_stable(self):
        '''méthode qui affiche le label de saisie pour l'utilisateur et récupère son choix grâce à la méthode choix()'''
        self.__isRunning = False
        self.__label_stable = Label(self.__fenetre2, text="Le jeu a détecté une structure stable, voulez-vous continuer ? Oui/Non")
        self.__label_stable.grid(row=5,column=self.__colonnes) 
        self.__saisie_stable = Entry(self.__fenetre2,width=25)
        self.__saisie_stable.grid(row=6,column=self.__colonnes)
        self.__boutton_valider_choix = Button(self.__fenetre2, text='Valider')
        self.__boutton_valider_choix.grid(row=7,column=self.__colonnes)
        self.__boutton_valider_choix.config(command = self.choix)
    
    def choix(self):
        choix = self.__saisie_stable.get()
        if choix == "oui" or choix == "Oui" :
            self.__isRunning = True
            self.__stable = 1
            self.bouton_start()
        elif choix == "non" or choix == "Non" :
            self.__fenetre2.destroy()
    
    def bouton_stop(self):
        '''Quand l'utilisateur appuie sur le bouton stop, on stop la boucle'''
        self.__isRunning = False
        
    def bouton_clear(self):
        '''Quand l'utilisateur appuie sur le bouton clear, la matrice se reinitialise, la grille de bouton et le timer aussi'''
        self.__jeu.reinitialise_mat()
        self.update_all_btns()
        self.__compteur = 0
        self.__timer.config(text = "Etape : "+ str(self.__compteur))
    
if __name__ == '__main__' :
    jeu = JeuDeLaVie.JeuDeLaVie(lignes, colonnes)
    mon_appli = VueJeuDeLaVie(jeu)
