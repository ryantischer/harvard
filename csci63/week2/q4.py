#!/usr/bin/python
__author__ = 'Ryan Tischer'

#FILENAME.py: Description of program or code.
#Use at your own risk
#Contact @ryantischer



from py2neo import Graph, Node, Relationship, NodeSelector
import csv

#auth disabled
graph = Graph("http://localhost:7474/db/data/")

#gd = graph.data("Match (n) return n")

y = graph.run("match (n:Movie) return n.title, n.year ").data()

counter = 0

with open('Movies.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'title', 'year'])

    for i in range(len(y)):
        spamwriter.writerow([counter + 10, y[counter]["n.title"], y[counter]["n.year"]])
        counter = counter +1

     #   counter = counter +1


b = graph.run("match (n:Actor) return n.name").data()

counter = 0

with open('actors.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'name'])

    for i in range(len(b)):
        spamwriter.writerow([counter +10, b[counter]["n.name"]])
        counter = counter +1

c = graph.run("match (n:Director) return n.name").data()

counter = 0

with open('directors.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'name'])

    for i in range(len(c)):
        spamwriter.writerow([counter +10, c[counter]["n.name"]])
        counter = counter +1

#end section

d = graph.run("MATCH (n:Actor)-[r]->(y:Movie ) return n.name, y.title, r.role").data()


counter = 0


with open('ACTS_IN.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'name', 'ACTS_IN' ,'title', 'role'])

    for i in range(len(d)):
        spamwriter.writerow([counter + 10, d[counter]["n.name"],"ACTS_IN",d[counter]["y.title"],d[counter]["r.role"]])
        counter = counter +1

#end section

e = graph.run("MATCH (n:Director)-[r]->(y:Movie ) return n.name, y.title").data()

counter = 0

#

with open('Directs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['id', 'name', 'Directed', 'title'])

    for i in range(len(e)):
        spamwriter.writerow([counter + 10, e[counter]["n.name"], "Directed", e[counter]["y.title"]])

        counter = counter +1

raw_input("wait")
#end csv collection

graph.delete_all()

command   = '''
LOAD CSV WITH HEADERS FROM "file:/Users/ryantischer/Dropbox/harvard/CSCI63/pycharm/actors.csv" AS line MERGE (a:Actor { id:line.id } )
ON CREATE SET a.name=line.name'''

graph.run(command)

command   = '''
LOAD CSV WITH HEADERS FROM "file:/Users/ryantischer/Dropbox/harvard/CSCI63/pycharm/Movies.csv" AS line MERGE (a:Movie { id:line.id } )
CREATE (m:Movie { id:line.id,title:line.title, released:toInteger(line.year)});'''

graph.run(command)

command   = '''
LOAD CSV WITH HEADERS FROM "file:/Users/ryantischer/Dropbox/harvard/CSCI63/pycharm/directors.csv" AS line MERGE (a:Director { id:line.id } )
ON CREATE SET a.name=line.name'''

graph.run(command)

command = '''LOAD CSV WITH HEADERS FROM "file:/Users/ryantischer/Dropbox/harvard/CSCI63/pycharm/ACTS_IN.csv" AS line
MERGE (m:Movie { title:line.title })
MERGE (a:Actor { name:line.name })
MERGE (a)-[:ACTED_IN { roles:line.role}]->(m);'''

graph.run(command)

command = '''LOAD CSV WITH HEADERS FROM "file:/Users/ryantischer/Dropbox/harvard/CSCI63/pycharm/Directs.csv" AS line
MERGE (m:Movie { title:line.title })
MERGE (a:Director { name:line.name })
MERGE (a)-[:Directs ]->(m);'''

graph.run(command)