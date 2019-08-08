

CREATE (minX:Strategy {name: 'minX',description: 'Mini Weighted Global Strategy'})

CREATE (minX_1:Quote {description: 'minx PortfolioA', ticker:"MN1"})-[:PUBLISHED_BY]->(minX)
CREATE (minX_2:Quote {description: 'minx PortfolioB', ticker:"MN2"})-[:PUBLISHED_BY]->(minX)

// Markets

CREATE (NYSE:Market {name: "NYSE"})
CREATE (OSAKA:Market{name: "OSAKA"})

//  Markets -> Instruments <- Minx

CREATE
   (OSAKA)<-[:TRADES_ON]-(NIKKEI:Instrument { name: 'Nikkei', description: 'Nikkei 250'})-[:CONSTITUENT_OF {trading_unit:0.108794987}]->(minX)
	,(NYSE)<-[:TRADES_ON]-(SanP500:Instrument {name: 'SanP500',description: 'S&P 500 index'})-[:CONSTITUENT_OF {trading_unit:0.973359159796373}]->(minX)
	,(NYSE)<-[:TRADES_ON]-(NDX:Instrument {name: 'NDX', description: 'NASDAQ'})-[:CONSTITUENT_OF {trading_unit: 0.576564941}]->(minX)


CREATE
    (EOD1730: Job {due_by: '2130', name:'2135 US NYK Close'})<-[:EVAL]-(minX)
   ,(INTRA0500: Job {due_by: '0500', name:'0500 TOK CLose'})<-[:EVAL]-(minX)

CREATE
    (minX_1)-[:PARAMS{weight:1.5}]->(NIKKEI)
    ,(minX_1)-[:PARAMS{weight:0.25}]->(SanP500)
    ,(minX_1)-[:PARAMS{weight:1=0.25}]->(NDX)

    ,(minX_2)-[:PARAMS{weight:1}]->(NIKKEI)
    ,(minX_2)-[:PARAMS{weight:1}]->(SanP500)
    ,(minX_2)-[:PARAMS{weight:1}]->(NDX)
















