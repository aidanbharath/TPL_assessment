from pandas import read_excel

def base_load_template(File = 'static/base_TPL_assessment.xlsx'):
    indexCols = ['Broad Capability','Narrow Capability','Specific Capability']
    tplAssessment = read_excel(File)
    tplAssessment.set_index(indexCols,inplace=True)    
    return tplAssessment