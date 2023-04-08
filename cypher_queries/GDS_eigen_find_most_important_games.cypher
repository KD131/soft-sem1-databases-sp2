// GDS eigen find most important games
call gds.eigenvector.stream('games', {
    relationshipWeightProperty: 'hours'
})
yield nodeId, score
return gds.util.asNode(nodeId).title as title, score
order by score desc, title asc