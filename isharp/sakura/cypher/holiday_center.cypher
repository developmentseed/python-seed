
// completed calendar for a particular trading center, showing hols.
match (TradingCenter{code:'CMG'}) -[:NEXT*]->(m)-[:ON]->(dd)
return tc.code, dd.caption,labels(m)[0]





//show all revisions for a time series
MATCH (n:Instrument{code:'FTSE'})-[:FEED]->(s:Source{code:'Bloomberg'})-[:EOD]->(ts:TimeSeries)-[:NEXT*]->(r)-[]->(rw:Row)-[:ON]->(wd:WeekDay)-[:ON]->(dt:Date)
return rw,dt


// show which stragegies depend on a trading center
MATCH(n:TradingCenter{code:'CMG'})<-[TRADES_ON]-(i:Instrument)<-[UsesComponent]-(strat:Strategy)
return n,strat

// show workflow for a strategy
MATCH (strat:Strategy {name: 'G3LongOnlyReturns'})-->(diary:DailySchedule)-[wfr:workflow]->(workflow:Workflow)-[:next*]->(phase:WorkPhase)-[:task*]->(task:Task)-[:produces]->(prod)<-[req:requires]-(requiredby)
RETURN *

// call timeseries stored proc
call sakura.timeseries('RUSS','Bloomberg','EOD')