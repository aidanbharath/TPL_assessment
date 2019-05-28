from numpy import sqrt, sum, product

def investOp(x, name):

    capOp, others = [], []
    for idx in x.loc[name].index:
        if 'CAPEX' in idx or 'OPEX' in idx:
            capOp.append(x.loc[name,'Input Score'][idx])
        else: 
            others.append(x.loc[name,'Input Score'][idx])
    result = [sum(capOp)]+others
    return product(result)**(1/len(result))

def pnc(x,name):
    return x.loc[name[0],'Input Score'].product()**(1/x.loc[name[0],'Input Score'].shape[0])

def baseEQ(x,name):
    return x.loc[name,'Input Score'].product()**(1/x.loc[name,'Input Score'].shape[0])
gst = {
    'Cost of Energy':{
        'Performance': baseEQ
    },
    'Investment Opportunity':{
        'Investment Opportunity': investOp
    },
    'Permitting and Certification':{
        'Area Use Conflicts': pnc,
        'Ecological Impacts': pnc,
        'Environmental Impacts': pnc
    },
    'Safety and Function':{
        'Be Survivable': baseEQ
    },
    'Be Deployable Globally':{
        'Be Deployable Globally': baseEQ
    }

}

def coe_third_level(x,name,capexScale=0.7,opexScale=0.3):
    
    cap, op, others = [], [], []
    X = x.loc[name]
    for idx,_ in X.index:
        if 'CAPEX' in idx:
            cap = X.loc[idx,'Net'].mean()
        elif 'OPEX' in idx:
            op = X.loc[idx,'Net'].mean()
        else: 
            others.append(X.loc[idx,'Net'].mean())
    weirds = [1/((capexScale/cap)+(opexScale/op))]
    result = weirds+others
    return product(result)**(1/len(result))

def safe(x,name):
    values = []
    X = x.loc[name]
    for idx in X.index.get_level_values(0).unique():
        values.append(X.loc[idx,'Net'].mean())

    return product(values)**(1/len(values))

def io(x,name):
    return x.loc[name,'Net'].mean()


hst = {
    'Cost of Energy': coe_third_level,
    'Permitting and Certification': baseEQ,
    'Safety and Function': safe,
    'Investment Opportunity': io
}