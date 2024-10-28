#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import redis
import os

def main():
    # Spécifiez le chemin du fichier texte d'entrée
    chemin = 'E:/Mamadou Aw/NMT_PROJECT/Cleaned Data/Eljezzira/Eljezzira_all_in_one1_sorted.txt'

    try:
        # Lecture du fichier texte et traitement des paragraphes
        with open(chemin, 'r', encoding='utf-8') as fichier:
            paragraphs = fichier.read().replace('\n', '').split('.')

        # Création d'un DataFrame avec une colonne 'Arabic'
        df = pd.DataFrame({'Arabic': paragraphs})

        # Affichage du DataFrame
        #print(df)

        # Connexion à Redis
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        # Itération et stockage de chaque paragraphe dans Redis
        for index, row in df.iterrows():
            redis_client.set(index, row['Arabic'])

        # # Vérification
        # print("Valeurs stockées dans Redis :")
        # for index in df.index:
        #     print(f"Clé : {index}, Valeur : {redis_client.get(index)}")

    except FileNotFoundError:
        print(f'Erreur : Le fichier {chemin} n\'a pas été trouvé.')
    except redis.ConnectionError:
        print('Erreur : Impossible de se connecter à Redis.')
    except Exception as e:
        print(f'Une erreur est survenue : {e}')

if __name__ == '__main__':
    main()
