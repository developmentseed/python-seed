
from neo4j import GraphDatabase
import luigi
import os
from isharp.flow.core import DatahubRequirement
from isharp.flow.core import CalculationTask


class JobFetcher(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()


    def fetchJobs(self):
        with self._driver.session() as session:
            records = session.write_transaction(self.showJobs)
            evalJobs = {}
            requirements = {}
            for record in records:
                requirement_rel = record['requirement']
                eval_task_node = record['job']
                strat_node = record['index_group']
                if eval_task_node.id not in evalJobs:
                    evalJobs[eval_task_node.id] = CalculationTask([], eval_label=eval_task_node['name'],
                                                                  dueBy=eval_task_node['due_by'],
                                                                  strategy=strat_node['description'])



    def strategies(self):
        with self._driver.session() as session:
            return session.write_transaction(lambda tx: tx.run("MATCH (p:IndexGroup) RETURN p"))

    @staticmethod
    def showJobs(tx):
        return tx.run("MATCH (index_group)-[evaluation:EVAL]->(job)-[requirement:REQUIRES]->(instrument) RETURN evaluation,index_group,job,requirement,instrument")









jf = JobFetcher("bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687",user="",password="")
jf.fetchJobs()
jf.close()
