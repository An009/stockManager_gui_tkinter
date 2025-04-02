from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



dict_oui_non = { False: "Non", True: "Oui"}

class Produit:

    def __init__(self, reference: str, designation: str, prixU: float, tva: float, disponibilite: bool) -> None:
        self.__reference = str(reference)
        self.__designation = str(designation)
        self.__prixU = float(prixU)
        self.__tva = float(tva)
        self.__disponibilite = bool(disponibilite)

    def get_reference(self) -> str:
        return self.__reference
        
    def get_designation(self) -> str:
        return self.__designation

    def set_designation(self, designation: str) -> None:
        self.__designation = str(designation)
    
    def get_prix_u(self) -> float:
        return self.__prixU

    def set_prix_u(self, prixU: float) -> None:
        self.__prixU = float(prixU)

    def get_tva(self) -> float:
        return self.__tva

    def set_tva(self, tva: float) -> None:
        self.__tva = float(tva)

    def est_disponible(self) -> bool:
        return self.__disponibilite

    def set_disponibilite(self, disponibilite: bool) -> None:
        self.__disponibilite = bool(disponibilite)

    def __str__(self) -> str:
        ch = "\n"
        ch += "Référence: {0}".format(self.get_reference()) + "\n"
        ch += "Désignation: {0}".format(self.get_designation()) + "\n"
        ch += "Prix Unitaire: {0}".format(self.get_prix_u()) + "DH\n"
        ch += "TVA: {0}".format(self.get_tva()) + "%\n"
        ch += "Disponibilité: {0}".format(dict_oui_non.get(self.est_disponible())) + "\n"
        ch += "\n"
        return ch

    def __eq__(self, __o: object) -> bool:
        return type(__o) == Produit and self.get_reference() == __o.get_reference()
    
    def __repr__(self) -> str:
        return f"{self.get_reference()};{self.get_designation()};{self.get_prix_u()};{self.get_tva()};{self.est_disponible()}"
    
    @classmethod
    def depuis_list(cls,donnes:list):
        reference , designation , prix , tva , disponibilite = donnes
        if disponibilite == 'True' :
            disponibilite = True
        else :
            disponibilite = False
        return cls(reference , designation , float(prix) , float(tva) , disponibilite)


class Stock:

    def __init__(self, nom: str, adresse: str, telephone: str) -> None:
        self.__nom = nom
        self.__adresse = adresse
        self.__telephone = telephone
        self.__produits:list[Produit] = []

    def get_nom(self) -> str:
        return self.__nom

    def set_nom(self, nom: str) -> None:
        self.__nom = str(nom)

    def get_adresse(self) -> str:
        return self.__adresse

    def set_adresse(self, adresse: str) -> None:
        self.__adresse = str(adresse)

    def get_telephone(self) -> str:
        return self.__telephone

    def set_telephone(self, telephone: str) -> None:
        self.__telephone = str(telephone)

    def get_produits(self):
        return self.__produits

    def __str__(self) -> str:
        ch = "\n"
        ch += "Nom: {0}".format(self.get_nom()) + "\n"
        ch += "Adresse: {0}".format(self.get_adresse()) + "\n"
        ch += "N° Téléphone: {0}".format(self.get_telephone()) + "\n"
        ch += "\n"
        return ch

    def get_produits_par_disponibilite(self, disponibilite: bool = True):
        disponibles:list[Produit] = []
        for produit in self.get_produits():
            if produit.est_disponible() == disponibilite:
                disponibles.append(produit)
        return disponibles

    def get_produit_par_reference(self, reference: str) -> Produit:
        for produit in self.get_produits():
            if produit.get_reference().lower() == reference.lower():
                return produit
        return None

    def get_produits_par_designation(self, designation: str):
        produits:list[Produit] = []
        for produit in self.get_produits():
            if produit.get_designation().lower().find(designation.lower()) != -1:
                produits.append(produit)
        return produits

    def ajouter_produit(self, produit: Produit) -> bool:
        if self.get_produit_par_reference(produit.get_reference()) != None:
            return False
        self.get_produits().append(produit)
        return True

    def modifier_produit(self, produit: Produit) -> bool:
        for _produit in self.get_produits():
            if _produit.get_reference().lower() == produit.get_reference().lower():
                _produit.set_designation(produit.get_designation())
                _produit.set_prix_u(produit.get_prix_u())
                _produit.set_tva(produit.get_tva())
                _produit.set_disponibilite(produit.est_disponible())
                return True
        return False
        
    def supprimer_produit(self, reference: str) -> bool:
        if self.get_produit_par_reference(reference) == None:
            return False
        a_supprimer = Produit(reference, "", 0.0, 0.0, False)
        self.get_produits().remove(a_supprimer)
        return True

    def lire_depuis_fichier(self,fichier):
        produits:list[Produit] = []
        for line in fichier.readlines():
            donnes = line.rstrip().split(';')
            produits.append(Produit.depuis_list(donnes))
        self.get_produits().extend(produits)


