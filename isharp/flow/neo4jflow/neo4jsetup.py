from neo4j import GraphDatabase
import luigi
import os

feedpoints = {
    "InvestCo": {
        "CLOSING": {"times": ["EOD"],
                    "tickers": ["NIK", "RUSS", "FTSE", "NDX", "EURO","SP"]
                    },
        "SPOT": {"times": ["0500", "0900", "1000", "1730"],
                 "tickers": ["NIK", "RUSS", "FTSE", "NDX", "EURO","SP"]

                 },

    },

    "YahooFinance": {
        "CLOSING": {"times": ["EOD"],
                    "tickers": ["NIK", "RUSS", "FTSE", "NDX", "EURO","SP"]
                    },
        "SPOT": {"times": ["0500", "0900", "1000", "1730"],
                 "tickers": ["NIK", "RUSS", "FTSE", "NDX", "EURO","SP"]

                 },
    },

}

requirements = {
    'minX': {
        '2130': {
            'Nikkei': ['InvestCo', 'CLOSING', 'EOD', 'NIK'],
            'NDX': ['InvestCo', 'CLOSING', 'EOD', 'NDX'],
            'SanP500': ['InvestCo', 'CLOSING', 'EOD', 'SP']
        },

        '0500': {
            'Nikkei': ['YahooFinance', 'SPOT', '0500', 'NIK'],
            'NDX': ['InvestCo', 'CLOSING', 'EOD', 'NDX'],
            'SanP500': ['InvestCo', 'CLOSING', 'EOD', 'SP']
        }
    }
}


def inject_requirements(session, requirements):
    for (strat_name,requirements_map) in requirements.items():
        for (job_name, job_requirements) in requirements_map.items():
            for (instr_name, requirement_path) in job_requirements.items():
                find_instr_phrase = "MATCH (n:Instrument {{name:'{}'}}) return n".format(instr_name)
                instr_node_id = session.write_transaction(lambda tx: tx.run(find_instr_phrase)).single()['n'].id

                find_job_phrase = "MATCH (n:Job {{due_by:'{}'}}) return n".format(job_name)
                job_node_id = session.write_transaction(lambda tx: tx.run(find_job_phrase)).single()['n'].id

                observation_insert_phrase = "CREATE(n:Observation) RETURN n"
                obs_node_id = session.write_transaction(lambda tx: tx.run(observation_insert_phrase)).single()['n'].id

                link_prhase = "MATCH (obs),(job) where id(obs) = {} and id(job) = {} CREATE (job)-[r:NEEDS]->(obs) return r".format(obs_node_id,job_node_id)
                session.write_transaction(lambda tx:tx.run(link_prhase))
                link_prhase = "MATCH (obs),(instr) where id(obs) = {} and id(instr) = {} CREATE (instr)-[r:NEEDS]->(obs) return r".format(
                    obs_node_id, instr_node_id)
                session.write_transaction(lambda tx: tx.run(link_prhase))


                find_feed_point_prhase = "MATCH (PriceFeed {{name: '{}'}})--(FeedField {{ name: '{}'}})--(FeedTicker {{name: '{}'}})--(n: Capture {{name:'{}'}}) return n"\
                    .format(requirement_path[0],requirement_path[1],requirement_path[3],requirement_path[2])
                find_results =session.write_transaction(lambda  tx: tx.run(find_feed_point_prhase))
                print(find_feed_point_prhase)
                print (find_results.single())


def inject_feeds(session, feed_points):
    for (feed_name, feed_info) in feed_points.items():
        price_feed_phrase = "CREATE (z:PriceFeed {{name:'{}'}}) return z".format(feed_name, feed_name)
        feed_id_result = session.write_transaction(lambda tx: tx.run(price_feed_phrase))
        feed_id = feed_id_result.single()['z'].id
        for (field_value, field_value_info) in feed_info.items():
            field_phrase = "match(n) WHERE id(n) = {} CREATE(n)-[:HAS_FIELD]->(z:FeedField {{name:'{}'}}) RETURN z".format(
                feed_id, field_value, field_value)
            field_insert_result = session.write_transaction(lambda tx: tx.run(field_phrase))
            field_id = field_insert_result.single()['z'].id
            for ticker in field_value_info['tickers']:
                add_ticker_phrase = "match(n) WHERE id(n) = {} CREATE(n)-[:HAS_TICKER]->(z:FeedTicker {{name:'{}'}} ) RETURN z".format(
                    field_id, ticker, ticker)
                result = session.write_transaction(lambda tx: tx.run(add_ticker_phrase))
                ticker_id = result.single()['z'].id
                for time in field_value_info['times']:
                    time_insert_phrase = "match(n) WHERE id(n) = {} CREATE(n)-[:CAPUTURES]->(z:Capture {{name:'{}'}} ) RETURN z".format(
                        ticker_id, time, time)
                    session.write_transaction(lambda tx: tx.run(time_insert_phrase))




class DbSetup():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def clean(self):
        with self._driver.session() as session:
            return session.write_transaction(self.delete_all)

    def setUp(self):
        with self._driver.session() as session:
            return session.write_transaction(self.set_up)

    def inject_requirements (self,job_requirements):
        with self._driver.session() as session:
            return inject_requirements(session, job_requirements)


    def insert_feeds(self, feed_points):
        with self._driver.session() as session:
            return inject_feeds(session, feed_points)

    @staticmethod
    def set_up(tx):
        return tx.run(setup_query)

    @staticmethod
    def delete_all(tx):
        tx.run("match (n) detach delete n")


path = os.path.dirname(os.path.realpath(__file__))
cypher_path = os.path.join(path, "neo4jsetup.cypher")
with open(cypher_path, 'r') as cypher_file:
    setup_query = cypher_file.read()

setup = DbSetup("bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687", user="", password="")

setup.clean()
setup.setUp()
setup.insert_feeds(feedpoints)
setup.inject_requirements(requirements)
setup.close()
