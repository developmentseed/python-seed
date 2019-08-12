import py2neo
import os
import yaml
from py2neo import  Graph, Node, Relationship

path = os.path.dirname(os.path.realpath(__file__))
yaml_path =  os.path.join(path, "strategies.yaml")
with open(yaml_path, 'r') as stream:
    yam = yaml.safe_load(stream)


url = "bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687"
graph = Graph(url)
tx = graph.begin()
graph.delete_all()
instrument_nodes = {}
capture_nodes = {}

def new_node(label,**properties):
    newNode = Node(label,**properties)
    graph.create(newNode)
    return newNode
    graph.create(Relationship(from_node,name,to_node))


for market in yam['markets']:
    newMarket = new_node("Market", **market['props'])
    for instr in market['instrs']:
        new_instr = new_node ('Instrument',**instr)
        instrument_nodes[instr['name']]= new_instr
        graph.create(Relationship(new_instr ,"TRADES_ON",newMarket))


for (feedkey,feedVal) in yam['feedpoints'].items():
    newFeed = Node("PriceFeed", name=feedkey)
    graph.create(newFeed)
    for (fieldKey,fieldVal) in feedVal.items():
        newField = new_node("FeedField",name=fieldKey)
        feed_to_field = Relationship(newFeed,"HAS_FIELD",newField)
        graph.create(feed_to_field)
        for ticker in fieldVal['tickers']:
            newTicker = new_node("FeedTicker",name=ticker)
            field_to_ticker = Relationship(newField,"HAS_TICKER",newTicker)
            graph.create(field_to_ticker)
            for capture in fieldVal['times']:
                feed_path = '/'.join([feedkey,fieldKey,ticker,capture])
                capture_nodes[feed_path]=new_node("Capture", name=capture,path=feed_path)
                graph.create(Relationship(newTicker,"CAPTURES",capture_nodes[feed_path]))


for strat in yam['strategies']:
    newStrat = new_node("Strategy",**strat['props'])
    for quote in strat['quotes']:
        quote_to_strat = Relationship(new_node('Quote',**quote['props']),"PUBLISHED_BY",newStrat)
        graph.create(quote_to_strat)
    for constituent in strat['constituents']:
        graph.create(Relationship(instrument_nodes[constituent['name']],"CONSTITUENT_OF", newStrat,**constituent['props']))

    for eval in strat['evals']:
        new_job = new_node("Job",**eval['props'])
        graph.create(Relationship(newStrat,"EVAL_JOB",new_job))
        for (capture_key,capture_path) in eval['dependencies'].items():
            amended_path = capture_path[0:2]
            amended_path.append(capture_path[3])
            amended_path.append(capture_path[2])
            path = '/'.join(amended_path)
            capture_node = capture_nodes[path]
            graph.create(Relationship(new_job,"USES",capture_node))
            graph.create(Relationship(capture_node,"OBSERVATION_OF",instrument_nodes[capture_key]))



tx.commit()