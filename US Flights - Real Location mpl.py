# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:21:07 2022

@author: Sibo Ding
"""

'''
This code plots US airports and flight routes in real location using mpl.
Updated version can use NetworkX.
More detailed infomation:
https://ipython-books.github.io/142-drawing-flight-routes-with-networkx/
'''

import pandas as pd
import matplotlib.pyplot as plt

# Running time: about 15s
# Import dataset containing airports
names = ('id,name,city,country,iata,icao,lat,lon,'
         'alt,timezone,dst,tz,type,source').split(',')
airports = pd.read_csv('https://github.com/ipython-books/'
                       'cookbook-2nd-data/blob/master/'
                       'airports.dat?raw=true',
                       header=None,
                       names=names,
                       na_values='\\N')
# Filter the airports in the US
airports_us = airports[airports['country'] == 'United States']

# Import dataset containing flight routes
names = ('airline,airline_id,'
         'source,source_id,'
         'dest,dest_id,'
         'codeshare,stops,equipment').split(',')
routes = pd.read_csv('https://github.com/ipython-books/'
                     'cookbook-2nd-data/blob/master/'
                     'routes.dat?raw=true',
                     names=names,
                     header=None)

# Filter all national US flight routes
# The source and the destination airports belong to US
routes_us = routes[routes['source'].isin(airports_us['iata']) &
                   routes['dest'].isin(airports_us['iata'])]

# Filter all connected US airports
# The airports are connected to either source or destination
airports_filter = airports_us[airports_us['iata'].isin(routes_us['source']) |
                    airports_us['iata'].isin(routes_us['dest'])]

#%% Merge airports' latitudes and longitudes to flight routes
nodes = airports_filter[['iata', 'lat', 'lon']]
edges = routes_us[['source', 'dest']]

edges = pd.merge(edges, nodes, how='left', left_on='source', right_on='iata')
edges = edges[['source', 'lat', 'lon', 'dest']]
edges.columns = ['source', 'source_lat', 'source_lon', 'dest']

edges = pd.merge(edges, nodes, how='left', left_on='dest', right_on='iata')
edges = edges[['source', 'source_lat', 'source_lon', 'dest', 'lat', 'lon']]
edges.columns = ['source', 'source_lat', 'source_lon', 'dest', 'dest_lat', 'dest_lon']

#%% Plot the figure
plt.rcParams['figure.figsize'] = (48, 36)  # Set figure size
for i in range(len(edges)):
    # Plot each line [x1, x2], [y1, y2]
    plt.plot([edges.loc[i,'source_lon'], edges.loc[i,'dest_lon']], 
             [edges.loc[i,'source_lat'], edges.loc[i,'dest_lat']],
             lw=0.03, c='k')  # lw: line width; c: color, 'k': black
plt.show()  # Show the figure
