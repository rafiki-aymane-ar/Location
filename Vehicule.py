from tabulate import tabulate
from datetime import date, timedelta


class Vehicule:
    def __init__(self, marque, modele, anneeFabrication, prixLocation):
        self.__marque = marque
        self.__modele = modele
        self.__anneeFabrication = anneeFabrication
        self._prixLocation = prixLocation

    @property
    def marque(self):
        return self.__marque

    @marque.setter
    def marque(self, marque):
        self.__marque = marque

    @property
    def modele(self):
        return self.__modele

    @modele.setter
    def modele(self, modele):
        self.__modele = modele

    @property
    def anneeFabrication(self):
        return self.__anneeFabrication

    @anneeFabrication.setter
    def anneeFabrication(self, anneeFabrication):
        if isinstance(anneeFabrication, int) and anneeFabrication > 0:
            self.__anneeFabrication = anneeFabrication
        else:
            raise ValueError("L'annee de fabrication doit etre un nombre positif")

    @property
    def prixLocation(self):
        return self._prixLocation

    @prixLocation.setter
    def prixLocation(self, prixLocation):
        if prixLocation > 0:
            self._prixLocation = prixLocation
        else:
            raise ValueError("Le prix de location ne peut pas etre negatif")

    def afficher(self):
        print(f" Marque : {self.__marque} \n"
              f" Modele : {self.__modele} \n"
              f" Annee de fabrication : {self.__anneeFabrication} \n"
              f" Prix de location : {self._prixLocation}")

    def calculer_prix_location(self, duree):
        prix = self._prixLocation * duree
        if duree >= 7:
            return self.reduire_prix_location(prix)
        else:
            return prix

    def reduire_prix_location(self, prix):
        return prix - prix * 10 / 100

    def augmenter_prix_location(self, prix, pourcentage):
        if pourcentage > 0:
            prix += prix * (pourcentage / 100)
            return prix
        else:
            raise ValueError("Le pourcentage d'augmentation doit être positif")

    def getNouveauPrix(self, pourcentage):
        return self.augmenter_prix_location(self.prixLocation, pourcentage)


class Voiture(Vehicule):
    def __init__(self, marque, modele, anneeFabrication, prixLocation, nombre_de_portes):
        super().__init__(marque, modele, anneeFabrication, prixLocation)
        self.__nombre_de_portes = nombre_de_portes

    @property
    def nombre_de_portes(self):
        return self.__nombre_de_portes

    @nombre_de_portes.setter
    def nombre_de_portes(self, nombre_de_portes):
        if nombre_de_portes > 0:
            self.__nombre_de_portes = nombre_de_portes
        else:
            raise ValueError("Le nombre de portes ne peut pas etre negatif")

    def afficher(self):
        super().afficher()
        print(f" Nombre de portes : {self.__nombre_de_portes}")


class Moto(Vehicule):
    def __init__(self, marque, modele, anneeFabrication, prixLocation, cylindre):
        super().__init__(marque, modele, anneeFabrication, prixLocation)
        self.__cylindre = cylindre

    @property
    def cylindre(self):
        return self.__cylindre

    @cylindre.setter
    def cylindre(self, cylindre):
        self.__cylindre = cylindre

    def afficher(self):
        super().afficher()
        print(f" Cylindre : {self.__cylindre} ")


class Camion(Vehicule):
    def __init__(self, marque, modele, anneeFabrication, prixLocation, capacite_de_charge):
        super().__init__(marque, modele, anneeFabrication, prixLocation)
        self.__capacite_de_charge = capacite_de_charge

    @property
    def capacite_de_charge(self):
        return self.__capacite_de_charge

    @capacite_de_charge.setter
    def capacite_de_charge(self, capacite_de_charge):
        if capacite_de_charge > 0:
            self.__capacite_de_charge = capacite_de_charge
        else:
            raise ValueError("La capacite de charge ne peut pas etre negatif")

    def afficher(self):
        super().afficher()
        print(f" Capacite de charge : {self.__capacite_de_charge}")


