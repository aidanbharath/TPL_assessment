import load

from groupScoreTemplates import gst, hst
from pandas import Series

idxCols = ['Broad Capability','Narrow Capability','Specific Capability','Question Group Description']


def calc_input_scores(sid):
    '''
    This functions replicates the values found in the 'input score' section of 
    the spreadsheet.

    return frame still has the indexing available
    '''

    userDF = load.load_user_template(sid)
    userDF = userDF.groupby(idxCols).mean()
    return userDF

def calc_relative_weight(df):
    for name,group in df.groupby(level=[0,1]):
        df.loc[name,'RW'] = group['SpecCap Weight']/group['Input Score'].shape[0]
    return df

def calc_second_level_group_score(sid):
    '''
    I'm finding it a little tricky to find a rhyme or reason to how these are 
    calculated. 
    
    This is going to cause issues for easy upgradability!!!!!

    Current default behaviour will calculate the second level group score as
    just the sum of the net scores
    '''

    meansDF = calc_relative_weight(calc_input_scores(sid))

    groups = meansDF.groupby(level=[0,1])
    for name,group in groups:
        if name[0] in gst.keys() and name[1] in gst[name[0]].keys():
            meansDF.loc[name,'RW'] = group['SpecCap Weight']/group['Input Score'].shape[0]
            meansDF.loc[name,'Contribution'] = group['Input Score']*meansDF.loc[name,'RW']
            meansDF.loc[name,'Net'] = gst[name[0]][name[1]](meansDF,name)
        else:
            meansDF.loc[name,'RW'] = group['SpecCap Weight']/group['Input Score'].shape[0]
            meansDF.loc[name,'Contribution'] = group['Input Score']*meansDF.loc[name,'RW']
            meansDF.loc[name,'Net'] = meansDF.loc[name,'Contribution'].sum()
    
    return meansDF

def calc_third_level_group_score(sid):

    meansDF = calc_second_level_group_score(sid)

    names = meansDF.index.get_level_values(0).unique()
    df = Series()
    for name in names:
        if name in hst.keys():
            df[name] = hst[name](meansDF,name)
        else:
            df[name] = meansDF.loc[name,'Net'].sum()

    return df
            
    
    


