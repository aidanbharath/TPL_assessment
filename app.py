import sys
import uuid
sys.setrecursionlimit(5000)

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from flask_caching import Cache 
import plotly.graph_objs as go
import numpy as np

from pyfladesk import init_gui

from LayoutBase import colors, header, top_Divs_Base, bot_Divs_Base,bot_Divs_Base2
from load import (base_load_template,
					cache_create_template,
					temp_load_assessment,
					create_user_template,
					load_user_template,
					save_user_template)
from calculate import (calc_input_scores,
						calc_second_level_group_score,
						calc_third_level_group_score)

import pandas as pd

idxCols = ['Broad Capability','Narrow Capability','Specific Capability']

app = dash.Dash(__name__,static_folder='static')
app.config.suppress_callback_exceptions = False
server = app.server

# Here we going to enable session based user data caching ... hopefully
# current setup to run on local filesystem
cache = Cache(server, config={
    #'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './cache/',
    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
})



# ok so .to_json() requires a unique index for each columns so .set_index() breaks it
def init_user_dataframe(session_id):
	@cache.memoize()
	def create_and_serialize_data(session_id):
		df = cache_create_template()
		return df.to_json()
	return pd.read_json(create_and_serialize_data(session_id))

# with the session file created, we need to use the same logic to first write then read

def update_user_cache(session_id):
	#ud = pd.read_json(f'./cache/{session_id}')
	#print(ud)
	@cache.memoize()
	def load_data(session_id):
		return df.to_json()
	#print(store_data(session_id,ud))
	return pd.read_json(store_data(session_id))



app.run = app.run_server

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    #"https://cdn.rawgit.com/amadoukane96/8f29daabc5cacb0b7e77707fc1956373/raw/854b1dc5d8b25cd2c36002e1e4f598f5f4ebeee3/test.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})


def serve_layout():
	session_id = str(uuid.uuid4())
	session_div = html.Div(session_id, id='session-id', style={'display': 'none'})

	return html.Div([session_div,header(),top_Divs_Base(),bot_Divs_Base(),bot_Divs_Base2()],
						id='full-div',style={'background':'#F0FEFE'})

app.layout = serve_layout()


#################################
'''
These callbacks are meant to read the assessment tool basefile 
from the static folder. This effort is done so that changes to 
the basefile are automatically accounted for in the app.
'''
#################################

@app.callback(Output('tpl-assessment-store','data'),
                [Input('standard-load-button','n_clicks'),
				Input('session-id','children')], # Access to cache id
                [State('tpl-assessment-store','data')])
def load_base_tpl_assessment_package(click,sid,data):
	
	if click and not data:
		df = init_user_dataframe(sid)
		print(type(df))
		df.set('Score') = 10
		print(df.get('Score'))
		return True


@app.callback(Output('capabilities-dropdown-div','children'),
                [Input('tpl-assessment-store','data')],
				[State('session-id','children'),
				State('capabilities-dropdown-div','children')])
def set_tpl_assessment_options(data,sid,Div):
	if data and sid:
		df = init_user_dataframe(sid)
		options =  [{'label':names,'value':names} for names in df[idxCols[0]].unique()]
		return dcc.Dropdown(
                    id='capabilities-dropdown',
                    options = options,
                    placeholder='Select Capability',
                    value=None
                )
	else:
		return Div

# Begin new callback for plot
    
@app.callback(Output('q1-holdernew','children'),
                [Input('tpl-assessment-store','data')])
