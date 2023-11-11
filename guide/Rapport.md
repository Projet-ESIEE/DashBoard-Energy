# <center>Rapport 23_E4_DSIA_4101A - Python pour la datascience :</center>


## Interprétation : 
Malgré un certain nombre de données manquantes, nous pouvons faire de nombreuses conclusions sur leurs interpretations. 
On constate à tous les niveaux une augmentation de la consommation d'énergie, des revenus et de l'IDH. 
De manière attendue les pays avec un fort IHD ont une forte consommation énergétique. 
De même, on constate une explosion des energies renouvelable, une possible interpretation est qu'en 2000, elles n'était pas utile comparé à maintenant ou les enjeux écologiques sont primordiaux.
Les comparaisons sont intéressants par régions ou par pays de même type (dévelopment économique, en voie de développement, etc.). 
L'histogramme de l'IDH montre vraiment bien augmentation de l'indice dans le temps, le box plot associé permet aussi bien de voir l'évolution de manière condensée. 
De manière générale, il y a une corrélation entre les variables (hormis les outliers et les na). 
Il serait intéressant de faire une régréssion linéaire avec toutes les variables pour prédire les na et constaté certaines tendances. 




## Axes d'améliorations :

#### Optimisation : 
La fonction `df_energy_query()` qui permet de filtrer le dataframe en fonction des DropDown coté front-end, est appellé 
plusieurs fois. Cette duplication n'est pas optimal. Deux optimisations sont vraisemblablement possibles : 
1. Réaliser le filtre lors grâce à un `callball()` et changer la valeur du dataframe qui est un variable `global`.
2. Utiliser `DCC.Store()`, l'option recommandé dans la documentation. Le souci est qu'il faille sérialiser le dataframe avant et apres. 

*Il n'est pas possible de partager un dataframe en output d'un callback et n'est pas envisageable d'avoir un dataframe par possibilitées.*

Patcher la méthode qui provoque de Futur warning

Comprendre pourquoi l'histogramme fait des siennes de temps à autre (le margin boxplot)/

#### Ajout : 
1. L'ajout de `components` avec un footer par exemple
2. Plus de CSS, notamment pour customizer les DBC.

## Copyright : 
Le code de `main.py` est largement inspiré de [ce repos GitHub](https://github.com/AnnMarieW/dash-multi-page-app-demos) et de la doc officiel. 
