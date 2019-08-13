
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
            queryStr = """"
            match (s:Strategy)-->(p:Job)-->(c:Capture)<--(ticker:FeedTicker)<--(field:FeedField)<--(feed:PriceFeed) return 
            
            p,s,c,ticker,field,feed
            
            """

            records = session.write_transaction(lambda tx:tx.run(queryStr))
            for record in records:
                print(record)

    def reducedJobs(self):
        with self._driver.session() as session:
            queryStr = "match  p= (s:Strategy)-->(j:Job)-->(c:Capture)<--(ticker:FeedTicker)<--(field:FeedField)<--(feed:PriceFeed)  return reduce (stratMap = 0, n IN nodes(p) | stratMap + 1  )  AS reduction"

            records = session.write_transaction(lambda tx: tx.run(queryStr))
            for record in records:
                print(record)


jf = JobFetcher("bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687",user="",password="")
jf.reducedJobs()
jf.close()
