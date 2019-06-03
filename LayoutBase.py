import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
#import dash_bootstrap_components as dbc

import base64

from textwrap import dedent


tplOverview = 'Technology performance level (TPL) assessment is intended to provide a comprehensive and holistic measure of a wave energy converter’s (WEC) techno-economic performance potential. While the TPL assessments can be applied at all technology development stages and associated technology readiness levels (TRLs), this tool is aimed at assessing early stage concepts. This tool uses a series of questions in seven distinct categories to guide the assessor in evaluating a WEC. Each question addresses a specific aspect that impacts the techno-economic performance of a WEC. For each question, the reviewer must provide a score. Also, this tool is intended to evaluate a wide range of WEC architypes who’s techno-economic performance may be impacted differently by different evaluation criteria, each question has an associated weighting that can be customized by the assessor. The net TPL score is calculated for the score and weighting of each question.'

colors = {
    'background': '#ADD8E6',
    'text': '#4169E1'
}
buttonStyle = style={'textAlign': 'center',
						'display':'table-cell',
						'verticalAlign':'middle',
						'margin':'auto'}

def header():
        div = html.Div(
                style={'backgroundColor': colors['background']},
                children =[
                        html.H1('TPL ASSESSMENT TOOL',
                                style={
                                        'textAlign': 'left',
                                        'color': colors['text']
                                        }
                                ),
                        dcc.Store(id='tpl-assessment-store',storage_type='local'),
                        dcc.Store(id='capabilities-store',storage_type='local'),
                        dcc.Store(id='subCats-store',storage_type='local'),
                        dcc.Store(id='narrowC-store',storage_type='local'),
                        dcc.Store(id='specificC-store',storage_type='local'),
                        dcc.Store(id='qGroup-store',storage_type='local'),
                        dcc.Store(id='qChoiceGroup-store',storage_type='local'),
                        dcc.Store(id='qChoice-store',storage_type='local'),
						html.Div(id='dummy-out-1', style={'display':'none'}),
						html.Div(id='dummy-out-2', style={'display':'none'})
                        ]
        )
        return div

'''
# need to spend a bit of time getting static files to work correctly
def logo(image_filename = './static/logo.png'):
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        return html.Img(src='data:image/png;base64,{}'.format(encoded_image))
'''
        
def top_Divs_Base():
        div = html.Div(id='top-background-div',
				children=[
						html.Button('Start Fresh TPL Assessment',
												title='Click this to begin a new TPL Assessment',
												id='standard-load-button',
												style=buttonStyle,
												className='four columns'),
						html.Div(id='capabilities-dropdown-div',
								children=[
										dcc.Dropdown(
												id='capabilities-dropdown',
												options = [{'label':'No TPL Assessment Loaded',
																'value':'NoTPL'}],
												placeholder='No TPL Assessment Loaded',
										)
								],
								style={'visible':False},
								className='four columns'),
						html.Div([
							dcc.ConfirmDialogProvider(
								children=html.Button('TPL?',
											className='twelve columns'),
								id='overview-button',
								message=f'{tplOverview}')
						],id='overview-div',className='two columns')
				],style={'background':'#F0FEFE'},
				className='twelve columns')
        return div

def bot_Divs_Base():
        div = html.Div(id='bot-background-div',
                        children=[
                                html.Div(left_div_preamble(),
                                id='left-div',
                                hidden=True,

                                className='twelve columns'),
								html.Div([

                                html.Div([
                                        html.Div(id='bot-left-div-1',
                                        className='twelve columns'),
                                        html.Div(id='bot-left-div-2',
                                        className='twelve columns'),
                                        html.Div([
                                                dcc.Dropdown(id='numQuestions-dropdown',

															options=[{'label':'noQ','value':'noQ'}],
															value=None,
															placeholder="Select Question"
															),
                                        ],id='bot-left-div-3',

                                        className='twelve columns')
                                        ],id='bot-left-div',
                                        className='six columns'),
                                html.Div([
                                        html.Div(
											children=bot_right_div_1_preamble(),
											id='bot-right-div-1',
                                        className='twelve columns'),
                                        html.Div(id='bot-right-div-2',
                                        className='twelve columns'),
                                        html.Div(id='bot-right-div-3',
                                        className='twelve columns'),
                                ],
                                id='bot-right-div',
                                className='six columns')
                        ]),
						],
                        className='twelve columns'
                )
        return div
    
