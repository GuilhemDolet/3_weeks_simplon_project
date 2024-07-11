from itemadapter import ItemAdapter
import re

class FormationSimplonPipeline:
    def process_item(self, item, spider):
        # items de la page formation
        item = self.clean_categorie(item)
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_voie_acces(item)

        # items de la page session
        item = self.clean_date_limite(item)
        item = self.clean_region(item)
        item = self.clean_distanciel(item)
        item = self.clean_alternance(item)
        item = self.clean_echelle_duree(item)
        item = self.clean_date_debut(item)
        item = self.clean_date_fin(item)

        # item de la page francecompetences
        item = self.clean_nsf_code(item)
        item = self.clean_nsf_nom(item)
        item = self.clean_formacode_code(item)
        item = self.clean_formacode_nom(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_certificateur_nom(item)
        item = self.clean_siret(item)

        item = self.clean_nsf_code_rs(item)
        item = self.clean_nsf_nom_rs(item)
        item = self.clean_formacode_code_rs(item)
        item = self.clean_formacode_nom_rs(item)
        item = self.clean_certificateur_nom_rs(item)
        item = self.clean_siret_rs(item)

        return item
    
    # Nettoyage pages "découvrez la formation"
    def clean_categorie(self, item):
        adapter = ItemAdapter(item)
        categorie = adapter.get("categorie")
        if categorie:
            categorie = categorie.strip()
        adapter["categorie"] = categorie
        return item
    
    def clean_rncp(self, item):
        adapter = ItemAdapter(item)
        rncp = adapter.get("code_rncp")
        if rncp is not None:
            rncp = re.findall(r'(\d+)', rncp)[0]
            adapter["code_rncp"] = rncp
        return item
    
    def clean_rs(self, item):
        adapter = ItemAdapter(item)
        rs = adapter.get("code_rs")
        if rs is not None:
            rs = re.findall(r'(\d+)', rs)[0]
            adapter["code_rs"] = rs
        return item
    
    def clean_voie_acces(self, item):
        adapter = ItemAdapter(item)
        voie_acces = adapter.get("voie_acces")
        voie_temp = []
        if voie_acces:
            if voie_acces != []:
                for i in range(len(voie_acces)):
                    voie_acces[i] = voie_acces[i].replace(";","")
                    voie_acces[i] = voie_acces[i].strip()
                    if voie_acces[i]:
                        voie_temp.append(voie_acces[i])
                adapter["voie_acces"] = voie_temp
        return item
   
    # Nettoyage pages sessions/session?
    def clean_date_limite(self, item):
        adapter = ItemAdapter(item)
        date_limite = adapter.get("date_limite")
        if date_limite:
            if date_limite != []:
                date_limite = ";".join(date_limite)
                date_limite = re.findall(r'(\d+)', date_limite)
                date_limite = "/".join(date_limite)
                adapter["date_limite"] = date_limite
        return item
    
    def clean_region(self, item):
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        region_temp = []
        if region:
            if region != []:
                for i in range(len(region)):
                    region[i] = region[i].strip()
                    if region[i]:
                        region_temp.append(region[i])
                adapter["region"] = region_temp[0]
        return item

    def clean_distanciel(self, item):
        adapter = ItemAdapter(item)
        distanciel = adapter.get(item)
        if distanciel is not None:
            distanciel = True
        else:
            distanciel= False
        adapter["distanciel"] = distanciel
        return item
    
    def clean_alternance(self, item):
        adapter = ItemAdapter(item)
        alternance = adapter.get("alternance")
        if alternance is not None:
            alternance = True
        else:
            alternance = False
        adapter["alternance"] = alternance
        return item

    def clean_echelle_duree(self, item):
        adapter = ItemAdapter(item)
        echelle_duree = adapter.get("echelle_duree")
        if echelle_duree:
            if echelle_duree != []:
                for i in range(len(echelle_duree)):
                    echelle_duree[i] = echelle_duree[i].strip()
                echelle_duree = "".join(echelle_duree)
            adapter["echelle_duree"] = echelle_duree
        return item

    def clean_date_debut(self, item):
        adapter = ItemAdapter(item)
        date_debut = adapter.get("date_debut")
        if date_debut:
            if date_debut != []:
                date_debut = "".join(date_debut)
                date_debut = re.findall(r'\d+/?', date_debut)
                date_debut = "".join(date_debut)
                adapter["date_debut"] = date_debut
        return item
    
    def clean_date_fin(self, item):
        adapter = ItemAdapter(item)
        date_fin = adapter.get("date_fin")
        if date_fin is not None:
            date_fin = date_fin.replace("\xa0"," ")\
                .replace("Janvier", "01").replace("janvier","01")\
                .replace("Février", "02").replace("février", "02")\
                .replace("Mars", "03").replace("mars", "03")\
                .replace("Avril", "04").replace("avril", "04")\
                .replace("Mai", "05").replace("mai", "05")\
                .replace("Juin", "06").replace("juin", "06")\
                .replace("Juillet","07").replace("juillet", "07")\
                .replace("Août","08").replace("août", "08")\
                .replace("Septembre","09").replace("septembre", "09")\
                .replace("Octobre","10").replace("octobre", "10")\
                .replace("Novembre","11").replace("novembre", "11")\
                .replace("Décembre","12").replace("décembre", "12")
            try:
                date_fin = re.findall(r"(au .+\d{2,4})(?! ?[hH])",date_fin)[0]
            except IndexError:
                pass
            date_fin = re.findall(r'(\d+)', date_fin)
            date_fin = "".join(date_fin)
            date_fin = f"{date_fin[:-6]}/{date_fin[-6:-4]}/{date_fin[-4:]}"
            adapter["date_fin"] = date_fin
        return item

    # def clean_date_fin(self, item):
    #     adapter = ItemAdapter(item)
    #     date_fin = adapter.get("date_fin")
    #     if date_fin is not None:
    #         date_fin = date_fin.replace("\xa0"," ")\
    #             .replace("Janvier", "01").replace("janvier","01")\
    #             .replace("Février", "02").replace("février", "02")\
    #             .replace("Mars", "03").replace("mars", "03")\
    #             .replace("Avril", "04").replace("avril", "04")\
    #             .replace("Mai", "05").replace("mai", "05")\
    #             .replace("Juin", "06").replace("juin", "06")\
    #             .replace("Juillet","07").replace("juillet", "07")\
    #             .replace("Août","08").replace("août", "08")\
    #             .replace("Septembre","09").replace("septembre", "09")\
    #             .replace("Octobre","10").replace("octobre", "10")\
    #             .replace("Novembre","11").replace("novembre", "11")\
    #             .replace("Décembre","12").replace("décembre", "12")
    #         date_fin = re.findall(r'(\d+)', date_fin)[-3:]
    #         date_fin = "/".join(date_fin)
    #         adapter["date_fin"] = date_fin
    #     return item


    # Nettoyage pages francecompetences    
    def clean_nsf_code(self, item):
        adapter = ItemAdapter(item)
        nsf_code = adapter.get("nsf_code")
        if nsf_code:
            if nsf_code != []:
                for i in range(len(nsf_code)):
                    nsf_code[i] = nsf_code.strip()
                adapter["nsf_code"] = nsf_code
        return item
    
    def clean_nsf_nom(self, item):
        adapter = ItemAdapter(item)
        nsf_nom = adapter.get("nsf_nom")
        nsf_nom_temp = []
        if nsf_nom:
            if nsf_nom != []:
                for i in range(len(nsf_nom)):
                    nsf_nom[i] = nsf_nom[i].strip()
                    if nsf_nom[i]:
                        nsf_nom_temp.append(nsf_nom[i])
                adapter["nsf_nom"] = nsf_nom_temp
        return item
    
    def clean_formacode_code(self, item):
        adapter = ItemAdapter(item)
        formacode_code = adapter.get("formacode_code")
        if formacode_code:
            if formacode_code != []:
                for i in range(len(formacode_code)):
                    formacode_code[i] = re.findall(r'(\d+)',formacode_code[i])[0]
                adapter["formacode_code"] = formacode_code
        return item
    
    def clean_formacode_nom(self, item):
        adapter = ItemAdapter(item)
        formacode_nom = adapter.get("formacode_nom")
        formacode_nom_temp = []
        if formacode_nom:
            if formacode_nom != []:
                for i in range(len(formacode_nom)):
                    formacode_nom[i] = formacode_nom[i].strip()
                    if formacode_nom[i]:
                        formacode_nom_temp.append(formacode_nom[i])
                adapter["formacode_nom"] = formacode_nom_temp
        return item
    
    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie is not None:
            niveau_sortie = niveau_sortie.strip()
            adapter["niveau_sortie"] = niveau_sortie
        return item
    
    def clean_certificateur_nom(self, item):
        adapter = ItemAdapter(item)
        certificateur_nom = adapter.get("certificateur_nom")
        if certificateur_nom is not None:
            certificateur_nom = certificateur_nom.strip()
            adapter["certificateur_nom"] = certificateur_nom
        return item
    
    def clean_siret(self, item):
        adapter = ItemAdapter(item)
        siret = adapter.get("siret")
        if siret:
            siret = siret.strip()
            siret = int(siret)
            adapter["siret"] = siret
        return item
    
    def clean_nsf_code_rs(self, item):
        adapter = ItemAdapter(item)
        nsf_code_rs = adapter.get("nsf_code_rs")
        if nsf_code_rs:
            if nsf_code_rs != []:
                for i in range(len(nsf_code_rs)):
                    nsf_code_rs[i] = nsf_code_rs.strip()
                adapter["nsf_code"] = nsf_code_rs
        return item
    
    def clean_nsf_nom_rs(self, item):
        adapter = ItemAdapter(item)
        nsf_nom_rs = adapter.get("nsf_nom_rs")
        nsf_nom_rs_temp = []
        if nsf_nom_rs:
            if nsf_nom_rs != []:
                for i in range(len(nsf_nom_rs)):
                    nsf_nom_rs[i] = nsf_nom_rs[i].strip()
                    if nsf_nom_rs[i]:
                        nsf_nom_rs_temp.append(nsf_nom_rs[i])
                adapter["nsf_nom_rs"] = nsf_nom_rs_temp
        return item

    def clean_formacode_code_rs(self, item):
        adapter = ItemAdapter(item)
        formacode_code = adapter.get("formacode_code_rs")
        if formacode_code:
            if formacode_code != []:
                for i in range(len(formacode_code)):
                    formacode_code[i] = re.findall(r'(\d+)',formacode_code[i])[0]
                adapter["formacode_code_rs"] = formacode_code
        return item
    
    def clean_formacode_nom_rs(self, item):
        adapter = ItemAdapter(item)
        formacode_nom = adapter.get("formacode_nom_rs")
        formacode_nom_temp = []
        if formacode_nom:
            if formacode_nom != []:
                for i in range(len(formacode_nom)):
                    formacode_nom[i] = formacode_nom[i].strip()
                    if formacode_nom[i]:
                        formacode_nom_temp.append(formacode_nom[i])
                adapter["formacode_nom_rs"] = formacode_nom_temp
        return item
    
    def clean_certificateur_nom_rs(self, item):
        adapter = ItemAdapter(item)
        certificateur_nom = adapter.get("certificateur_nom_rs")
        if certificateur_nom is not None:
            certificateur_nom = certificateur_nom.strip()
            adapter["certificateur_nom_rs"] = certificateur_nom
        return item
    
    def clean_siret_rs(self, item):
        adapter = ItemAdapter(item)
        siret = adapter.get("siret_rs")
        if siret:
            siret = siret.strip()
            siret = int(siret)
            adapter["siret_rs"] = siret
        return item