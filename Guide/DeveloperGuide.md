# Developer Guide : 


Faire un df avec idh par tranche + continent pour comprendre les outliers et les na

### To do : 
1. typage des données 
   1. les transformé en numpy ? 
2. ajouter les continents en mode hot-one encoding
3. ajouter l'IDH
4. mise a l'échelle ? 
5. identifier les types de données manquantes
6. identifier les outliers 

--- 

## Project structure : 
```shell
- assets/
  |-- style.css
- dataset
- Guide
- pages
   |-- analytics.py
   |-- home.py
   |-- archive.py
  - components
    |-- footer.py
    |-- ....py
- app.py
- .gitignore
- LICENSE
- process_data.ipynb
- README.md
- tools.py
```

## Multi-pages :
The multi-pages property is set just like in the [official documentation](https://dash.plotly.com/urls).

The asset system is detailed [here](https://dash.plotly.com/external-resources).