def bot_Divs_Base2():
        div = html.Div(id='bot-background-div2',
                        children=[
                                html.Div([
                                        html.Div(id='bot-right-div-6',
                                        className='twelve columns'),
                                        html.Div(id='bot-right-div-7',
                                        className='twelve columns'),
                                        html.Div(id='bot-right-div-8',
                                        className='twleve columns'),                                        
                                        html.Div(right_div_preamble(),
                                        id='right-div',
                                        hidden=False,
                                        className='six columns'
                                        , style={'marginleft': 5000000000000000, 'marginTop': 25}) 
                                        ],
                                        ),                                      
                                        ],
                        className='twelve columns'
                )
        return div

def left_div_preamble():

        return [html.Div([
                        html.H5('Narrow Index:'),
                        html.Div(
                        dcc.Dropdown(id='narrowC-dropdown',
                                options=[{'label':'Select Device Capabilities',
                                                'value':'NoCG'}],
                                value=None,
                                placeholder="Select Device Capabilities"
                                ),id='left-div-1')],
                        id='q1-holder',
                        className='four columns'
                        ),
                html.Div([
                        html.H5('Specific Index:'),
                        html.Div(
                        dcc.Dropdown(id='specificC-dropdown',
                                options= [{'label':'Select Capability Group',
                                                'value':'NoCG'}],
                                value=None,
                                placeholder="Select Capability Group"
                                ),id='left-div-2')],
                        id='q2-holder',
                        className='four columns'
                        ),
                html.Div([
                        html.H5('Question Index:'),
                        html.Div(
                        dcc.Dropdown(id='qGroup-dropdown',
                                options= [{'label':'Select Question Group',
                                                'value':'NoQG'}],
                                value=None,
                                placeholder="Select Question Group"
                                ),id='left-div-3')],
                        id='q3-holder',
                        className='four columns'
                        )
        ]


def right_div_preamble():
    
        return [html.Div(#[
#                        html.H5('Plot:'),
                        html.Div(id='test-graph'),
#                        html.Div(dcc.Graph(
#                                id='test-graph',
#                                figure={
#                                       'data': [{'values': [20,20,20,20],'type' : 'pie'}],
#                                        'layout': {
#                                                'title': 'Dash Data Visualization'
#                                                    },
#                                                'legend': {'x': 0, 'y': 1, 'z': 2}
#                                        }
#        
#                                    )
#                               # id='left-div-new'
#                                )
#                        
#                                ],
                                id='q1-holdernew',
                        className='eleven columns'
                        ),
                    html.Div(id='q2-holdernew',className='eleven columns'),
                    html.Div(id='q3-holdernew',className='eleven columns'),
                        
#                                                #layout=go.Layout(
#                                                       # title='US Export of Plastic Scrap',
#                                                      #  showlegend=True,
#                                                      #  legend=go.layout.Legend(
#                                                       #         x=0,
#                                                        #        y=1.0
#                                                        #        ),
#                                                        #margin=go.layout.Margin(l=40, r=0, t=40, b=30)
#                                                      #  )
                                             #  )
                                   # style={'height': 300},
                                   # id='my-graph'
 
                                    
                                    ]                                                                
                            

def bot_right_div_1_preamble():
        return [html.Div(id='net-score-div'),
						dcc.Input(placeholder='Enter your Score',
								id='contribution-weight',
								type='number',
								value=0,
								min=0,max=10,
								debounce = True,
								className='four columns'),
				html.Div([
					html.Div([
						dcc.ConfirmDialogProvider(
						children=html.Button('',
									className='twelve columns'),
						id='background-button',
						message=''),
						dcc.ConfirmDialogProvider(
						children=html.Button('',
									className='twelve columns'),
						id='score-button',
						message=f'')
					],className='four columns'),
					html.Div([
						html.Div([html.Div(children=''),
									dcc.Input(placeholder='',
											id='question-score',
											type='number',
											value='',
											min=0,max=10,
											className='twelve columns'
									)],className='six columns'),
						html.Div([html.Div(''),
									dcc.Input(placeholder='',
											id='question-weight',
											type='number',
											value='',
											min=0,max=10,
											className='twelve columns'
									)
									],className='six columns'),
								html.Button('',
										id = 'score-sub-button',
										className='twelve columns')
					],className='eight columns')
				],className='twelve columns')
				
				]








