#!/usr/bin/python
__author__ = 'Ryan Tischer'

#FILENAME.py: Description of program or code.
#Use at your own risk
#Contact @ryantischer

from py2neo import Graph, Node
import json

#Connect to db.  auth disabled
graph = Graph("http://localhost:7474/db/data/")

#create new movie with merge command.  Merge used to eliminate dups
graph.merge( Node ("Movie", title="John Wick", year="2014-7-7") )

#Create new actors
graph.merge(Node ("Actor", name='William Dafoe'))
graph.merge(Node ("Actor", name='Michael Nyquist'))

#Create Directors
graph.merge(Node ("Director", name='Chad Stahelski'))
graph.merge(Node ("Director", name='David Leitch'))


#Build relationship between directors and movies

#Build a cypher command to run.  This command matchs director and movie then creates relationship
graphcmd='''MATCH (u:Director {name:'Chad Stahelski'}), (m:Movie {title:'John Wick'}) CREATE (u)-[:Directs]->(m)'''

#run the command - Repeat until all relationships are built.  Code omitted availible on github


graph.run(graphcmd)

graphcmd='''
MATCH (u:Director {name:'David Leitch'}), (m:Movie {title:'John Wick'})
MERGE (u)-[:Directs]->(m)
'''

graph.run(graphcmd)

#Build relationship between actors and movies

graphcmd='''
MATCH (u:Actor{name:'William Dafoe'}), (m:Movie {title:'John Wick'})
MERGE (u)-[:ACTS_IN]->(m)
'''

graph.run(graphcmd)

graphcmd='''
MATCH (u:Actor{name:'Michael Nyquist'}), (m:Movie {title:'John Wick'})
MERGE (u)-[:ACTS_IN]->(m)
'''

graph.run(graphcmd)


graphcmd='''
MATCH (u:Actor{name:'Keanu Reeves'}), (m:Movie {title:'John Wick'})
MERGE (u)-[:ACTS_IN]->(m)
'''

graph.run(graphcmd)



#Prove it works
y =  graph.run("match (n:Movie) return n.title, n.year ").data()

print json.dumps(y, sort_keys=True,indent=4, separators=(',', ': '))

b = graph.run("match (n:Actor) return n.name").data()

print json.dumps(b, sort_keys=True,indent=4, separators=(',', ': '))


c = graph.run("match (n:Director) return n.name").data()

print json.dumps(c, sort_keys=True,indent=4, separators=(',', ': '))
