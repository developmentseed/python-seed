
from py2neo import  Graph, Node, Relationship,RelationshipMatcher


url = "bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687"
graph = Graph(url)

strategies = graph.nodes.match('Strategy')
for strategy in strategies:
    print ("STRATEGY = {}".format(strategy['name']))
    jobs = graph.match((strategy,),r_type='EVAL_JOB')

    for j in jobs:

        job_node = j.end_node
        print("   JOB = {}".format(job_node['name']))
        dependencies = graph.match((job_node,),r_type="USES")
        for dependency in dependencies:
            print ("            " + dependency.end_node['path'])



