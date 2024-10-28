import pandas as pd
import re

def data_cleaning(chemin_fichier):
    # 1. Lire le fichier texte et le diviser en paragraphes
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        paragraphes = fichier.read().split('\n')
    
    # 2. Créer un DataFrame avec les paragraphes
    df = pd.DataFrame({'Arabe': paragraphes})

    # 3. Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # 4. Suppression des lignes vides ou NaN
    df_nettoye = df.dropna().replace('', float('NaN')).dropna()

    # # 5. Filtrer les lignes où le texte contient "»" sans son pair "«"
    df_nettoye = df_nettoye[~((df_nettoye['Arabe'].str.contains('»')) & ~(df_nettoye['Arabe'].str.contains('«')))]

    # # 6. Filtrer les lignes où le texte contient "«" sans son pair "»"
    df_nettoye = df_nettoye[~((df_nettoye['Arabe'].str.contains('«')) & ~(df_nettoye['Arabe'].str.contains('»')))]

    # # 7. Supprimer les guillemets doubles
    #df_nettoye['Arabe'] = df_nettoye['Arabe'].str.replace('"', '', regex=False)

    # # 8. Supprimer les astérisques
    df_nettoye['Arabe'] = df_nettoye['Arabe'].str.replace('*', '', regex=False)
    
    

    # # 9. Supprimer les lignes avec une seule occurrence de "”"
    df_nettoye = df_nettoye[df_nettoye['Arabe'].str.count('”') != 1]

    # # 10. Supprimer les lignes avec une seule occurrence de "“"
    df_nettoye = df_nettoye[df_nettoye['Arabe'].str.count('“') != 1]

    # 11. Supprimer les lignes contenant des caractères latins (A-Z, a-z)
    df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains(r'[A-Za-z]', regex=True)]

    # # 11. Fonction pour compter les mots arabes dans une chaîne
    def compter_mots_arabes(texte):
        if pd.isna(texte):
            return 0
        mots_arabes = re.findall(r'\b[\u0600-\u06FF]+\b', texte)
        return len(mots_arabes)

    # 12. Garder les lignes où le nombre de mots arabes est supérieur à 4
    df_nettoye = df_nettoye[df_nettoye['Arabe'].apply(compter_mots_arabes) > 5]

    # # 13. Suppression des versets coraniques avec les délimiteurs '﴿'
    df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('﴿')]

    #14 suppression des lignes contenant "#"
    df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('#')]
    df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('"')]
  
    
    
    #15 suppression de l'espace entre mot et ponctuations
    df_nettoye = df_nettoye['Arabe'].str.replace(r'\s+([.])', r'\1', regex=True)

    #lignes contenant د en isolation
    #df_nettoye = df_nettoye[~df_nettoye.str.contains(r'\bد\b', regex=True)]

    #Remplace double points par un seul point:
    df_nettoye = df_nettoye.str.replace(r'\.{2,}', '.', regex=True)

    #suppression des lines contenant un seul » mais pas son opposé et vice-verça
    df_nettoye = df_nettoye.apply(lambda x: x.replace('»', '') if '»' in x and '«' not in x else x)
    df_nettoye = df_nettoye.apply(lambda x: x.replace('«', '') if '«' in x and '»' not in x else x)


    #Enlever les " 
    #df_nettoye = df_nettoye.str.replace('"', '', regex=False)

    

    return df_nettoye

#----------------------------------------------------------------------

if __name__ == "__main__":
    # Chemin vers le fichier texte
    chemin_fichier = 'E:/Mamadou Aw/NMT_PROJECT/Data from OPUS/Classification/Religion.txt'

    # Nettoyer les données à partir du fichier texte
    df_nettoye = data_cleaning(chemin_fichier)

    # Sauvegarder éventuellement les données nettoyées
    df_nettoye.to_csv('E:/Mamadou Aw/NMT_PROJECT/Data from OPUS/Classification/Religion_cleaned.txt', index=False)