class Location:
    liste_locations = []

    def __init__(self, nomClient, vehicule, dateDebut, dateFin):
        self.__nomClient = nomClient
        self.__vehicule = vehicule
        self.__dateDebut = dateDebut
        self.__dateFin = dateFin
        if vehicule is not None:
            Location.liste_locations.append(self)

    @property
    def vehicule(self):
        return self.__vehicule

    @vehicule.setter
    def vehicule(self, vehicule):
        self.__vehicule = vehicule

    @property
    def dateDebut(self):
        return self.__dateDebut

    @dateDebut.setter
    def dateDebut(self, nouveauDateDebut):
        if isinstance(nouveauDateDebut, date):
            self.__dateDebut = nouveauDateDebut
        else:
            raise ValueError("La date de debut doit etre une date")

    @property
    def dateFin(self):
        return self.__dateFin

    @dateFin.setter
    def dateFin(self, nouveauDateFin):
        if isinstance(nouveauDateFin, date):
            self.__dateFin = nouveauDateFin
        else:
            raise ValueError("La date de fin doit etre une date")

    def afficher_toutes_locations(self):
        if len(Location.liste_locations) == 0:
            print("\n===== LISTE DES LOCATIONS =====")
            print("Aucune location n'est enregistrée.")
            return

        headers = ["Numero", "Type", "Marque", "Modele", "Date Debut", "Durée (jours)", "Prix Total (DH)"]
        table_data = []

        for i, location in enumerate(Location.liste_locations, 1):
            duree = (location.dateFin - location.dateDebut).days
            prix = location.vehicule.calculer_prix_location(duree)

            row = [
                i,
                location.vehicule.__class__.__name__,
                location.vehicule.marque,
                location.vehicule.modele,
                location.dateDebut.strftime("%d/%m/%Y"),
                duree,
                f"{prix:.2f}"
            ]
            table_data.append(row)

        print("\n===== LISTE DES LOCATIONS =====")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def ajouter_location(self):
        print("\n=== AJOUTER UNE LOCATION ===")
        nom_client = input("Nom du client : ")

        print("\nType de véhicule :")
        print("1. Voiture")
        print("2. Moto")
        print("3. Camion")
        type_vehicule = input("Choix : ").strip()

        marque = input("Marque : ")
        modele = input("Modèle : ")

        try:
            annee = int(input("Année de fabrication : "))
            prix = float(input("Prix de location par jour : "))

            if type_vehicule == "1" or type_vehicule == 1:
                portes = int(input("Nombre de portes : "))
                vehicule = Voiture(marque, modele, annee, prix, portes)
            elif type_vehicule == "2" or type_vehicule == 2:
                cylindre = int(input("Cylindrée : "))
                vehicule = Moto(marque, modele, annee, prix, cylindre)
            elif type_vehicule == "3" or type_vehicule == 3:
                capacite = float(input("Capacité de charge : "))
                vehicule = Camion(marque, modele, annee, prix, capacite)
            else:
                print("Type de véhicule invalide")
                return
            annee_debut = int(input("Date début - Année : "))
            mois_debut = int(input("Date début - Mois : "))
            jour_debut = int(input("Date début - Jour : "))
            date_debut = date(annee_debut, mois_debut, jour_debut)

            duree = int(input("Durée de location (en jours) : "))
            if duree <= 0:
                print("La durée doit être positive")
                return

            date_fin = date_debut + timedelta(days=duree)

            nouvelle_location = Location(nom_client, vehicule, date_debut, date_fin)
            print("Location ajoutée avec succès!")

        except ValueError as e:
            print(f"Erreur de saisie : {e}")
            return

    def rechercher_location(self, numero):
        if 1 <= numero <= len(self.liste_locations):
            return self.liste_locations[numero - 1]
        return None

    def afficher_details(self):
        try:
            numero = int(input("Entrez le numéro de la location : "))
            location = self.rechercher_location(numero)
            if location:
                print("\n=== DÉTAILS DE LA LOCATION ===")
                print(f"Client : {location._Location__nomClient}")
                print(f"Véhicule : {location.vehicule.__class__.__name__}")
                print(f"Marque : {location.vehicule.marque}")
                print(f"Modèle : {location.vehicule.modele}")
                print(f"Date début : {location.dateDebut.strftime('%d/%m/%Y')}")
                print(f"Date fin : {location.dateFin.strftime('%d/%m/%Y')}")
                duree = (location.dateFin - location.dateDebut).days
                prix = location.vehicule.calculer_prix_location(duree)
                print(f"Durée : {duree} jours")
                print(f"Prix total : {prix:.2f} DH")

                if isinstance(location.vehicule, Voiture):
                    print(f"Nombre de portes : {location.vehicule.nombre_de_portes}")
                elif isinstance(location.vehicule, Moto):
                    print(f"Cylindrée : {location.vehicule.cylindre}")
                elif isinstance(location.vehicule, Camion):
                    print(f"Capacité de charge : {location.vehicule.capacite_de_charge}")
            else:
                print("Location non trouvée")
        except ValueError as e:
            print(f"Erreur de saisie : {e}")

    def chiffre_affaire(self):
        total = 0
        for location in self.liste_locations:
            duree = (location.dateFin - location.dateDebut).days
            total += location.vehicule.calculer_prix_location(duree)
        return total

    def augmenter_prix(self):
        try:
            numero = int(input("Entrez le numéro de location : "))
            location = self.rechercher_location(numero)
            if location:
                pourcentage = float(input("Entrez le pourcentage d'augmentation : "))
                if pourcentage <= 0:
                    print("Le pourcentage doit être positif")
                    return

                ancien_prix = location.vehicule.prixLocation
                nouveau_prix = location.vehicule.getNouveauPrix(pourcentage)
                location.vehicule.prixLocation = nouveau_prix

                print(f"Prix de location modifié avec succès!")
                print(f"Ancien prix : {ancien_prix:.2f} DH")
                print(f"Nouveau prix : {nouveau_prix:.2f} DH")
            else:
                print("Location non trouvée")
        except ValueError as e:
            print(f"Erreur de saisie : {e}")

    def prolonger_location(self):
        try:
            numero = int(input("Entrez le numéro de location : "))
            location = self.rechercher_location(numero)
            if location:
                jours_supplementaires = int(input("Entrez le nombre de jours supplémentaires : "))
                if jours_supplementaires <= 0:
                    print("Le nombre de jours doit être positif")
                    return

                ancienne_date_fin = location.dateFin
                nouvelle_date_fin = ancienne_date_fin + timedelta(days=jours_supplementaires)
                location.dateFin = nouvelle_date_fin

                print(f"Durée de location prolongée avec succès!")
                print(f"Ancienne date de fin : {ancienne_date_fin.strftime('%d/%m/%Y')}")
                print(f"Nouvelle date de fin : {nouvelle_date_fin.strftime('%d/%m/%Y')}")

                duree_totale = (nouvelle_date_fin - location.dateDebut).days
                nouveau_prix = location.vehicule.calculer_prix_location(duree_totale)
                print(f"Nouveau prix total : {nouveau_prix:.2f} DH")
            else:
                print("Location non trouvée")
        except ValueError as e:
            print(f"Erreur de saisie : {e}")

    def supprimer_location(self):
        try:
            self.afficher_toutes_locations()
            numero = int(input("Entrez le numéro de la location à supprimer : "))
            location = self.rechercher_location(numero)

            if location:
                # Demander confirmation
                confirmation = input(
                    f"Êtes-vous sûr de vouloir supprimer la location de {location.vehicule.marque} {location.vehicule.modele} ? (o/n) : ")

                if confirmation.lower() == 'o':
                    Location.liste_locations.remove(location)
                    print("Location supprimée avec succès!")
                    self.afficher_toutes_locations()
                else:
                    print("Suppression annulée")
            else:
                print("Location non trouvée")

        except ValueError as e:
            print(f"Erreur de saisie : {e}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")


