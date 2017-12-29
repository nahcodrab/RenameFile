import os
import string
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Action:
    '''
    Création de la classe action
    nomdurepertoire
    regle
    constructeur
    getters/setters
    simule qui affiche à l’écran le nom du fichier original et celui qu’il aura après renommage
    __str__
    '''
    def __init__(self, nom_repertoire, Regle):
        self.nom_repertoire = nom_repertoire
        self.Regle = Regle
    def get_nom_repertoire(self):
        return self.nom_repertoire
    def set_nom_repertoire(self, nom_repertoire):
        self.nom_repertoire = nom_repertoire
    def get_Regle(self):
        return self.Regle
    def set_Regle(self, Regle):
        self.Regle = Regle
    def __str__(self):
        return "Nom du répertoire : '" + self.nom_repertoire + "' \n" + self.Regle.__str__()
    def entier_string(self, int):
        string = ""
        while int > 0:
            int, retenue = divmod(int - 1, 26)
            string = chr(65 + retenue) + string
        return string
    def string_entier(self, alphabet):
        num = 0
        for c in alphabet:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num
    def simulation(self):
        if self.Regle.get_extension() == '':
            nom_fichier_originals = [fn for fn in os.listdir(self.nom_repertoire)]
        else:
            nom_fichier_originals = [fn for fn in os.listdir(self.nom_repertoire)
                                   if fn.endswith(tuple(self.Regle.get_extension()))]

        nom_fichier_renommes = []

        if self.Regle.get_Dep_init() == '' or self.Regle.get_initiation() == '':
            Dep_init = 0
        elif self.Regle.get_initiation() == 'Lettre':
            Dep_init = self.string_entier(self.Regle.get_Dep_init())
        elif self.Regle.get_initiation() == 'Nombre':
            number = self.Regle.get_Dep_init()
            if number.isdigit():
                Dep_init = int(number)
            else:
                Dep_init = 0

        for nom_fichier_original in nom_fichier_originals:
            nom_fichier_renomme, extension = os.path.splitext(nom_fichier_original)

            if isinstance(self.Regle.get_nom_fichier(), str):
                nom_fichier_renomme = self.Regle.get_nom_fichier()

            if self.Regle.get_prefix() != '':
                nom_fichier_renomme = self.Regle.get_prefix() + nom_fichier_renomme

            if self.Regle.get_suffix() != '':
                nom_fichier_renomme = nom_fichier_renomme + self.Regle.get_suffix()

            Dep_init += 1

            if self.Regle.get_initiation() == '':
                initiation = ''
            elif self.Regle.get_initiation() == 'Lettre':
                initiation = self.entier_string(Dep_init)
            elif self.Regle.get_initiation() == 'Nombre':
                initiation = '{0}'.format(str(Dep_init).zfill(3))

            if initiation != '':
                nom_fichier_renomme = initiation + nom_fichier_renomme

            nom_fichier_renomme = nom_fichier_renomme + extension

            nom_fichier_renommes.append(nom_fichier_renomme)

        return nom_fichier_originals, nom_fichier_renommes

