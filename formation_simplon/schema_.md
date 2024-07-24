```mermaid
---
title: Simplon
---

erDiagram
    formations {
        int id_formation PK
        string intitule_formation
        string catagorie
        string voie_acces
    }
    sessions {
        int id_session PK
        string region
        string agence
        bool distanciel
        bool alternance
        string echelle_duree
        string date_limite
        string date_debut
        string date_fin
        int id_formation FK
    }
    registres {
        string type_registre PK
        int code_registre PK
        string titre
        string statut
        string niveau_sortie
        string certificateur_nom
        int siret
        blob url
    }
    nsf {
        int nsf_code PK
        string nsf_nom
    }
    formacodes {
        int formacode_code PK
        string formacode_nom
    }
    ass_formation_registre {
        int id_formaion PK, FK
        string type_registre PK, FK
        int code_registre PK, FK
    }
    ass_registre_nsf {
        int nsf_code PK, FK
        string type_registre PK, FK
        int code_registre PK, FK
    }
    ass_registre_formacode {
        int formacode_code PK, FK
        string type_registre PK, FK
        int code_registre PK, FK
    }
    formations ||--o{ sessions : a
    formations ||--|{ ass_formation_registre : a
    registres ||--|{ ass_formation_registre : a
    registres ||--|{ ass_registre_nsf : a
    nsf ||--|{ ass_registre_nsf : a
    registres ||--|{ ass_registre_formacode : a
    formacodes ||--|{ ass_registre_formacode : a

```