import dash
from dash import html, dcc

dash.register_page(__name__, order=3)


markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

layout = html.Div(
    className="content",
    children=[
        html.H1('This is our user guide page'),
        dcc.Markdown(children=markdown_text),
        html.Div('...'),
        html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quam est, ultrices egestas sapien a, interdum tempus arcu. Sed sed porta turpis. Praesent malesuada, augue vulputate commodo commodo, felis dui fermentum odio, a maximus neque urna eget purus. Donec tempus auctor molestie. Sed varius mattis magna et iaculis. Donec pharetra orci vitae urna rutrum, non vulputate felis eleifend. Sed tincidunt volutpat elementum. Morbi fermentum vehicula sem ut volutpat. Phasellus blandit tortor ante, eleifend vulputate libero accumsan sed. Aenean a mattis magna. Nam vehicula non odio sed vulputate. Nullam malesuada neque vulputate, tristique quam non, fermentum nunc. Praesent feugiat, metus non congue semper, ante lectus feugiat orci, a interdum lacus ligula eget lectus. Sed quis tellus egestas, tristique leo et, interdum sapien. Curabitur rutrum mi vitae ligula pulvinar fringilla. Aenean cursus volutpat sem ut elementum. Morbi sed arcu in lorem ullamcorper volutpat a vel orci. Donec in tincidunt leo. Integer tempus efficitur nisi vel porttitor. Donec vel fringilla quam, ac sollicitudin diam. Nam vel ante lorem. Vivamus aliquet purus in magna semper, quis tempor orci volutpat. Cras neque diam, lobortis ac sem vitae, pharetra ultricies nisi. Praesent ut ullamcorper erat.'),
        html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quam est, ultrices egestas sapien a, interdum tempus arcu. Sed sed porta turpis. Praesent malesuada, augue vulputate commodo commodo, felis dui fermentum odio, a maximus neque urna eget purus. Donec tempus auctor molestie. Sed varius mattis magna et iaculis. Donec pharetra orci vitae urna rutrum, non vulputate felis eleifend. Sed tincidunt volutpat elementum. Morbi fermentum vehicula sem ut volutpat. Phasellus blandit tortor ante, eleifend vulputate libero accumsan sed. Aenean a mattis magna. Nam vehicula non odio sed vulputate. Nullam malesuada neque vulputate, tristique quam non, fermentum nunc. Praesent feugiat, metus non congue semper, ante lectus feugiat orci, a interdum lacus ligula eget lectus. Sed quis tellus egestas, tristique leo et, interdum sapien. Curabitur rutrum mi vitae ligula pulvinar fringilla. Aenean cursus volutpat sem ut elementum. Morbi sed arcu in lorem ullamcorper volutpat a vel orci. Donec in tincidunt leo. Integer tempus efficitur nisi vel porttitor. Donec vel fringilla quam, ac sollicitudin diam. Nam vel ante lorem. Vivamus aliquet purus in magna semper, quis tempor orci volutpat. Cras neque diam, lobortis ac sem vitae, pharetra ultricies nisi. Praesent ut ullamcorper erat.'),
        html.P('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quam est, ultrices egestas sapien a, interdum tempus arcu. Sed sed porta turpis. Praesent malesuada, augue vulputate commodo commodo, felis dui fermentum odio, a maximus neque urna eget purus. Donec tempus auctor molestie. Sed varius mattis magna et iaculis. Donec pharetra orci vitae urna rutrum, non vulputate felis eleifend. Sed tincidunt volutpat elementum. Morbi fermentum vehicula sem ut volutpat. Phasellus blandit tortor ante, eleifend vulputate libero accumsan sed. Aenean a mattis magna. Nam vehicula non odio sed vulputate. Nullam malesuada neque vulputate, tristique quam non, fermentum nunc. Praesent feugiat, metus non congue semper, ante lectus feugiat orci, a interdum lacus ligula eget lectus. Sed quis tellus egestas, tristique leo et, interdum sapien. Curabitur rutrum mi vitae ligula pulvinar fringilla. Aenean cursus volutpat sem ut elementum. Morbi sed arcu in lorem ullamcorper volutpat a vel orci. Donec in tincidunt leo. Integer tempus efficitur nisi vel porttitor. Donec vel fringilla quam, ac sollicitudin diam. Nam vel ante lorem. Vivamus aliquet purus in magna semper, quis tempor orci volutpat. Cras neque diam, lobortis ac sem vitae, pharetra ultricies nisi. Praesent ut ullamcorper erat.'),
    ]
)