def afficher_banniere():
    print("\n" + "=" * 60)
    print("🚗  SYSTÈME DE GESTION DES LOCATIONS DE VÉHICULES  🏍")
    print("=" * 60)


def afficher_menu():
    print("\n" + "-" * 40)
    print("📋  MENU PRINCIPAL")
    print("-" * 40)
    options = [
        "➕ Ajouter une location",
        "📋 Afficher toutes les locations",
        "❌ Supprimer une location",
        "🔍 Rechercher une location",
        "📝 Afficher détails d'une location",
        "💰 Augmenter le prix de location",
        "⏰ Prolonger une location",
        "💵 Afficher le chiffre d'affaire",
        "🚪 Quitter"
    ]
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("-" * 40)


def menu():
    gestionnaire = Location("", None, date.today(), date.today())
    while True:
        afficher_banniere()
        afficher_menu()

        try:
            choix = input("\n👉 Choisir une option : ")

            if choix == "1":
                print("\n" + "=" * 40)
                print("📝  NOUVELLE LOCATION")
                print("=" * 40)
                gestionnaire.ajouter_location()

            elif choix == "2":
                gestionnaire.afficher_toutes_locations()
                input("\nAppuyez sur Entrée pour continuer...")

            elif choix == "3":
                print("\n" + "=" * 40)
                print("❌  SUPPRESSION DE LOCATION")
                print("=" * 40)
                gestionnaire.supprimer_location()

            elif choix == "4":
                print("\n" + "=" * 40)
                print("🔍  RECHERCHE DE LOCATION")
                print("=" * 40)
                try:
                    numero = int(input("Entrez le numéro de location : "))
                    location = gestionnaire.rechercher_location(numero)
                    if location:
                        location.afficher_details()
                    else:
                        print("⚠️  Location non trouvée")
                except ValueError:
                    print("⚠️  Veuillez entrer un numéro valide")

            elif choix == "5":
                print("\n" + "=" * 40)
                print("📝  DÉTAILS DE LOCATION")
                print("=" * 40)
                gestionnaire.afficher_details()

            elif choix == "6":
                print("\n" + "=" * 40)
                print("💰  AUGMENTATION DE PRIX")
                print("=" * 40)
                gestionnaire.augmenter_prix()

            elif choix == "7":
                print("\n" + "=" * 40)
                print("⏰  PROLONGATION DE LOCATION")
                print("=" * 40)
                gestionnaire.prolonger_location()

            elif choix == "8":
                print("\n" + "=" * 40)
                print("💵  CHIFFRE D'AFFAIRES")
                print("=" * 40)
                print(f"Chiffre d'affaire total : {gestionnaire.chiffre_affaire():.2f} DH")
                input("\nAppuyez sur Entrée pour continuer...")

            elif choix == "9":
                print("\n" + "=" * 40)
                print("👋  Au revoir !")
                print("=" * 40)
                break

            else:
                print("\n⚠️  Option invalide ! Veuillez choisir une option entre 1 et 9.")

        except Exception as e:
            print(f"\n⚠️  Une erreur s'est produite : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    menu()








