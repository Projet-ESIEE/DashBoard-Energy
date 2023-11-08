# <center>Developer Guide :</center> 

The purpose is to allows you to understand the architecture of the code and modify or extend it.

--- 

## Project structure : 
### Mermaid magic: 
```mermaid
graph TB

%% Directories
run(Run) -->|Executes| mainpy(Main.py)
assets(Assets) -->|Static files| assetsFiles
dataset(Dataset) -->|Data files| datasetFiles
guide(Guide) -->|Documentation| guideFiles
pages(Pages) -->|Web Pages| home(Home)
pages --> analytics1(Analytics 1)
pages --> analytics2(Analytics 2)
pages --> guide1(Guide 1)
pages --> guide2(Guide 2)

%% Files
mainpy(Main.py)
.gitignore(.gitignore)
LICENSE(LICENSE)
README(README.md)
requirement(requirement.txt)

%% Subdirectories
subgraph assetsFiles[Static Files]
    image1[Favicon]
    image2[404.gif]
    image3[style.css]
end

subgraph datasetFiles[Data Files]
    data1[global-data-sustainable-energy.csv]
    data2[countryContinent.csv]
    data3[human-development-index.csv]
   
end

subgraph guideFiles[Documentation]
    doc1[User Guide]
    doc2[Developer Guide]
    doc3[Rapport]
end
```


### Multi-pages :
This multi-pages repository is set like the [official documentation](https://dash.plotly.com/urls) guidelines.

Here were going through each folder and give a little detail of what is it.
- The `.run` folder is a default folder for the running configuration (made by PyCharm itself)
- The asset system is detailed [here](https://dash.plotly.com/external-resources).
- The dataset folder contain each dataset csv and the ipython notebook associated to the data cleaning and aggregation.
- The guide folder contain some markdown files
- The **Pages** folder contain a .py file per pages on the Dash app. 
- The **main.py** is the entry point of the project. It is the luncher of the dash app.
- The `.gitignore` is the file which indicate the file and folder to do not commit and push on the git repo (set by GitHub and modify by us)
- The `LICENSE` is the file which indicate under which condition the project could be used. (set by GitHub) 
- The `README.md` fie is the landing page on GitHub. contain a brief description of the project.
- The `requirement.txt` is the list of all necessary dependency with the version.


```mermaid
---
title: Dash app Flow chart
---
flowchart TD
subgraph "Run the App"
  main{{main.py}} -- "call" --> analytics1{{missing values.py}}
  analytics1{{missing values.py}} -- plots ----> heatmap[/heatmap/]
  analytics1{{missing values.py}} -- plots ----> histo[/histo/]
  analytics1{{missing values.py}} -- plots ----> line[/line/]
  analytics1{{missing values.py}} -.query .-> df_energy

  main{{main.py}} -- "call" --> analytics2{{maps.py}}
  analytics2{{maps.py}} -.query .-> df_energy
  analytics2{{maps.py}} -- plots ----> maps[/histo/]
  analytics2{{maps.py}} -- plots ----> pie[/line/]

  main{{main.py}} -- "call" --> home{{home.py}}
  home{{home.py}} -- display --> readme.md

  main{{main.py}} -- "call" --> guide1{{userGuide.py}}
  guide1{{userGuide.py}} -- display --> userguide.md

  main{{main.py}} -- "call" --> guide2{{devGuide.py}}
  guide2{{devGuide.py}} -- display --> devGuide.md
end


subgraph "Build our dataset"
  process_data{{process_data.ipynb}} -- "read" --> db[(.csv)]
  db[(.csv)] -- "process + clean + merge" -->  dataframes
  dataframes -- plots --> box[/box plots/]
  dataframes -- create ---> df_energy.
end
```



## How to Guide : 

### Add an element to the Dash app layout : 
```python
layout = html.Div(
    className="new-element-class",
    children=[
        html.H1('This a heading 1'),
    ]
```

### customise the Dash app : 
['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
 'ylorrd'].

### Theming plotly : 
"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"
