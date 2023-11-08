# Rapport : 
un rapport d’analyse qui met en avant les principales conclusions extraites des données ;
## Interprétation : 


## Axes d'améliorations :

#### Optimisation : 
La fonction `df_energy_query()` qui permet de filtrer le dataframe en fonction des DropDown coté front-end, est appellé 
plusieurs fois. Cette duplication n'est pas optimal. Deux optimisations sont vraisemblablement possibles : 
1. Réaliser le filtre lors grâce à un `callball()` et changer la valeur du dataframe qui est un variable `global`.
2. Utiliser `DCC.Store()`, l'option recommandé dans la documentation. Le souci est qu'il faille sérialiser le dataframe avant et apres. 

*Il n'est pas possible de partager un dataframe en output d'un callback et n'est pas envisageable d'avoir un dataframe par possibilitées.*


#### Ajout : 
1. L'ajout de `components` avec un footer par exemple
2. Plus de CSS, notamment pour customizer les DBC.

## Copyright : 
Le code de `main.py` est largement inspiré de [ce repos GitHub](https://github.com/AnnMarieW/dash-multi-page-app-demos)
