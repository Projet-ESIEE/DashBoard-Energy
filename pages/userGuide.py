import dash
from dash import html, dcc

dash.register_page(
    __name__,
    name="User guide",
    guide=True,
)


layout = html.Div(
    className="content",
    children=[
        html.H1('This is our User guide page'),
        dcc.Markdown(
            """
            This file lets you deploy and use your dashboard on another machine
            
            ## How to clone the git repo
            `git clone https://github.com/Projet-ESIEE/DashBoard-Energy`
            
            ## librairy used and Requirements: 
            Check the `requirement.txt` to get the list of dependency and the version used for running the app.
            Plotly is the only librairy used to plot graph. Dash is then used to power the dashboard. 
            Of course Pandas and Numpy are use all around the project. (seaborn is not mandatory)
            
            `pip install -r requirements.txt` to install all the dependency.
            
            *To get the list of dependency :*
            ```shell
            pip install pipreqs 
            pipreqs
            ```
            ### Launch the app
            `python main.py` or use the `main.run.xml` in .run folder for PyCharm user.
            """
        ),
    ],
)
