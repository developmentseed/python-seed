CREATE (minX:IndexGroup {description: 'Mini Weighted Global Strategy'})

CREATE (minX_1:PublishedIndex {description: 'minx PortfolioA', ticker:"MN1"})-[:PUBLISHED_BY]->(minX)
CREATE (minX_2:PublishedIndex {description: 'minx PortfolioB', ticker:"MN2"})-[:PUBLISHED_BY]->(minX)

// Markets

CREATE (NYSE:Market {name: "NYSE"})
CREATE (OSAKA:Market{name: "OSAKA"})

//  Markets -> Instruments <- Minx

CREATE
   (OSAKA)<-[:TRADES_ON]-(NIKKEI:Instrument {description: 'Nikkei 250'})-[:CONSTITUENT_OF {trading_unit:0.108794987}]->(minX)
	,(NYSE)<-[:TRADES_ON]-(SanP500:Instrument {description: 'S&P 500 index'})-[:CONSTITUENT_OF {trading_unit:0.973359159796373}]->(minX)
	,(NYSE)<-[:TRADES_ON]-(NDX:Instrument {description: 'NASDAQ'})-[:CONSTITUENT_OF {trading_unit: 0.576564941}]->(minX)


CREATE
    (EOD1730: Job {due_by: '1730'})<-[:EVAL]-(minX)
   ,(INTRA0500: Job {due_by: '0500'})<-[:EVAL]-(minX)

CREATE
     (EOD1730)-[:REQUIRES {feed: 'Investec', field:'SETTLE', time:'EOD', ticker: 'NIK'}]->(NIKKEI)
    ,(EOD1730)-[:REQUIRES {feed: 'Investec', field:'SETTLE', time:'EOD', ticker: 'NAS'}]->(NDX)
    ,(EOD1730)-[:REQUIRES {feed: 'Investec', field:'SETTLE', time:'EOD', ticker: 'SP'}]->(SanP500)

    ,(INTRA0500)-[:REQUIRES {feed: 'Google', field:'LATEST', time:'0500', ticker: 'NIK', fallback:'latest'}]->(NIKKEI)
    ,(INTRA0500)-[:REQUIRES {feed: 'Investec', field:'SETTLE', time:'EOD', ticker: 'NAS', t: -1}]->(NDX)
    ,(INTRA0500)-[:REQUIRES {feed: 'Investec', field:'SETTLE', time:'EOD', ticker: 'SP', t: -1}]->(SanP500)

CREATE
    (minX_1)-[:PARAMS{weight:1.5}]->(NIKKEI)
    ,(minX_1)-[:PARAMS{weight:0.25}]->(SanP500)
    ,(minX_1)-[:PARAMS{weight:1=0.25}]->(NDX)

    ,(minX_2)-[:PARAMS{weight:1}]->(NIKKEI)
    ,(minX_2)-[:PARAMS{weight:1}]->(SanP500)
    ,(minX_2)-[:PARAMS{weight:1}]->(NDX)




CREATE (Latest:PriceFieldType {name:'Latest'} )<-[:FIELD]-(BLOOMSON)
CREATE (SettlePrice:PriceFieldType {name:'SettlePrice'})<-[:FIELD]-(BLOOMSON)
CREATE (DayHigh:PriceFieldType {name:'High'})<-[:FIELD]-(BLOOMSON)

CREATE (H09M00 : Time {name: '0900'})<-[:TIMES]-(Latest)
CREATE (H10M00 : Time {name: '0100'})<-[:TIMES]-(SettlePrice)
CREATE (EOD : Time {name: 'EOD'})<-[:TIMES]-(DayHigh)













