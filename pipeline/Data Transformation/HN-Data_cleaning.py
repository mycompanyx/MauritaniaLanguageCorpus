import pandas as pd
import re


def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FAFF"  # Chess Symbols
        "\U00002702-\U000027B0"  # Dingbats
        "\u2600-\u26FF"          # Misc symbols
        "\u2700-\u27BF"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r'', text)


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
    # df_nettoye = df_nettoye[~((df_nettoye['Arabe'].str.contains('»')) & ~(df_nettoye['Arabe'].str.contains('«')))]

    # # 6. Filtrer les lignes où le texte contient "«" sans son pair "»"
    # df_nettoye = df_nettoye[~((df_nettoye['Arabe'].str.contains('«')) & ~(df_nettoye['Arabe'].str.contains('»')))]

    # # 7. Supprimer les guillemets doubles
    # df_nettoye['Arabe'] = df_nettoye['Arabe'].str.replace('"', '', regex=False)

    # # 8. Supprimer les astérisques
    #df_nettoye['Arabe'] = df_nettoye['Arabe'].str.replace('*', '', regex=False)
    
    

    # # 9. Supprimer les lignes avec une seule occurrence de "”"
    # df_nettoye = df_nettoye[df_nettoye['Arabe'].str.count('”') != 1]

    # # 10. Supprimer les lignes avec une seule occurrence de "“"
    # df_nettoye = df_nettoye[df_nettoye['Arabe'].str.count('“') != 1]

    # 11. Supprimer les lignes contenant des caractères latins (A-Z, a-z)
    df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains(r'[A-Za-z]', regex=True)]

    # # 11. Fonction pour compter les mots arabes dans une chaîne
    def compter_mots_arabes(texte):
        if pd.isna(texte):
            return 0
        mots_arabes = re.findall(r'\b[\u0600-\u06FF]+\b', texte)
        return len(mots_arabes)

    # # 12. Garder les lignes où le nombre de mots arabes est supérieur à 4
    df_nettoye = df_nettoye[df_nettoye['Arabe'].apply(compter_mots_arabes) > 1]

    # # 13. Suppression des versets coraniques avec les délimiteurs '﴿'
    # df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('﴿')]

    # #14 suppression des lignes contenant "#"
    # df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('#')]
    # df_nettoye = df_nettoye[~df_nettoye['Arabe'].str.contains('"')]
  
    
    
    #15 suppression de l'espace entre mot et ponctuations
    # df_nettoye = df_nettoye['Arabe'].str.replace(r'\s+([.])', r'\1', regex=True)

    # #lignes contenant د en isolation
    # #df_nettoye = df_nettoye[~df_nettoye.str.contains(r'\bد\b', regex=True)]

    # #Remplace double points par un seul point:
    # df_nettoye = df_nettoye.str.replace(r'\.{2,}', '.', regex=True)

    #suppression des lines contenant un seul » mais pas son opposé et vice-verça
    # df_nettoye = df_nettoye.apply(lambda x: x.replace('»', '') if '»' in x and '«' not in x else x)
    # df_nettoye = df_nettoye.apply(lambda x: x.replace('«', '') if '«' in x and '»' not in x else x)


    #Enlever les " 
    #df_nettoye = df_nettoye.str.replace('"', '', regex=False)

    

    df_nettoye = df_nettoye['Arabe'].apply(remove_emojis)
   

    return df_nettoye

#----------------------------------------------------------------------

if __name__ == "__main__":
    # Chemin vers le fichier texte
    chemin_fichier = 'C:/Users/USER/Desktop/Project/DATA/FB_Comments_HN/HN_cleaned_sen1_sorted.txt'
    # Nettoyer les données à partir du fichier texte
    df_nettoye = data_cleaning(chemin_fichier)

    # Sauvegarder éventuellement les données nettoyées
    df_nettoye.to_csv('C:/Users/USER/Desktop/Project/DATA/FB_Comments_HN/HN_cleaned2.txt', index=False)
