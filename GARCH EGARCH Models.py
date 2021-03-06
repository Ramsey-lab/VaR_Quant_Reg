#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from arch import arch_model
import statistics as stat
from scipy.stats import norm
from scipy.stats import t


#1 Modèle GARCH(1,1) avec résidus suivant une loi normale
#r étant le vecteur des rendement du ptf équipondéré
 
def Garch_Normal(r,alpha):
    
    model=arch_model(r,mean="AR",lags=1,vol='GARCH',p=1,o=0,q=1,dist='Normal')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    pred=fit_model.forecast(horizon=1);
    var_1day=pred.variance.values[-1, :]
    VaR= -(norm.ppf(1-alpha)*np.sqrt(var_1day))
    
    return VaR
     
def Garch_Student(r,alpha):

    #calcul de la moyenne
    rescale=False
    model=arch_model(r,mean="AR",lags=1,vol='GARCH',p=1,o=0,q=1,dist='studentst')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    pred=fit_model.forecast(horizon=1)
    var_1day=pred.variance.values[-1, :]
    VaR= -(t.ppf(1-alpha,df=10)*np.sqrt(var_1day))
    return VaR


def GARCH_FHS(r,alpha):

   
    model=arch_model(r,mean="AR",lags=1,vol='GARCH',p=1,o=0,q=1,dist='Normal')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    #pred=fit_model.forecast(start='1996-1-1',horizon=1)
    pred=fit_model.forecast(horizon=1)
    cond_mean = pred.mean.values[-1:]
    cond_var = pred.variance.values[-1:]
    #calcul des résidus standardisés
    std_rets = r / fit_model.conditional_volatility
    std_rets = std_rets.dropna()
    q = std_rets.quantile(alpha)
    VAR = - np.sqrt(cond_var) * q
    return VAR 


def EGarch_Normal(r,alpha):
   

    model=arch_model(r,mean="AR",lags=1,vol='EGARCH',p=1,o=0,q=1,dist='Normal')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    pred=fit_model.forecast(horizon=1);
    var_1day=pred.variance.values[-1, :]
    VaR= -(norm.ppf(1-alpha)*np.sqrt(var_1day))
    return VaR
    
    
     
def EGarch_Student(r,alpha):
    
    rescale=False
    model=arch_model(r,mean="AR",lags=1,vol='EGARCH',p=1,o=0,q=1,dist='studentst')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    pred=fit_model.forecast(horizon=1);
    var_1day=pred.variance.values[-1, :]
    VaR= -(t.ppf(1-alpha,df=10)*np.sqrt(var_1day))
    return VaR

def EGarch_FHS(r,alpha):
    
    model=arch_model(r,mean="AR",lags=1,vol='EGARCH',p=1,o=0,q=1,dist='Normal')
    fit_model=model.fit()
    #Faire la prédiction à 1 jour de la variance
    #pred=fit_model.forecast(start='1996-1-1',horizon=1)
    pred=fit_model.forecast(horizon=1)
    cond_mean = pred.mean.values[-1:]
    cond_var = pred.variance.values[-1:]
    #calcul des résidus standardisés
    std_rets = r / fit_model.conditional_volatility
    std_rets = std_rets.dropna()
    q = std_rets.quantile(1-alpha)
    VAR = - np.sqrt(cond_var) * q
    return VAR 

