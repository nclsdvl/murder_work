# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:09:33 2020

@author: MonOrdiPro
"""
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.graph_objs import *
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import tools
from tools import get_row_col
data1 = pd.read_csv('SHR76_17.csv')



##################################################################################
###########  Graph Homicide number and solved percentage by year  ################
##################################################################################
grouped_year = data1.groupby('Year')

years=[]
nb_homicide=[]
rates_solved=[]
grouped_year.size()




for year, groupe in grouped_year:
    sub_group = grouped_year.get_group(year)
    
    nb_resolved = len(sub_group[sub_group['Solved'] == 'Yes'])
    nb_unresolved = len(sub_group[sub_group['Solved'] == 'No'])
    years.append(year)
    nb_homicide.append(len(groupe))
    rate_solved = 100 * nb_resolved / (nb_resolved + nb_unresolved)
    rates_solved.append(rate_solved)
     

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(
    x=years,
    y=nb_homicide,
    name='Homicide Number by year',
    marker_color='violet',
    
),secondary_y=False)

trace1 = {'type' : 'scatter',
          'x' : years,
          'y' : rates_solved,
          'name' : 'Solved percent',
          'marker_color':'darkred'
          }
fig.add_trace(trace1, secondary_y=True)

fig.update_yaxes(secondary_y=False, title_text="<b>Number of homicide</b>")
fig.update_yaxes(range=[50, 100], secondary_y=True, title_text="<b>percent of solved case</b>")
fig.update_layout(xaxis = {'title':'year'}, title = '<b>Homicide number and solved percentage by year</b>')

plot(fig, auto_open=True)





##################################################################################
#####Graphs Homicide by 32 circumstances and by year with % solved case  #########
##################################################################################

years = []
traces = []
circ = data1.Circumstance.unique()


# preparation d'un objet afin de recuperer les années en clés et le pd.Series 'circonstance' : 'nbr homicide'
# pas tres opti...
obj = {}
obj_resolved = {}


# preparation direct d'un df avec en colonne les circonstances et en ligne les années
# plus opti...
df_resolved = pd.DataFrame( columns = circ)
df_resolved['year'] = 9999



grouped_year = data1.groupby('Year')

# recuperation des données
for year, groupe in grouped_year:
    sub_group = grouped_year.get_group(year)
    val_count = sub_group.Circumstance.value_counts()
    val_count.reset_index()
    obj[year] = val_count
    
    # on prepare une ligne de pourcentage (par année) que l'on pourra inserer dans df_resolved
    row_resolved = pd.Series(index = circ)
    
    for circonstance in circ :
        sub_group_circ = sub_group[sub_group['Circumstance'] == circonstance]
        nb_resolved = len(sub_group_circ[sub_group_circ['Solved'] == 'Yes'])
        nb_unresolved = len(sub_group_circ[sub_group_circ['Solved'] == 'No'])
        try :
            rate_solved = int(100 * nb_resolved / (nb_resolved + nb_unresolved))
        # si (nb_resolved + nb_unresolved) en place le % a 100 -> pas de cas sur l'année
        except :
            rate_solved = 100
        row_resolved[circonstance] = rate_solved
    print(year)
    # on ajoute l'année a notre ligne et on l'insere dans df_resolved       
    row_resolved['year'] = year
    df_resolved.loc[len(df_resolved)] = row_resolved
    

# preparation du df contenant le nombre d'homicide en colonne circonstance et en ligne les années
df = pd.DataFrame( columns = circ)
df['year'] = 9999

# remplissage de df grace à l'obj
for key, val in obj.items():
    row=pd.Series(index = circ)
    for circonstance, nbr in val.items() :
        row[circonstance]=nbr
    row['year'] = key
    df.loc[len(df)] = row
    
# nettoyage de df (les na represente les circonstances sans cas pour l'années)
df = df.astype({'year' : 'int32'})
df = df.fillna(0)

# recuperation des subplot_titles
subplot_titles = df.columns.drop('year')


# choix subjectif d'un graph en 7 lignes 5 colonnes (avec un second axe y )
plots = make_subplots(rows=7, cols=5, subplot_titles= subplot_titles, specs=[[{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}],
                                                                              [{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True},{"secondary_y": True}]])

# remplissage du graph
for i in range (0,len(subplot_titles)) : 
    # recuperation des coordonnées du subplot
    row, col = get_row_col(i)
    
    # preparation de la liste nombre de cas
    y= df[df.columns[i:i+1]]
    y = np.transpose(y)
    y=y.values.tolist()[0]
    
    # preparation de la liste du pourcentage solved
    y_resolved= df_resolved[df_resolved.columns[i:i+1]]
    y_resolved = np.transpose(y_resolved)
    y_resolved=y_resolved.values.tolist()[0]   
    
    
    plots.append_trace({'type' : 'scatter',
                   'x' : df['year'],
                   'y' : y,
                   'name' : df.columns[i:i+1][0],
                   'mode' : 'lines', },row = row, col = col)
    plots.append_trace({'type' : 'scatter',
                   'x' : df_resolved['year'],
                   'y' : y_resolved,
                   'name' : df_resolved.columns[i:i+1][0],
                   'line': {'dash':'dot', 'color':'coral'}}, row = row, col = col)   
  

    
# customization de l'affichage du graph   
plots.update_layout(showlegend=False, 
                    title_text="<b style='font-size: 30px'>Murder number by year and Circumstances </b><b>(dotted line = % solved case, double click -> auto-range)</b>",
                    height=1000,
                    width=2000)

# les seconds axes y sont identique aux premiers pour chaque subplot
# il faut donc : 
#    1 - lui assigner un nouveau nom (arbitrairement de y101 à y163 par pas de deux)
#    2 - aligner son anchor et son overlaying pour faire correspondre les secondes traces aux premiere


# liste_y va nous permettre d'iterer sur les secondes traces
liste_y = np.arange(1, len(plots['data']), 2)

# j va nous permettre d'aligner l'overlaying du yaxis secondaire (fonctionne par pas de 2)
# k son anchor (fonctionne par pas de 1)
j = 3
k = 2

#first time nous sert à la premiere iteration (j et k ne doivent pas etre utilisés)
first_time = True


for x in liste_y :
    print('--------------'+str(x)+'----------')
    print(j)
    print(k)
    print('update sur : yaxis=y'+str(100+x))
    
    # modification du nom du second yaxis
    plots['data'][x].update(yaxis=('y'+str(100+x)))
    
    if first_time :
        print('if first time')
        plots['layout']['yaxis'+str(100+x)]=dict(range= [0, 100], 
                              overlaying= 'y', 
                              anchor= 'x', 
                              side= 'right',
                              color = 'coral',
                              showgrid= False, 

                             )
        first_time = False
    # alignement des anchor et overlaying    
    else :
        print('else')
        print('plots dot layout at yaxis'+str(100+x)+' overlaying = y'+str(j)+' anchor = x'+str(k))
        
        plots['layout']['yaxis'+str(100+x)]=dict(range= [0, 100], 
                              overlaying= 'y'+str(j), 
                              anchor= 'x'+str(k), 
                              side= 'right',
                              color = 'coral',
                              showgrid= False, 

                             )      
        
        
        j+=2
        k+=1

plot(plots, auto_open=True)

####################################################################################
####################################################################################

