
// completed calendar for a particular trading center, showing hols.
match (TradingCenter{code:'CMG'}) -[:NEXT*]->(m)-[:ON]->(dd)
return tc.code, dd.caption,labels(m)[0]



// all holiday centers which have holidays on a particular day

show all revisions for a time series
MATCH (n:Instrument{code:'FTSE'})-[:FEED]->(s:Source{code:'Bloomberg'})-[:EOD]->(ts:TimeSeries)-[:NEXT*]->(r)-[]->(rw:Row)-[:ON]->(wd:WeekDay)-[:ON]->(dt:Date)
return rw,dt
