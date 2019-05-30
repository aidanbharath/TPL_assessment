from pandas import DataFrame,read_excel,read_csv
from numpy import float64, nan

def base_load_template(File = 'static/base_TPL_assessment.xlsx'):
    indexCols = ['Broad Capability','Narrow Capability','Specific Capability']
    tplAssessment = read_excel(File)
    tplAssessment.set_index(indexCols,inplace=True)    
    return tplAssessment

def create_user_template(baseTemplate):
    userDF = DataFrame(index = baseTemplate.index,
                            columns = ['Score','Weight','SpecCap Weight','Threshold'],
                            dtype=float64)
    userDF['Score'] = float64(baseTemplate['Score'])
    userDF['Weight'] = float64(baseTemplate['Weight'])
    userDF['SpecCap Weight'] = float64(baseTemplate['SpecCap Weight'])
    userDF['RW'] = nan
    userDF['Input Score'] = userDF['Score']*userDF['Weight']
    userDF['Contribution'] = userDF['Input Score']*userDF['RW']
    userDF['Net'] = nan
    userDF['Threshold'] = float64(baseTemplate['Threshold'])
    userDF.to_csv('./static/userDF.csv')

def load_user_template():
    indexCols = ['Broad Capability','Narrow Capability','Specific Capability']
    userAssessment = read_csv('./static/userDF.csv')
    userAssessment.set_index(indexCols,inplace=True)    
    return userAssessment

def save_user_template(userTemplate):
    userTemplate.to_csv('./static/userDF.csv')


