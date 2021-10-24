# Hearhston-o-tron

- Sujet : Projet de modélisation mathématique d'introduction à l'intélligence artificielle.<br />
- Auteurs : Gaspard ANDRIEU et Maxime POULAIN<br />
- Technologies utilisées : Python 3.7, Pygame 1.9.6, Numpy, Pandas, Tqdm.
> Ces dernières sont indispensables au fonctionnement de l'application.

## Mise en contexte

- Le but du projet est de créer une IA capable de battre un joueur moyen sur une version très simplifiée de Hearthstone.<br />
- Bien que notre version soit très simplifiée, celle-ci reste quand même complexe et permet approximativement 600000 mouvements
différents.<br />
- Pour arriver à nos fins, il nous faut tout d'abord recréer Hearthstone pour pouvoir avoir le support pour tester l'IA.<br />
- Mais ce n'est pas tout. Il faut ensuite créer un jeu de données sur les actions possibles pour un joueur. Nous avons
donc mis au point un algorithme simple qui joue toutes ses parties aléatoirement afin de récolter des informations
sur tous les mouvements possibles. <br />
- Pour un mouvement donnée, on récupère son contenu et son "winrate" *(Pourcentage de parties gagnées en effectuant ce mouvement)*.<br />
En faisant cela sur des millions de parties, nous pourrons obtenir un jeu de données fiable et complet. L'IA est alors entraînée
(avant même d'avoir réellement été créée).<br />
- Et enfin, on peut enfin créer l'IA finale, qui va essayer de tout le temps jouer le meilleur mouvement possible, d'après les données récoltées dans la BDD.<br />

## Notice d'utilisation

Après avoir téléchargé le programme, plusieurs choix s'offrent à vous :
- Entrainer l'IA : Exécuter ConsoleTest.py
- Jouer contre l'IA : Exécuter Main.py
- Librairies à installer : numpy, pandas, tqdm, matplotlib, pygame
- Configuration de l'affichage : 
	* APP_SCALE = 1 -> 1280 x 720 
	* APP_SCALE = 1.5 -> 1920 x 1080 
	* APP_SCALE = 2 -> 2560 x 1440 

## Conseils pour mieux comprendre le projet

**Avant toute chose**<br />
Certain fichiers sont devenu inutile car nous n'avons pas eu le temps d'implémenter ses fonctionnalités (notamment tout ce qui est en lien avec les *Weapon* et les *Spell*).

**Liste des dossiers et petite description**<br />

- Components<br />
> Tout type d'objets instanciés pendant une partie.

- Data<br />
> Implémentation dynamique d'un dictionnaire contenant toute les cartes jouables, mais aussi la gestion de la base de données des coup possible en pleine partie.

- Definitions<br />
> Des classes de stockages, contenant toute l'information statique une fois le programme lancé.

- Player<br />
> Des classes ayant peu d'utilités, mais concernant les joueurs (permet par exemple de savoir quel est le premier joueur).

- Resources<br />
> Images, musiques, et polices d'écriture.

- Utils<br />
> Constantes (paramètres) et fonctions utilisées dans tout le programmes.

- venv<br />
> Ne pas y toucher ! Ce sont les dépendances du programme, générées automatiquement.

<br />

**Oui, mais elle est ou l'IA dans tout ca ?**<br />
Dans aucun des dossiers cités au dessus. L'algorithme de résolution se trouve dans le fichier Game.py (à la racine du projet) et commence vers la ligne 170. Cet algorithme fait appel à 7 fonctions qui sont écrites juste en dessous. Ces dernières sont commentées, tout comme l'algorithme afin d'avoir une idée précise de comment l'IA joue. Quant à la base de données utilisée par l'IA, elle se trouve dans de dossier Data. Les fichier DataCollector y donne un accès en lecture seule, et DataSerializer un accès d'écriture contrôllée.<br />