class Gestion_Stock(Tk):
    def __init__(self,stock:Stock,className: str = ...) -> None:
        super().__init__(className=className)
        self.stock = stock
    def design(self):
        self.geometry("800x500")
        self.minsize(800,500)
        self.state('zoomed')
        self.resizable(False,False)
        
        self.menu_bar = Menu(self)

        self.fichier_menu = Menu(self.menu_bar,tearoff=0)

        self.fichier_menu.add_command(label='enregistrer',command=self.enregistrer)
        self.fichier_menu.add_command(label='ouvrir',command=self.ouvrir)
        self.fichier_menu.add_separator()
        self.fichier_menu.add_command(label='quitter',command=self.quitter)
        self.menu_bar.add_cascade(label='fichier',menu=self.fichier_menu)

        self.taches_menu = Menu(self.menu_bar,tearoff=0)

        self.taches_menu.add_command(label='Affichier statistics',command=self.affichier_statistics)
        self.taches_menu.add_command(label='Affichier tous les produits',command=self.affichier_tous)
        self.taches_menu.add_command(label='Affichier les produits disponibles en stock',command=lambda :self.affichier_par_disponibilite(True))
        self.taches_menu.add_command(label='Affichier les produits non disponibles en stock',command=lambda :self.affichier_par_disponibilite(False))
        self.taches_menu.add_command(label='Recherche par référence',command=lambda:(self.affichier_recherche('ref'),self.recherche_btn.config(text='recherche par reference')))
        self.taches_menu.add_command(label='Recherche par désignation',command=lambda:(self.affichier_recherche('des'),self.recherche_btn.config(text='recherche par designation')))
        self.taches_menu.add_command(label='Ajouter un produit',command=lambda: self.affichier_formulaire('Ajouter',self.ajouter_produit))
        self.taches_menu.add_command(label='Modifier un produit',command=lambda:self.affichier_recherche('mod'))
        self.taches_menu.add_command(label='Supprimer un produit',command=lambda:self.affichier_recherche('sup'))
        self.taches_menu.add_separator()

        self.tri_menu = Menu(self.taches_menu,tearoff=0)

        self.tri_menu.add_command(label='Tri croissant par Designation',command=lambda : self.tri_produits(Gestion_Stock.par_designation,False))
        self.tri_menu.add_command(label='Tri décroissant par Designation',command=lambda : self.tri_produits(Gestion_Stock.par_designation,True))
        self.tri_menu.add_separator()
        self.tri_menu.add_command(label='Tri croissant par Prix Unitaire',command=lambda : self.tri_produits(Gestion_Stock.par_prix,False))
        self.tri_menu.add_command(label='Tri décroissant par Prix Unitaire',command=lambda : self.tri_produits(Gestion_Stock.par_prix,True))
        self.tri_menu.add_separator()
        self.tri_menu.add_command(label='Tri croissant par TVA',command=lambda : self.tri_produits(Gestion_Stock.par_tva,False))
        self.tri_menu.add_command(label='Tri décroissant par TVA',command=lambda : self.tri_produits(Gestion_Stock.par_tva,True))

        self.taches_menu.add_cascade(label='tri les produits',menu=self.tri_menu)

        self.menu_bar.add_cascade(label='taches',menu=self.taches_menu)

        self.configure(menu=self.menu_bar)

        self.affichier_frame = Frame(self)

        coloms = ('reference','designation','prix untaire','TVA','disponabilite')
        self.table = ttk.Treeview(self.affichier_frame,columns=coloms,show='headings')
        for i in range(5):
            self.table.column(f'{i}',width=155,minwidth=100)
        for col in coloms:
            self.table.heading(col,text=col)
        self.table.pack(side=LEFT,fill=BOTH,expand=1)

        self.scrollbar = Scrollbar(self.affichier_frame,command=self.table.yview)
        self.scrollbar.pack(side=RIGHT,fill=Y,anchor=E)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.recherche_frame = Frame(self,width=600,padx=15,pady=15)
        
        self.recherche_entr = ttk.Entry(self.recherche_frame,width=30)
        self.recherche_entr.grid(column=0,row=1,columnspan=2,pady=10,padx=10)

        self.recherche_type = StringVar()
        self.recherche_type.set('ref')

        self.par_reference_rb = ttk.Radiobutton(self.recherche_frame,text='par reference',value='ref',variable=self.recherche_type,command=lambda : self.recherche_btn.config(text='recherche par reference'))
        self.par_reference_rb.grid(column=0,row=0,sticky='w',pady=10,padx=10)
        self.par_designation_rb = ttk.Radiobutton(self.recherche_frame,text='par designation',value='des',variable=self.recherche_type,command=lambda : self.recherche_btn.config(text='recherche par designation'))
        self.par_designation_rb.grid(column=1,row=0,sticky='w',pady=10,padx=10)
        self.recherche_btn = ttk.Button(self.recherche_frame,text='recherche par reference',width=26,command=self.recherche)
        self.recherche_btn.grid(column=0,row=2,columnspan=2,pady=10,padx=10)
        self.lbl_recherche = ttk.Label(self.recherche_frame,text='recherche par reference')

        self.formulaire_frame = Frame(self,width=600,padx=15,pady=35)
        
        self.lbl_reference = ttk.Label(self.formulaire_frame,text='reference : ',width=34)
        self.lbl_reference.grid(column=0,row=0,pady=10,padx=10,sticky='w')
        self.lbl_designation = ttk.Label(self.formulaire_frame,text='designation : ',width=34)
        self.lbl_designation.grid(column=0,row=1,pady=10,padx=10,sticky='w')
        self.lbl_prix = ttk.Label(self.formulaire_frame,text='prix untaire: ',width=34)
        self.lbl_prix.grid(column=0,row=2,pady=10,padx=10,sticky='w')
        self.lbl_tva = ttk.Label(self.formulaire_frame,text='TVA : ',width=34)
        self.lbl_tva.grid(column=0,row=3,pady=10,padx=10,sticky='w')
        self.lbl_disponibilite = ttk.Label(self.formulaire_frame,text='disponibilite : ',width=34)
        self.lbl_disponibilite.grid(column=0,row=4,pady=10,padx=10,sticky='w')

        self.entr_reference = ttk.Entry(self.formulaire_frame,width=50)
        self.entr_reference.grid(column=1,row=0)
        self.entr_designation = ttk.Entry(self.formulaire_frame,width=50)
        self.entr_designation.grid(column=1,row=1)
        self.entr_prix = ttk.Entry(self.formulaire_frame,width=50)
        self.entr_prix.grid(column=1,row=2)
        self.entr_tva = ttk.Entry(self.formulaire_frame,width=50)
        self.entr_tva.grid(column=1,row=3)
        self.disponibilite = BooleanVar()
        self.disponibilite.set(True)
        self.cb_disponibilite = ttk.Checkbutton(self.formulaire_frame,variable=self.disponibilite,onvalue=True,offvalue=False,command=lambda : self.cb_disponibilite.configure(text='oui') if self.disponibilite.get() else self.cb_disponibilite.configure(text='non'))
        self.cb_disponibilite.grid(column=1,row=4)

        self.error_reference = ttk.Label(self.formulaire_frame,foreground='red',width=50)
        self.error_reference.grid(column=2,row=0,padx=10,sticky='w')
        self.error_designation = ttk.Label(self.formulaire_frame,foreground='red',width=50)
        self.error_designation.grid(column=2,row=1,padx=10,sticky='w')
        self.error_prix = ttk.Label(self.formulaire_frame,foreground='red',width=50)
        self.error_prix.grid(column=2,row=2,padx=10,sticky='w')
        self.error_tva = ttk.Label(self.formulaire_frame,foreground='red',width=50)
        self.error_tva.grid(column=2,row=3,padx=10,sticky='w')
        self.error_disponibilite = ttk.Label(self.formulaire_frame,foreground='red',width=50)
        self.error_disponibilite.grid(column=2,row=4,padx=10,sticky='w')

        self.btn_formulaire = ttk.Button(self.formulaire_frame,text='button')

        self.statistic_frame = Frame(self,padx=20,pady=20)

        figure1 = Figure(figsize=(7, 5), dpi=100)

        self.canvas1 = FigureCanvasTkAgg(figure1,self.statistic_frame)

        self.histogram_1 = figure1.add_subplot()

        self.canvas1.get_tk_widget().grid(column=0,row=0)


        figure2 = Figure(figsize=(7, 5), dpi=100)

        self.canvas2 = FigureCanvasTkAgg(figure2,self.statistic_frame)

        self.histogram_2 = figure2.add_subplot()

        self.canvas2.get_tk_widget().grid(column=1,row=0)

        figure3 = Figure(figsize=(7, 5), dpi=100)

        self.canvas3 = FigureCanvasTkAgg(figure3,self.statistic_frame)

        self.pie_chart = figure3.add_subplot()

        self.canvas3.get_tk_widget().grid(column=0,row=1,columnspan=2)
        self.statistic_frame.grid_columnconfigure((0,1),weight=1)
        self.statistic_frame.grid_rowconfigure((0,1),weight=1)

        self.affichier_statistics()

        self.btn_3_menu = Menu(self.table,tearoff=0)
        self.btn_3_menu.add_command(label='modifier',command=lambda :(self.recherche_type.set('mod'), self.recherche()))
        self.btn_3_menu.add_command(label='supprimer',command=lambda :(self.recherche_type.set('sup'), self.recherche()))

        self.table.bind('<Button-3>',lambda ev:self.btn_3_click(ev.x,ev.y))
        self.selct = None
        
        self.protocol('WM_DELETE_WINDOW',self.quitter)

    def btn_3_click(self,x,y):
        iid = self.table.identify('item',x,y)
        if iid :
            self.table.selection_set(iid)
            self.selct=self.table.item(iid,'values')[0]
            self.recherche_entr.delete(0,END)
            self.recherche_entr.insert(0,self.selct)
            self.btn_3_menu.post(x,y)
        else :
            self.selct = None
    def affichier_menu(self,menu:Frame):
        self.recherche_frame.pack_forget()
        self.affichier_frame.pack_forget()
        self.formulaire_frame.pack_forget()
        self.statistic_frame.pack_forget()
        if menu in (self.affichier_frame,self.statistic_frame) :
            menu.pack(fill=BOTH, expand=True)
        else :
            menu.pack()

    def affichier_statistics(self):
        self.histogram_1.clear()
        self.histogram_2.clear()
        self.pie_chart.clear()

        designations = [produit.get_designation() for produit in self.stock.get_produits()]
        pris = [produit.get_prix_u() for produit in self.stock.get_produits()]
        tva = [produit.get_tva() for produit in self.stock.get_produits()]
        disponibilite = [produit.est_disponible() for produit in self.stock.get_produits()]
        if len(disponibilite)!=0:
            percentages = [(disponibilite.count(True)*100)/len(disponibilite),100-(disponibilite.count(True)*100)/len(disponibilite)]

            self.pie_chart.pie(percentages,autopct=lambda pct:f'{round(pct,2)}%',explode=(0.1,0.1),labels=('disonible','non disponible'),shadow=True,colors=("lime",'red'),startangle=90,wedgeprops={'linewidth':1,'edgecolor':"black"})
            self.pie_chart.legend(['disonible','non disponible'],title='disponibilte',loc ="upper right",bbox_to_anchor =(1, 0, 0.39, 1))
        


        self.histogram_1.bar(designations, pris)
        self.histogram_1.set_title('les pris')
        self.histogram_1.set_ylabel('prix untaire')

        self.histogram_2.bar(designations, tva)
        self.histogram_2.set_title('tva des produits')
        self.histogram_2.set_ylabel('tva')

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

        self.affichier_menu(self.statistic_frame)
    def affichier_recherche(self,recherche_type:str):
        self.recherche_entr.delete(0,END)
        self.recherche_type.set(recherche_type)
        if recherche_type in ("des","ref"):
            self.lbl_recherche.grid_forget()
            self.par_reference_rb.grid(column=0,row=0,sticky='w',pady=10,padx=10)
            self.par_designation_rb.grid(column=1,row=0,sticky='w',pady=10,padx=10)
        else :
            self.recherche_btn.config(text='recherche par reference')
            self.par_designation_rb.grid_forget()
            self.par_reference_rb.grid_forget()
            self.lbl_recherche.grid(column=0,row=0,columnspan=2,pady=10)
        
        self.affichier_menu(self.recherche_frame)

    def recherche(self):
        self.entr_reference.configure(state=NORMAL)
        self.entr_designation.configure(state=NORMAL)
        self.entr_prix.configure(state=NORMAL)
        self.entr_tva.configure(state=NORMAL)
        self.cb_disponibilite.configure(state=NORMAL)

        self.entr_reference.delete(0,END)
        self.entr_designation.delete(0,END)
        self.entr_prix.delete(0,END)
        self.entr_tva.delete(0,END)

        if self.recherche_type.get()== 'des':
            self.table.delete(*self.table.get_children())
            for produit in self.stock.get_produits_par_designation(self.recherche_entr.get()) :
                self.table.insert('',END,values=(produit.get_reference(),produit.get_designation(),produit.get_prix_u(),produit.get_tva(),dict_oui_non.get(produit.est_disponible())))
            self.affichier_menu(self.affichier_frame)
            return
        
        produit = self.stock.get_produit_par_reference(self.recherche_entr.get())
        if produit is None :
            messagebox.showwarning('produit introvable',f'il n\'existe pas un produit avec la reference " {self.recherche_entr.get()} "')
            
            return
        
        if self.recherche_type.get() == 'ref' :
            self.entr_reference.configure(state=NORMAL)
            self.entr_designation.configure(state=NORMAL)
            self.entr_prix.configure(state=NORMAL)
            self.entr_tva.configure(state=NORMAL)
            self.cb_disponibilite.configure(state=NORMAL)
            self.entr_reference.insert(0,produit.get_reference())
            self.entr_designation.insert(0,produit.get_designation())
            self.entr_prix.insert(0,produit.get_prix_u())
            self.entr_tva.insert(0,produit.get_tva())
            if produit.est_disponible() :
                self.disponibilite.set(True)
                self.cb_disponibilite.configure(text='oui')
            else :
                self.disponibilite.set(False)
                self.cb_disponibilite.configure(text='non')

            self.affichier_formulaire('affichier',None)
        elif self.recherche_type.get() =='mod' :
            self.entr_reference.insert(0,produit.get_reference())
            self.entr_reference.configure(state='readonly')
            self.entr_designation.insert(0,produit.get_designation())
            self.entr_prix.insert(0,produit.get_prix_u())
            self.entr_tva.insert(0,produit.get_tva())
            if produit.est_disponible() :
                self.disponibilite.set(True)
                self.cb_disponibilite.configure(text='oui')
            else :
                self.disponibilite.set(False)
                self.cb_disponibilite.configure(text='non')
            self.affichier_formulaire('Modifier',self.modifier_produit)
        elif self.recherche_type.get() == 'sup' :
            if messagebox.askyesno('confirmation','voulez vous supprimer ce produit ?') :
                self.stock.supprimer_produit(produit.get_reference())
                messagebox.showinfo('supprimer','le produit a bien supprimer')
            self.affichier_tous()

    def affichier_tous(self):
        self.table.delete(*self.table.get_children())
        for produit in self.stock.get_produits() :
            self.table.insert('',END,values=(produit.get_reference(),produit.get_designation(),produit.get_prix_u(),produit.get_tva(),dict_oui_non.get(produit.est_disponible())))
        self.affichier_menu(self.affichier_frame)
        if len(self.table.get_children()) != 0:
            self.table.see(self.table.get_children()[-1])

    def affichier_par_disponibilite(self,disponibilite:bool):
        self.table.delete(*self.table.get_children())
        for produit in self.stock.get_produits_par_disponibilite(disponibilite) :
            self.table.insert('',END,values=(produit.get_reference(),produit.get_designation(),produit.get_prix_u(),produit.get_tva(),dict_oui_non.get(produit.est_disponible())))
        self.affichier_menu(self.affichier_frame)
        if len(self.table.get_children()) != 0:
            self.table.see(self.table.get_children()[-1])

    def modifier_produit(self):
        self.error_reference.configure(text='')
        self.error_designation.configure(text='')
        self.error_prix.configure(text='')
        self.error_tva.configure(text='')
        while True :
            reference = self.entr_reference.get()

            designation = self.entr_designation.get()
            if len(designation) < 5 :
                self.error_designation.configure(text='la designation doit avoir 5 caractere')
                break

            try :
                prix_u = float(self.entr_prix.get())
                if prix_u < 0 :
                    raise Exception()
            except :
                self.error_prix.configure(text='valeur error')
                break

            try :
                tva = float(self.entr_tva.get())
                if tva < 0 :
                    raise Exception()
            except :
                self.error_tva.configure(text='valeur error')
                break

            disponibilite = self.disponibilite.get()

            produit = Produit(reference,designation,prix_u,tva,disponibilite)
            if messagebox.askyesno('modifier','voulez vous modifier ce produit ?') :
                self.stock.modifier_produit(produit)
                messagebox.showinfo('modifier','le produit a bien modifier')
                self.affichier_tous()

            break

    def ajouter_produit(self):
        self.error_reference.configure(text='')
        self.error_designation.configure(text='')
        self.error_prix.configure(text='')
        self.error_tva.configure(text='')
        while True :
            reference = self.entr_reference.get()
            if len(reference) < 3 :
                self.error_reference.configure(text='la refernce doit avoir 3 caractere')
                break
            elif self.stock.get_produit_par_reference(reference) is not None :
                self.error_reference.configure(text='il existe deja un produit avec cette reference')
                break
            designation = self.entr_designation.get()
            if len(designation) < 5 :
                self.error_designation.configure(text='la designation doit avoir 5 caractere')
                break

            try :
                prix_u = float(self.entr_prix.get())
                if prix_u < 0 :
                    raise Exception()
            except :
                self.error_prix.configure(text='valeur error')
                break

            try :
                tva = float(self.entr_tva.get())
                if tva < 0 :
                    raise Exception()
            except :
                self.error_tva.configure(text='valeur error')
                break

            disponibilite = self.disponibilite.get()
            produit = Produit(reference,designation,prix_u,tva,disponibilite)
            
            self.stock.ajouter_produit(produit)
            messagebox.showinfo('ajouter','le produit a bien ajouter')
            self.affichier_formulaire('Ajouter',self.ajouter_produit)
            break

    def affichier_formulaire(self,text,command):
        self.error_reference.configure(text='')
        self.error_designation.configure(text='')
        self.error_prix.configure(text='')
        self.error_tva.configure(text='')
        if text == 'affichier':
            self.entr_reference.configure(state='readonly')
            self.entr_designation.configure(state='readonly')
            self.entr_prix.configure(state='readonly')
            self.entr_tva.configure(state='readonly')
            self.cb_disponibilite.configure(state=DISABLED)
            self.btn_formulaire.grid_forget()
        else :
            self.btn_formulaire.configure(text=text,command=command)
            self.btn_formulaire.grid(column=0,row=5,columnspan=2,pady=10,sticky='e')
            if text == 'Ajouter':
                self.entr_reference.configure(state=NORMAL)
                self.entr_designation.configure(state=NORMAL)
                self.entr_prix.configure(state=NORMAL)
                self.entr_tva.configure(state=NORMAL)
                self.cb_disponibilite.configure(state=NORMAL)

                self.entr_reference.delete(0,END)
                self.entr_designation.delete(0,END)
                self.entr_prix.delete(0,END)
                self.entr_tva.delete(0,END)
                self.disponibilite.set(True)
                self.cb_disponibilite.configure(text='oui')
        self.affichier_menu(self.formulaire_frame)

    @staticmethod
    def par_designation(pr:Produit):
        return pr.get_designation()

    @staticmethod
    def par_tva(pr:Produit):
        return pr.get_tva()

    @staticmethod
    def par_prix(pr:Produit):
        return pr.get_prix_u()

    def tri_produits(self,key,rev):
        self.stock.get_produits().sort(key=key,reverse=rev)
        self.affichier_tous()

    def enregistrer(self):
        files = [('Text Document', '*.txt'),('All Files', '*.*')]
        file = filedialog.asksaveasfile(title='enregistrer',filetypes = files, defaultextension = files)
        if file is not None :
            for produit in self.stock.get_produits():
                file.write(repr(produit)+'\n')
            file.close()
    
    def ouvrir(self):
        if messagebox.askyesno('enregistrement',"voulez vous enregesrtrer les changement\navant d'ouvrir un neavau fichier"):
            self.enregistrer()
        filetypes = (('text files', '*.txt'),('All files', '*.*'))
        filename = filedialog.askopenfilename(title='Ouvrir un fichier',initialdir='/',filetypes=filetypes)
        if filename != '':
            fichier = open(filename,'r')
            self.stock.get_produits().clear()
            self.stock.lire_depuis_fichier(fichier)
            fichier.close()
            self.affichier_statistics()
    
    def quitter(self):
        con = messagebox.askyesnocancel('enregistrer','voulez vous enregestrer ?')
        if con == True :
            self.enregistrer()
        if con is not None :
            self.destroy()





mon_stock = Stock('mon stock','adress','0600000011')
root = Gestion_Stock(mon_stock,'gestion de stock')
root.design()

root.mainloop()