class bloqueTemplate:
    def __init__(self, master):
        self.master = master
        self.name_entry = Entry(self.master)
        self.name_entry.configure(width = 40)
        self.name_entry.place(x = 150, y = 55)

        self.initiation_label = Label(self.master, text = 'Amorce')
        self.initiation_label.place(x = 35, y = 125)
        self.combo_var = StringVar()
        self.combo_var.set('Aucune')
        self.initiation_box = ttk.Combobox(self.master, textvariable = self.combo_var, state = 'readonly', values = ['Aucune', 'Lettre', 'Chiffre'])
        self.initiation_box.configure(width = 8)
        self.initiation_box.place(x = 25, y = 150)
        self.MAPPING = {'Aucune' : '', 'Lettre' : 'letter', 'Chiffre' : 'number'}

        self.Dep_init_label = Label(self.master, text = 'A partir de')
        self.Dep_init_label.place(x = 27, y = 225)
        self.Dep_init_entry = Entry(self.master)
        self.Dep_init_entry.configure(width = 9)
        self.Dep_init_entry.place(x = 27, y = 250)
        
        self.prefix_label = Label(self.master, text = 'Préfixe')
        self.prefix_label.place(x = 140, y = 125)
        self.prefix_entry = Entry(self.master)
        self.prefix_entry.configure(width = 10)
        self.prefix_entry.place(x = 129, y = 150)
        
        self.nom_fichier_label = Label(self.master, text = 'Nom du fichier')
        self.nom_fichier_label.place(x = 225, y = 125)

        self.radio_var = StringVar()
        self.radio_var.set('original')

        self.nom_fichier_rb1 = ttk.Radiobutton(self.master, text = 'Nom original', variable = self.radio_var, value = 'original')
        self.nom_fichier_rb2 = ttk.Radiobutton(self.master, variable = self.radio_var, value = 'renommer')
        self.nom_fichier_rb1.place(x = 215, y = 150)
        self.nom_fichier_rb2.place(x = 215, y = 180)
        self.nom_fichier_entry = Entry(self.master)
        self.nom_fichier_entry.configure(width = 12)
        self.nom_fichier_entry.place(x = 235, y = 180)

        self.suffix_label = Label(self.master, text = 'Postfixe')
        self.suffix_label.place(x = 350, y = 125)
        self.suffix_entry = Entry(self.master)
        self.suffix_entry.configure(width = 10)
        self.suffix_entry.place(x = 342, y = 150)

        self.extension_label = Label(self.master, text = 'Extension concernée')
        self.extension_label.place(x = 440, y = 125)
        self.extension_entry = Entry(self.master)
        self.extension_entry.configure(width = 20)
        self.extension_entry.place(x = 447, y = 150)

        self.image = PhotoImage(file ='logo.gif')
        self.image_label = Label(self.master, image = self.image)
        self.image_label.place(x = 450, y = 20)

    def get_Regle(self):
        initiation = self.MAPPING[self.initiation_box.get()]
        Dep_init = self.Dep_init_entry.get()
        prefix = self.prefix_entry.get()
        if self.radio_var.get() == 'original':
            nom_fichier = True
        else:
            nom_fichier = self.nom_fichier_entry.get()
        suffix = self.suffix_entry.get()
        extension = self.extension_entry.get().split(',')
        
        return Regle(initiation, Dep_init, prefix, nom_fichier, suffix, extension)

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.combo_var.set('Aucune')
        self.Dep_init_entry.delete(0, END)
        self.prefix_entry.delete(0, END)
        self.radio_var.set('original')
        self.nom_fichier_entry.delete(0, END)
        self.suffix_entry.delete(0, END)
        self.extension_entry.delete(0, END)
        self.name_entry.focus_set()

class renommerbloque(bloqueTemplate):
    def __init__(self, master):
        bloqueTemplate.__init__(self, master)
        self.title_label = Label(self.master, text = 'Renommer en lots')
        self.title_label.place(x = 225, y = 15)
        self.name_label = Label(self.master, text = 'Nom du répertoire')
        self.name_label.place(x = 25, y = 53)
        self.renommer_button = Button(self.master, text = 'Renommer', command = self.renommer)
        self.renommer_button.place(x = 450, y = 225)
    def renommer(self):
        nom_repertoire = self.name_entry.get()
        if os.path.isdir(nom_repertoire):
            Regle = self.get_Regle()
            renommer_action = renommer(nom_repertoire, Regle)
            self.nouvelleFenetre = Toplevel(self.master)
            self.nouvelleFenetre.title('Vérification')
            self.nouvelleFenetre.minsize(width = 375, height = 300)
            self.simulation_bloque = Simulationbloque(self.nouvelleFenetre, renommer_action, self)
        else:
            messagebox.showinfo('Information', "Vérifiez le chemin n'existe pas")

class renommer(Action):
    def __init__(self, nom_repertoire, Regle):
        Action.__init__(self, nom_repertoire, Regle)
    def renommer_files(self):
        original, renommerd = self.simulation()
        a = 0
        for i in range(len(original)):
            os.renommer(os.path.join(self.nom_repertoire, original[i]),
                      os.path.join(self.nom_repertoire, renommerd[i]))
            a += 1
        return a

class Regle:
    def __init__(self, initiation, Dep_init, prefix, nom_fichier, suffix, extension, Regle_name = ''):
        self.initiation = initiation
        self.Dep_init = Dep_init
        self.prefix = prefix
        self.nom_fichier = nom_fichier
        self.suffix = suffix
        extension = [x.strip() for x in extension]
        self.extension = extension
        self.Regle_name = Regle_name

    def get_initiation(self):
        return self.initiation
    def set_initiation(self, initiation):
        self.initiation = initiation
    def get_Dep_init(self):
        return self.Dep_init
    def set_Dep_init(self, Dep_init):
        self.Dep_init = Dep_init
    def get_prefix(self):
        return self.prefix
    def set_prefix(self, prefix):
        self.prefix = prefix
    def get_nom_fichier(self):
        return self.nom_fichier
    def set_nom_fichier(self, nom_fichier):
        self.nom_fichier = nom_fichier
    def get_suffix(self):
        return self.suffix
    def set_suffix(self, suffix):
        self.suffix = suffix
    def get_extension(self):
        return self.extension
    def set_extension(self, extension):
        self.extension = extension
    def get_nom_regle(self):
        return self.Regle_name
    def set_nom_regle(self, Regle_name):
        self.Regle_name = Regle_name
    def __str__(self):
        string = "Initiation : '" + self.initiation + "' \n" \
                 "Depuis l'init : '" + self.Dep_init + "' \n" \
                 "Prefix : '" + self.prefix + "' \n" \
                 "Nom du fichier : '" + str(self.nom_fichier) + "' \n" \
                 "Suffix : '" + self.suffix + "' \n" \
                 "Nom de la règle : '" + self.Regle_name + "' \n" \
                 "Extension : '"
        i = 1
        for e in self.extension:
            string += e
            if i < len(self.extension):
                string += ', '
            i += 1
        string += "'"
        return string

