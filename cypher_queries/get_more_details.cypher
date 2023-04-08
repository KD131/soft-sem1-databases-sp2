// get more details
// add relationships like developer, genre etc.
load csv with headers from "file:///steam.csv" as row
match (g:Game) where apoc.text.compareCleaned(g.title, row.name)
// compareCleaned might match more than 1
with row, g, count(g) as count where count = 1
set
    g.appId = toInteger(row.appid),
    g.releaseDate = date(row.release_date)

foreach(dev in split(row.developer, ';') |
    merge (d:Developer {name: dev})
    merge (d)-[:DEVELOPED]->(g)
)
foreach(pub in split(row.publisher, ';') |
    merge (p:Publisher {name: pub})
    merge (p)-[:PUBLISHED]->(g)
)
foreach(cat in split(row.categories, ';') |
    merge (c:Category {name: cat})
    merge (g)-[:HAS]->(c)
)
foreach(genre in split(row.genres, ';') |
    merge (gen:Genre {name: genre})
    merge (g)-[:IS_A]->(gen)
)