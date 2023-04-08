// import csv
// should've trimmed
load csv from "file:///steam-200k.csv" as row
with toInteger(row[0]) as userId, row[1] as title, toUpper(row[2]) as relation, toFloat(row[3]) as hours
merge (u:User {userId:userId})
merge (g:Game {title:title})
with u, g, relation, hours
call apoc.do.case([
    relation = 'PURCHASE', "merge (u)-[r:PURCHASE]->(g)",
    relation = 'PLAY', "merge (u)-[r:PLAY {hours:hours}]->(g)"],
    '',
    {u:u, g:g, hours:hours}
)
yield value
return value