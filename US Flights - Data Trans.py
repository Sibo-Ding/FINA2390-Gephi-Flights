# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:02:12 2022

@author: Sibo Ding
"""

'''
This code transforms data of US airports and flight routes.
Next step, use Gephi to generate network visualizaion.
More detailed infomation:
https://ipython-books.github.io/142-drawing-flight-routes-with-networkx/
'''

import pandas as pd

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

# Create output nodes dataframe based on "Game of Thrones_Nodes" file
nodes = pd.DataFrame()
nodes['Id'] = airports_filter['iata']
nodes['Label'] = airports_filter['iata']
nodes['latitude'] = airports_filter['lat']
nodes['longitude'] = airports_filter['lon']
nodes[['timeset', 'modularity_class', 'pageranks', 'eigencentrality', 
       'clustering', 'triangles', 'weighted degree', 'Eccentricity',
       'closnesscentrality', 'harmonicclosnesscentrality',
       'betweenesscentrality']] = ''

# Create output edges dataframe based on "Game of Thrones_Edges" file
edges = pd.DataFrame()
edges['Source'] = routes_us['source']
edges['Target'] = routes_us['dest']
edges['Type'] = ['Directed' for i in range(len(routes_us))]
edges['Id'] = routes_us.index
edges[['Label', 'timeset', 'Weight']] = ''

nodes.to_csv('US Flights_Nodes.csv', index=False)
edges.to_csv('US Flights_Edges.csv', index=False)