class Reglebloque(bloqueTemplate):
    def __init__(self, master):
        bloqueTemplate.__init__(self, master)
        self.title_label = Label(self.master, text = 'Créer une règle')
        self.title_label.place(x = 225, y = 15)
        self.name_label = Label(self.master, text = 'Nom de la règle')
        self.name_label.place(x = 55, y = 53)
        self.creer_button = Button(self.master, text = 'Créer', command = self.creer)
        self.creer_button.place(x = 450, y = 225)
    def creer(self):
        Regle = self.get_Regle()
        Regle.set_nom_regle(self.name_entry.get())
        Regle_list = ListeRegle([])
        Regle_list.add_Regle('RenommageFichier.ini', Regle)
        self.master.destroy()
        messagebox.showinfo('Règle enregistrée', 'Règle enregistrée')

class ListeRegle:
    '''
    regles
    constructeur
    getters/setters
    charger()
    sauvegarder()
    __str__
    '''
    def __init__(self, Regles):
        self.Regles = Regles
    def get_Regles(self):
        return self.Regles
    def set_Regles(self, Regles):
        self.Regles = Regles
    def __str__(self):
        string = ''
        for r in self.Regles:
            string += r.__str__() + '\n \n'
        return string

    def sauvegarder_tous(self, nom_fichier):
        with open(nom_fichier, 'w', encoding = 'utf-8') as file:
            string = ''
            for r in self.Regles:
                string += r.get_initiation() + ',' + r.get_Dep_init() + ',' + r.get_prefix() + ',' + \
                          str(r.get_nom_fichier()) + ',' + r.get_suffix() + ',' + r.get_nom_regle() + '/'
                i = 1
                for e in r.get_extension():
                    string += e
                    if i < len(r.get_extension()):
                        string += ','
                    i += 1
                string += '\n'
            file.write(string)

    def sauvegarder(self, nom_fichier, Regle):
        with open(nom_fichier, 'a', encoding='utf-8') as file:
            string = Regle.get_initiation() + ',' + Regle.get_Dep_init() + ',' + Regle.get_prefix() + ',' + \
                      str(Regle.get_nom_fichier()) + ',' + Regle.get_suffix() + ',' + Regle.get_nom_regle() + '/'
            i = 1
            for e in Regle.get_extension():
                string += e
                if i < len(Regle.get_extension()):
                    string += ','
                i += 1
            string += '\n'
            file.write(string)

    def charger(self, nom_fichier):
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            split = line.split('/')
            nom_fichier_attributes = split[0].split(',')
            extension = split[1].split(',')
            if nom_fichier_attributes[3] == 'True':
                nom_fichier_attributes[3] = True
            elif nom_fichier_attributes[3] == 'False':
                nom_fichier_attributes[3] = False

            Regle = Regle(nom_fichier_attributes[0], nom_fichier_attributes[1], nom_fichier_attributes[2],
                        nom_fichier_attributes[3], nom_fichier_attributes[4], extension, nom_fichier_attributes[5])
            self.Regles.append(Regle)

    def add_Regle(self, nom_fichier, Regle):
        self.Regles.append(Regle)
        self.sauvegarder(nom_fichier, Regle)

