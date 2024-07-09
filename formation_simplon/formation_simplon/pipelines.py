from itemadapter import ItemAdapter
import re

class FormationSimplonPipeline:
    def process_item(self, item, spider):
        item = self.clean_categorie(item)
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_voie_acces(item)

        return item
    
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
            if "RNCP" in rncp:
                rncp = re.findall(r'(\d+)', rncp)[0]
            else:
                rncp = None
            adapter["code_rncp"] = rncp
        return item
    
    def clean_rs(self, item):
        adapter = ItemAdapter(item)
        rs = adapter.get("code_rs")
        if rs is not None:
            if "RS" in rs:
                rs = re.findall(r'(\d+)', rs)[0]
            else:
                rs = None
            adapter["code_rs"] = rs
        return item
    
    def clean_voie_acces(self, item):
        adapter = ItemAdapter(item)
        voie_acces = adapter.get("voie_acces")
        for i in range(len(voie_acces)):
            voie_acces[i] = voie_acces[i].replace(";","")
            voie_acces[i] = voie_acces[i].strip()
        adapter["voie_acces"] = voie_acces
        return item