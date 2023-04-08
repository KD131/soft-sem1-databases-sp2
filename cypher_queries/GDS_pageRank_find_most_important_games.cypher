// GDS pageRank find most important games
call gds.pageRank.stream('games', {
    relationshipWeightProperty: 'hours'
})
yield nodeId, score
return gds.util.asNode(nodeId).title as title, score
order by score desc, title asc