class ListeReglebloque:
    def __init__(self, master, renommer_bloque):
        self.master = master
        self.renommer_bloque = renommer_bloque
        self.prompt_label = Label(self.master, text = 'Sélectionnez une règle :')
        self.prompt_label.place(x = 50, y = 10)
        self.Regle_list = ListeRegle([])
        self.Regle_list.charger('RenommageFichier.ini')
        self.Regles = self.Regle_list.get_Regles()
        self.radio_var = IntVar()
        i = 0
        a = 40

        for Regle in self.Regles:
            ttk.Radiobutton(self.master, text = Regle.get_nom_regle(), variable = self.radio_var, value = i).place(x = 50, y = j)
            i += 1
            a += 20

        self.appliquer_button = Button(self.master, text = 'Appliquer', command = self.appliquer)
        self.appliquer_button.place(relx = 0.25, rely = 0.9)
        self.close_button = Button(self.master, text = 'Annuler', command = self.close)
        self.close_button.place(relx = 0.5, rely = 0.9)

    def appliquer(self):
        Regle = self.Regles[self.radio_var.get()]
        MAPPING = {'' : 'Aucune', 'letter' : 'Lettre', 'number' : 'Chiffre'}
        self.renommer_bloque.combo_var.set(MAPPING[Regle.get_initiation()])
        self.renommer_bloque.Dep_init_entry.delete(0, END)
        self.renommer_bloque.Dep_init_entry.insert(0, Regle.get_Dep_init())
        self.renommer_bloque.prefix_entry.delete(0, END)
        self.renommer_bloque.prefix_entry.insert(0, Regle.get_prefix())

        if isinstance(Regle.get_nom_fichier(), str):
            self.renommer_bloque.radio_var.set('renommer')
            self.renommer_bloque.nom_fichier_entry.delete(0, END)
            self.renommer_bloque.nom_fichier_entry.insert(0, Regle.get_nom_fichier())
        else:
            self.renommer_bloque.radio_var.set('original')
            self.renommer_bloque.nom_fichier_entry.delete(0, END)

        self.renommer_bloque.suffix_entry.delete(0, END)
        self.renommer_bloque.suffix_entry.insert(0, Regle.get_suffix())
        string = ''
        i = 1
        for e in Regle.get_extension():
            string += e
            if i < len(Regle.get_extension()):
                string += ','
            i += 1
        self.renommer_bloque.extension_entry.delete(0, END)
        self.renommer_bloque.extension_entry.insert(0, string)

        self.master.destroy()

    def close(self):
        self.master.destroy()

class Simulationbloque:
    def __init__(self, master, renommer_action, renommer_bloque):
        self.master = master
        self.renommer_action = renommer_action
        self.renommer_bloque = renommer_bloque
        self.prompt_label = Label(self.master, text = 'Voulez vous renommer ces fichiers ?')
        self.prompt_label.place(x = 50, y = 10)
        self.original, self.renommerd = self.renommer_action.simulation()
        a = 40
        for i in range(len(self.original)):
            Label(self.master, text = self.original[i] + ' -> ' + self.renommerd[i]).place(x = 50, y = a)
            a += 20

        self.renommer_button = Button(self.master, text = 'Oui', command = self.renommer)
        self.renommer_button.place(relx = 0.4, rely = 0.9)
        self.close_button = Button(self.master, text = 'Non', command = self.close)
        self.close_button.place(relx = 0.5, rely = 0.9)

    def renommer(self):
        seen = set()
        duplicates = set(x for x in self.renommerd if x in seen or seen.add(x))
        if len(duplicates) == 0:
            nb_files = self.renommer_action.renommer_files()
            self.master.destroy()
            messagebox.showinfo('Fichiers renommés', 'Nombre de fichiers renommés : ' + str(nb_files))
            self.renommer_bloque.clear_form()
        else:
            messagebox.showinfo('Avertissement', 'Opération impossible : \n'
                                                 'Un ou plusieurs fichiers ont le même nom et la même extension')

    def close(self):
        self.master.destroy()

class Toolbar:
    def __init__(self, master, renommer_bloque):
        self.master = master
        self.renommer_bloque = renommer_bloque

        self.menu_bar = Menu(self.master)
        self.Regle_menu = Menu(self.menu_bar, tearoff = 0)
        self.Regle_menu.add_command(label = 'Lister', command = self.open_Regle_list_bloque)
        self.Regle_menu.add_command(label = 'Créer', command = self.open_Regle_bloque)
        self.menu_bar.add_cascade(label = 'Règles', menu = self.Regle_menu)
        #self.menu_bar.add_command(label = '?', command = self.open_about)

        self.master.config(menu = self.menu_bar)

    def open_Regle_list_bloque(self):
        self.nouvelleFenetre_rl = Toplevel(self.master)
        self.nouvelleFenetre_rl.title('Liste des règles')
        self.nouvelleFenetre_rl.minsize(width = 300, height = 300)
        self.Regle_list_bloque = ListeReglebloque(self.nouvelleFenetre_rl, self.renommer_bloque)

    def open_Regle_bloque(self):
        self.nouvelleFenetre_r = Toplevel(self.master)
        self.nouvelleFenetre_r.title('Créer une règle')
        self.nouvelleFenetre_r.resizable(width = False, height = False)
        self.nouvelleFenetre_r.minsize(width = 600, height = 300)
        self.Regle_bloque = Reglebloque(self.nouvelleFenetre_r)

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title('Renommage de Fichier')
        self.master.resizable(width = False, height = False)
        self.master.minsize(width = 600, height = 300)
        self.renommer_bloque = renommerbloque(self.master)
        self.toolbar = Toolbar(self.master, self.renommer_bloque)


def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == '__main__':
    main()