def set_tpl_assessment_plot(capabilities):
    if capabilities:
       
        
        plot_options=[{'label':capabilities,'value':[10,10,10,10,10,10,10],'type':'pie',}]
        #print(plot_options)
        df=calc_input_scores()
        
        df2=calc_third_level_group_score()
        df3=calc_second_level_group_score()
        #print(df2)
        cats=[]
        for j in capabilities:
            #print(j)
            baseTemplate = base_load_template()
            subCats = baseTemplate.loc[j].index.get_level_values(0).unique().values
            cats=np.append([cats],[subCats])
            
        trace1 = figure={'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        trace2= figure= {'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        #print(df3['Net'])
        
        return html.Div([
                        
                        #dcc.Graph(id='test-graph'),
                        html.Div(dcc.Graph(
                                id='test-graph',
                                #figure={ 'data' : [trace1,trace2],
                                       figure={'data': [{'x': capabilities,'y': df2[capabilities],'type' : 'bar',
                                                 'hoverinfo':'labels + df2["Scores"]',},],
                                        'layout': {
                                                'title': 'TPL Capabilities Score',
                                                'showlegend': False},
                                        }
        
                                    )
                               # id='left-div-new'
                                )
                        
                                ],
                               # id='q1-holdernew',
                        className='eleven columns'
                        ),             
                        

#end plot callback


# Begin new callback for plot-2
    
@app.callback(Output('q2-holdernew','children'),
                [Input('capabilities-dropdown','value')])
def set_tpl_assessment_plot_subcat(options):
    while options:
       
        
       # plot_options=[{'label':capabilities,'value':[10,10,10,10,10,10,10],'type':'pie',}]
        #print(options)
        df=calc_input_scores()
        
        df2=calc_third_level_group_score()
        df3=calc_second_level_group_score()
        
        #print(df3.loc[options,'RW'])
        cats=[]
#        for j in capabilities:
#            #print(j)
        baseTemplate = base_load_template()
        subCats = baseTemplate.loc[options].index.get_level_values(0).unique().values
#            cats=np.append([cats],[subCats])
        #print(df3.loc[options,'Score'])    
       # trace1 = figure={'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        #trace2= figure= {'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        #print(df3['Net'])
   
        return html.Div([
                        
                        #dcc.Graph(id='test-graph'),
                        html.Div(dcc.Graph(
                                id='test-graph2',
                                #figure={ 'data' : [trace1,trace2],
                                       figure={'data': [{'x': subCats,'y': df3.loc[options,'Score'],'type' : 'bar',
                                                 'hoverinfo':'labels + df2["Score"]',},],
                                        'layout': {
                                                'title': 'TPL Sub_Catagory Score',
                                                'showlegend': False},
                                        }
        
                                    )
                               # id='left-div-new'
                                )
                        
                                ],
                               # id='q1-holdernew',
                        className='eleven columns'
                        ),             
                        

#end plot callback
'''
@app.callback(Output('subCats-store','data'),
                [Input('capabilities-dropdown','value')])
def set_subCats_store(options):
    if options:
        return options
'''

################################
'''
Now we would like to start narrowing down what we are looking at
selections are made possible through successive dropdowns
'''
################################

@app.callback(Output('left-div','hidden'),
                [Input('subCats-store','data')])
def break_left_hidden(value):
	if value:
		return False

@app.callback(Output('left-div-1','children'),
                [Input('capabilities-dropdown','value')],
				[State('session-id','children')])
def set_tpl_assessment_second_level_selection_1(value,sid):

	if value:        
		df = init_user_dataframe(sid)
		subCats = df[df[idxCols[0]]==value][idxCols[1]].unique()
		options = [{'label':subcat,'value':subcat} for subcat in subCats]

		dropDowns = [dcc.Dropdown(id='narrowC-dropdown',
								options=options,
								value=None,
								placeholder="Select Device Capabilities"
								)]
		return dropDowns
	else:
		return  [dcc.Dropdown(id='narrowC-dropdown',
						options=[{'label':'Select Device Capabilities',
										'value':'NoCG'}],
						value=None,
						placeholder="Select Device Capabilities"
						)]

@app.callback(Output('left-div-2','children'),
                [Input('narrowC-dropdown','value')],
                [State('capabilities-dropdown','value'),
				State('session-id','children')])
def set_tpl_assessment_second_level_selection_2(ndata,value,sid):

	if ndata:
		df = init_user_dataframe(sid)
		subCats = df[(df[idxCols[0]]==value)&(df[idxCols[1]]==ndata)][idxCols[2]].unique()
		options = [{'label':subcat,'value':subcat} for subcat in subCats]

		dropDowns = [dcc.Dropdown(id='specificC-dropdown',
								options=options,
								value=None,
								placeholder="Select Device Capabilities"
								)]
		return dropDowns
	else:
		return  [dcc.Dropdown(id='specificC-dropdown',
						options=[{'label':'Select Specific Capabilities',
										'value':'NoCG'}],
						value=None,
						placeholder="Select Specific Capabilities"
						)]

@app.callback(Output('left-div-3','children'),
                [Input('specificC-dropdown','value')],
				[State('narrowC-dropdown','value'),
            	State('capabilities-dropdown','value'),
				State('session-id','children')])
def set_tpl_assessment_second_level_selection_3(sdata,ndata,value,sid):

	if sdata:
		df = init_user_dataframe(sid)
		df = df[(df[idxCols[0]]==value)&(df[idxCols[1]]==ndata)]
		tpl = temp_load_assessment()
		subCats = tpl[(tpl[idxCols[0]]==value)&(tpl[idxCols[1]]==ndata)&(tpl[idxCols[2]]==sdata)]
		subCats = subCats['Question Group Description'].unique()
		options = [{'label':subcat,'value':subcat} for subcat in subCats]

		return [dcc.Dropdown(id='qGroup-dropdown',
								options=options,
								value=None,
								placeholder="Select Device Capabilities"
								)]
	
	else:
		return  [dcc.Dropdown(id='qGroup-dropdown',
						options=[{'label':'Select Device Capabilities',
										'value':'NoCG'}],
						value=None,
						placeholder="Select Device Capabilities"
						)]

	
# Begin new callback for plot-3
    
@app.callback(Output('q3-holdernew','children'),
                [Input('narrowC-dropdown','value')],
                [State('subCats-store','data')])
def set_tpl_assessment_plot_subcat(ndata,value):
    while value:
        print(value)
        print(ndata)
        

        df=calc_input_scores()
        
        df2=calc_third_level_group_score()
        df3=calc_second_level_group_score()
        
        #print(df3.loc[options,'RW'])
        cats=[]
#        for j in capabilities:
#            #print(j)
        userTemplate = load_user_template()
        subcats=df.loc[value].loc[ndata].index.get_level_values(0).unique().values
        print(subcats)
        #subCats = userTemplate.loc[value,ndata].index.get_level_values(0).unique().values
#            cats=np.append([cats],[subCats])
        #print(userTemplate['Narrow Capability'])    
       # trace1 = figure={'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        #trace2= figure= {'x': capabilities, 'y': df3['Net'], 'type' : 'bar'}
        #print(df3['Net'])
   
        return html.Div([
                        
                        #dcc.Graph(id='test-graph'),
                        html.Div(dcc.Graph(
                                id='testgraph-3',
                                #figure={ 'data' : [trace1,trace2],
                                       figure={'data': [{'x': subcats,'y': df.loc[value].loc[ndata]['Score'],'type' : 'bar',
                                                 'hoverinfo':'labels + df2["Score"]',},],
                                        'layout': {
                                                'title': 'TPL Narow Capability',
                                                'showlegend': False},
                                        }
        
                                    )
                               # id='left-div-new'
                                )
                        
                                ],
                               # id='q1-holdernew',
                        className='eleven columns'
                        ),             
                        

#end plot callback

@app.callback(Output('bot-left-div-2','children'),
                [Input('specificC-dropdown','value')],
                [State('narrowC-dropdown','value'),
                State('capabilities-dropdown','value')])
def set_specific_definition(sdata,ndata,value):

	if sdata:
		tpl = temp_load_assessment()
		description = tpl[(tpl[idxCols[0]]==value)&(tpl[idxCols[1]]==ndata)&(tpl[idxCols[2]]==sdata)]

		return [html.H6(f'{sdata} Definition:'),
				html.Div(description['nCapability description'].unique())]


@app.callback(Output('bot-left-div-3','children'),
                [Input('qGroup-dropdown','value')],
                [State('specificC-dropdown','value'),
                State('narrowC-dropdown','value'),
                State('capabilities-dropdown','value'),
				State('session-id','children')])
def set_question_dropdown(qdata,sdata,ndata,value,sid):

	if qdata:
		tpl = temp_load_assessment()
		length = tpl[(tpl[idxCols[0]]==value)&(tpl[idxCols[1]]==ndata)&(tpl[idxCols[2]]==sdata)]
		length = length[length['Question Group Description']==qdata]
		length = length.shape[0]

		return [dcc.Dropdown(id='numQuestions-dropdown',
						options=[{'label':f'Question {i+1}',
										'value':i} for i in range(length)],
						value=None,
						placeholder="Select Question"
						,className='six columns')]


@app.callback(Output('bot-right-div-1','children'),
                [Input('numQuestions-dropdown','value')],
				[State('qGroup-dropdown','value'),
				State('specificC-dropdown','value'),
                State('narrowC-dropdown','value'),
                State('capabilities-dropdown','value'),
				State('session-id','children')])
def disp_question(qn,qdata,sdata,ndata,value,sid):

	style={'textAlign': 'center',
			'color': colors['text']
		}
	print(qn)
	if qn is not None:
		df = init_user_dataframe(sid)
		df = df[(df[idxCols[0]]==value)&(df[idxCols[1]]==ndata)&(df[idxCols[2]]==sdata)].iloc[qn]
		df['Score'] = 10
		df = init_user_dataframe(sid)
		df = df[(df[idxCols[0]]==value)&(df[idxCols[1]]==ndata)&(df[idxCols[2]]==sdata)].iloc[qn]
		print(df['Score'])

		tpl = temp_load_assessment()
		qGroup = tpl[(tpl[idxCols[0]]==value)&(tpl[idxCols[1]]==ndata)&(tpl[idxCols[2]]==sdata)]
		qGroup = qGroup.iloc[qn]
		question = qGroup['Question']
		background = qGroup['Background']
		h,m,l = qGroup['High'],qGroup['Medium'],qGroup['Low']
	
		return	[html.H6(f'Question {qn+1}'),
				html.Div(id='net-score-div'),
				html.Div([
					html.Div([f'Contribution to {sdata} Score:'],
							className='eight columns'),
					dcc.Input(placeholder='Enter your Score',
								id='contribution-weight',
								type='number',
								value=df['SpecCap Weight'],
								min=0,max=10,
								debounce = True,
								className='four columns')
				],
				className='twelve columns'),
				html.Div(question),
				html.Div([
					html.Div([
						dcc.ConfirmDialogProvider(
						children=html.Button('Background',
									className='twelve columns'),
						id='background-button',
						message=background),
						dcc.ConfirmDialogProvider(
						children=html.Button('Score Guidance',
									className='twelve columns'),
						id='score-button',
						message=f'High: {h} \n\nMedium: {m} \n\nLow: {l}')
					],className='twelve columns'),
					html.Div([
						html.Div([html.Div(children='Score', 
									style=style),
								html.Div(children='(0-10)', 
									style=style),
									dcc.Input(placeholder='Enter your Score',
											id='question-score',
											type='number',
											value=df['Score'],
											min=0,max=10,
											debounce = True,
											className='twelve columns'
									)],className='six columns'),
						html.Div([html.Div(children='Value Weighting', 
									style=style),
									html.Div(children='(0-1)', 
									style=style),
									dcc.Input(placeholder='Enter your Weighting',
											id='question-weight',
											type='number',
											value=df['Weight'],
											min=0,max=1,
											debounce = True,
											className='twelve columns'
									)
									],className='six columns'),
								html.Button('Submit Score',
										id = 'score-sub-button',
										className='twelve columns')
					],className='twelve columns')
				],className='twelve columns')
				
				]


@app.callback(Output('dummy-out-1','children'),               
                [Input('score-sub-button','n_clicks')],
				[State('question-score','value'),
				State('question-weight','value'),
				State('numQuestions-dropdown','value'),
				State('qGroup-dropdown','value'),
				State('specificC-dropdown','value'),
                State('narrowC-dropdown','value'),
                State('capabilities-dropdown','value'),
				State('session-id','children')])
def sub_new_scores(click,score,weight,qn,qdata,sdata,ndata,value,sid):
	if click:
		ud = 1
		
		ut = init_user_dataframe()

		try:
			ut.loc[value,ndata,sdata].iloc[qn]['Score'] = score
			ut.loc[value,ndata,sdata].iloc[qn]['Weight'] = weight
			ut.loc[value,ndata,sdata].iloc[qn]['Input Score'] = score*weight

		except (AttributeError,ValueError) as e:
			ut.loc[value,ndata,sdata]['Score'] = score
			ut.loc[value,ndata,sdata]['Weight'] = weight
			ut.loc[value,ndata,sdata]['Input Score'] = score*weight

		save_user_template(ut)

        

@app.callback([Output('net-score-div','children'),
               Output('test-graph','children')],               
                [Input('score-sub-button','n_clicks')],
				[State('question-score','value'),
				State('question-weight','value'),
				State('numQuestions-dropdown','value'),
				State('qGroup-store','data'),
				State('specificC-store','data'),
                State('narrowC-store','data'),
                State('subCats-store','data')])
def set_input_score(click,score,weight,qn,qdata,sdata,ndata,value):
    if click:
        net = score*weight
        figure=set_tpl_assessment_plot_subcat(value)
        return html.H6(f'Question Score:  {net}'),figure
    else:
        ut = load_user_template()

        try:
            net = ut.loc[value,ndata,sdata].iloc[qn]['Input Score']
       

        except (AttributeError,ValueError) as e:
            net = ut.loc[value,ndata,sdata]['Input Score']
        figure=set_tpl_assessment_plot_subcat(value)
			
        return html.H6(f'Question Score:  {net}'),figure

@app.callback(Output('dummy-out-2','children'),
                [Input('contribution-weight','value')],
				[State('numQuestions-dropdown','value'),
				State('qGroup-store','data'),
				State('specificC-store','data'),
                State('narrowC-store','data'),
                State('subCats-store','data')])
def sub_new_scores(spWeight,qn,qdata,sdata,ndata,value):
    if value:
        ut = load_user_template()

        try:
            ut.loc[value,ndata,sdata].iloc[qn]['SpecCap Weight'] = spWeight

        except (AttributeError,ValueError) as e:
            ut.loc[value,ndata,sdata]['SpecCap Weight'] = spWeight
        
        save_user_template(ut)
        


        


if __name__ == '__main__':
    ## Run in Browser
    #app.run()
    ## run standalone

    init_gui(app,window_title='TPL Assessment Stand Alone Tool',
				width=800,height=800,icon='./images/logo.png')

