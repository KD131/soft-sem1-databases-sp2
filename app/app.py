import pandas as pd
from graphdatascience import GraphDataScience
from modules.secrets import NEO4J_AUTH, NEO4J_URI


def game_recommendations(gds: GraphDataScience, game_title: str, limit: int=10) -> pd.DataFrame:
    """Recommend games similar to the given game title."""
    games = gds.run_cypher(
        """
        match (s:Game {title: $title})<-[:PLAY]-(u:User)-[:PLAY]->(t:Game)
        where (s)-->(:Genre)<--(t)
        return t.title as Title, count(*) as Count
        order by Count desc
        limit $limit
        """,
        params={
            "title": game_title,
            "limit": limit
        },
        database='neo4j'
    )
    # Index from 1. Could also use RangeIndex or normal range.
    games.index += 1
    return games

def project_graph(gds: GraphDataScience):
    return gds.graph.project(
        'games',
        ['Game', 'User'],
        ['PLAY', 'PURCHASE'],
        relationshipProperties={
            'hours': { 'defaultValue': 1.0 }
        }
    )

def most_important_games(gds: GraphDataScience, G, limit: int=10):
    df = gds.eigenvector.stream(G, relationshipWeightProperty='hours')
    df.sort_values(by='score', ascending=False, inplace=True)
    df = pd.DataFrame(df.head(limit))
    df.index = pd.RangeIndex(start=1, stop=len(df)+1)   # this is also limit + 1
    ids = df['nodeId'].to_list()
    nodes = gds.util.asNodes(ids)
    titles = [node['title'] for node in nodes]
    df.insert(1, 'Title', titles)
    return df

def game_recommendation_menu(gds: GraphDataScience):
    while True:
        game_title = input("Enter a game title (or '0' to exit): ")
        if game_title == '0':
            break
        else:
            games = game_recommendations(gds, game_title)
            if len(games) == 0:
                print(f"No recommendations for {game_title}")
            else:
                print(games)

def main():
    gds = GraphDataScience(NEO4J_URI, NEO4J_AUTH, database='neo4j')
    G = None

    print(f"Connected to Neo4j database version {gds.version()}")
    while True:
        print("1. Game recommendations")
        print("2. Most 'important' games")
        print("0. Exit (or 'quit', '\q')")
        command = input("Please select an option: ")
        
        if command in ['0', 'quit', '\q']:
            break
        elif command == '1':
            game_recommendation_menu(gds)
        elif command == '2':
            if G is None:
                try:
                    G = gds.graph.get('games')
                except:
                    G, _ = project_graph(gds)
            games = most_important_games(gds, G)
            print(games)
        
    gds.close()

if __name__ == "__main__":
    main()