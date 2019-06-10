from pandas import DataFrame,read_excel,read_csv
from numpy import float64, nan

def base_load_template(File = 'static/base_TPL_assessment.xlsx'):
    indexCols = ['Broad Capability','Narrow Capability','Specific Capability','Question Group Description']
    tplAssessment = read_excel(File)
    tplAssessment.set_index(indexCols,inplace=True) 
    #print(tplAssessment.loc)
    return tplAssessment

def standard_load_assessment(File = 'static/base_TPL_assessment.xlsx'):
    return read_excel(File)


def cache_create_template(File = 'static/base_TPL_assessment.xlsx'):
    base = read_excel(File)
    userDF = base.loc[:,('Broad Capability','Narrow Capability','Specific Capability','Question Group Description')]
    userDF['Score'] = float64(base['Score'])
    userDF['Weight'] = float64(base['Weight'])
    userDF['SpecCap Weight'] = float64(base['SpecCap Weight'])
    userDF['RW'] = nan
    userDF['Input Score'] = userDF['Score']*userDF['Weight']
    userDF['Contribution'] = userDF['Input Score']*userDF['RW']
    userDF['Net'] = nan
    userDF['Threshold'] = float64(base['Threshold'])
    return userDF

def create_user_template(base,sid):
    userDF = base.loc[:,('Broad Capability','Narrow Capability','Specific Capability','Question Group Description')]
    userDF['Score'] = float64(base['Score'])
    userDF['Weight'] = float64(base['Weight'])
    userDF['SpecCap Weight'] = float64(base['SpecCap Weight'])
    userDF['RW'] = nan
    userDF['Input Score'] = userDF['Score']*userDF['Weight']
    userDF['Contribution'] = userDF['Input Score']*userDF['RW']
    userDF['Net'] = nan
    userDF['Threshold'] = float64(base['Threshold'])
    userDF.to_csv(f'./static/userDF-{sid}.csv')

def load_user_template(sid):
    #indexCols = ['Broad Capability','Narrow Capability','Specific Capability']
    userAssessment = read_csv(f'./static/userDF-{sid}.csv')
    #userAssessment.set_index(indexCols,inplace=True)    
    return userAssessment

def save_user_template(userTemplate,sid):
    userTemplate.to_csv(f'./static/userDF-{sid}.csv')


