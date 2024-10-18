from dash import html
import dash_bootstrap_components as dbc


header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 70}),
            html.H1("МОНИТОРИНГ СОСТОЯНИЯ КОМПЬЮТЕРА", className="text-center"),
        ]
    ),
    className="mb-4",
)



tabs_styles = {
    'height': '90px'
}

tab_style = {
    'padding': '11px',
    'fontWeight': 'bold',
    'borderBottom': '2px solid #B179EA',
    'borderTop': '2px solid #B179EA',
    'font-size': '40px',
}

tab_selected_style = {
    'backgroundColor': '#B179EA',
    'color': 'black',
    'padding': '11px',
    'borderBottom': '2px solid #B179EA',
    'borderTop': '2px solid #B179EA',
    'font-size': '40px'
}
