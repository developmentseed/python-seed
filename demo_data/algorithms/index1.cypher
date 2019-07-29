CREATE (tWIGy:IndexGroup {description: 'Weighted Index Global'})
CREATE (tWIGy1:PublishedIndex {description: 'Weighted Index Global PortfolioA', ticker:"TWA"})
CREATE (tWIGy2:PublishedIndex {description: 'Weighted Index Global PortfolioB',ticker:"TWB"})
CREATE (tWIGy1)-[:PUBLISHED_BY]->(tWIGy)
CREATE (tWIGy2)-[:PUBLISHED_BY]->(tWIGy)



CREATE
   (NIKKEI:Instrument {description: 'Nikkei 250'})-[:CONSTITUENT_OF {trading_unit:0.108794987}]->(tWIGy)
  ,(HANGSENG:Instrument {description: 'HangSeng Equities Index'})-[:CONSTITUENT_OF {trading_unit:0.049679591}]->(tWIGy)
	,(FTSE:Instrument {description: 'FTSE100'})-[:CONSTITUENT_OF {trading_unit:0.208081901}]->(tWIGy)
	,(EURO50:Instrument {description: 'EuroStox 50'})-[:CONSTITUENT_OF {trading_unit:0.430203744493392}]->(tWIGy)
	,(SanP500:Instrument {description: 'S&P 500 index'})-[:CONSTITUENT_OF {trading_unit:0.973359159796373}]->(tWIGy)
	,(NDX:Instrument {description: 'NASDAQ'})-[:CONSTITUENT_OF]->(tWIGy)
	,(BOV:Instrument {description: 'Brasilian'})-[:CONSTITUENT_OF]->(tWIGy)
	,(ASX:Instrument {description: 'Aussie equities index'})-[:CONSTITUENT_OF]->(tWIGy)
	,(CAC40:Instrument {description: 'Credit Agricole 40'})-[:CONSTITUENT_OF]->(tWIGy)
	,(IBEX35:Instrument {description: 'IBEX 35'})-[:CONSTITUENT_OF]->(tWIGy)


CREATE
    (EOD1730: Job {due_by: '1730'})<-[:EVAL]-(tWIGy)
   ,(INTRA0500: Job {due_by: '0500'})<-[:EVAL]-(tWIGy)




CREATE
   (NIKKEI)<-[:REQUIRES {source: 'EOD', date_t_offset: '0' }]-(EOD1730)
  ,(HANGSENG)<-[:REQUIRES]-(EOD1730)
	,(FTSE)<-[:REQUIRES]-(EOD1730)
	,(EURO50)<-[:REQUIRES]-(EOD1730)
	,(SanP500)<-[:REQUIRES]-(EOD1730)
	,(NDX)<-[:REQUIRES]-(EOD1730)
	,(BOV)<-[:REQUIRES]-(EOD1730)
	,(ASX)<-[:REQUIRES]-(EOD1730)
	,(CAC40)<-[:REQUIRES]-(EOD1730)
	,(IBEX35)<-[:REQUIRES]-(EOD1730)

CREATE
   (NIKKEI)<-[:REQUIRES]-(INTRA0500)
  ,(HANGSENG)<-[:REQUIRES]-(INTRA0500)
	,(FTSE)<-[:REQUIRES]-(INTRA0500)
	,(EURO50)<-[:REQUIRES]-(INTRA0500)
	,(SanP500)<-[:REQUIRES]-(INTRA0500)
	,(NDX)<-[:REQUIRES]-(INTRA0500)
	,(BOV)<-[:REQUIRES]-(INTRA0500)
	,(ASX)<-[:REQUIRES]-(INTRA0500)
	,(CAC40)<-[:REQUIRES]-(INTRA0500)
	,(IBEX35)<-[:REQUIRES]-(INTRA0500)









