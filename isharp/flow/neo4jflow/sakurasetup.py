import py2neo
import os
import yaml
import calendar
from py2neo import  Graph, Node, Relationship,NodeMatcher
import neotime
from datetime import date,timedelta

graph = Graph("bolt://{}:7687".format('localhost'), user="neo4j", password="guest", auth=('neo4j', 'guest'))



tx = graph.begin()

graph.delete_all()

def new_node(label,**properties):
    newNode = Node(label,**properties)
    graph.create(newNode)
    return newNode


# time_tree = new_node("TIME_TREE")
nodes = NodeMatcher(graph)
matcher = nodes.match("TIME_TREE")
if matcher.exists():
    graph.delete(matcher.first())

for thisM in nodes.match('Year').all():
    graph.delete(thisM)

for thisM in nodes.match('Year').all():
    graph.delete(thisM)


time_tree = new_node("TIME_TREE",name='Time tree')

year_nodes = []
month_nodes = []
weekday_nodes = []



for month_idx in range(1, 13):
    month_nodes.append(new_node("MONTH", name=calendar.month_name[month_idx]))
    graph.create(Relationship(time_tree,"CHILD", month_nodes[month_idx-1]))
    if (month_idx > 0):
        graph.create(Relationship(month_nodes[month_idx-1],"NEXT",month_nodes[month_idx-1]))



for idx,weekday in enumerate(list(calendar.day_name)):
    weekday_nodes.append(new_node("WEEKDAY", name=weekday))
    graph.create(Relationship(time_tree,"CHILD",weekday_nodes[idx]))
    if (idx > 0):
        graph.create(Relationship(weekday_nodes[idx-1],"NEXT", weekday_nodes[idx]))


for idx,year in enumerate(list(range(2020,2021,1))):
    year_node = new_node("Year", name=year)
    year_nodes.append(year_node)
    graph.create(Relationship(time_tree, "CHILD", year_node))
    if idx>1:
            graph.create(Relationship(year_nodes[idx-1], "NEXT", year_node))


    first_date_in_year = date(year,1,1)
    last_date_in_year = date(year,12,31)
    delta = last_date_in_year - first_date_in_year
    day_nodes = []
    for i in range(delta.days +1):
        day = first_date_in_year + timedelta(days=i)
        month_name = calendar.month_name[day.month]
        day_name = "{}-{}-{}".format(day.year,month_name,day.day)
        day_nodes.append(new_node("DAY", name=day_name, year = day.year, month = day.month, dayofmonth=day.day))
        graph.create(Relationship(day_nodes[i],"IN_MONTH_OF",month_nodes[day.month-1]))
        graph.create(Relationship(day_nodes[i], "ON_WEEKDAY", weekday_nodes[day.weekday()]))
        if (i>0):
            graph.create(Relationship(day_nodes[i-1],"NEXT",day_nodes[i]))









graph.create(Relationship(time_tree,"FIRST", year_nodes[0]))
graph.create(Relationship(time_tree, "LAST", year_nodes[-1]))
graph.create(Relationship(time_tree,"FIRST", month_nodes[0]))
graph.create(Relationship(time_tree,"LAST", month_nodes[-1]))
graph.create(Relationship(time_tree,"FIRST", weekday_nodes[0]))
graph.create(Relationship(time_tree,"LAST", weekday_nodes[-1]))












tx.commit()