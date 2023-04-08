// GDS project graph with both relationships
// default of 1.0
call gds.graph.drop('games');
call gds.graph.project(
    'games',
    ['Game', 'User'],
    ['PLAY', 'PURCHASE'],
    {
        relationshipProperties: {
            hours: { defaultValue: 1.0 }
        }
    }
)