import pandas as pd
from graphdatascience import GraphDataScience
from modules.secrets import NEO4J_AUTH, NEO4J_URI


def game_recommendations(gds: GraphDataScience, game_title: str, limit: int=10) -> pd.DataFrame:
    """Recommend games similar to the given game title."""
    return gds.run_cypher(
        """
        match (s:Game {title: $title})<-[:PLAY]-(u:User)-[:PLAY]->(t:Game)
        where (s)-->(:Genre)<--(t)
        return t.title as title, count(*) as cnt
        order by cnt desc
        limit $limit
        """,
        params={
            "title": game_title,
            "limit": limit
        },
        database='neo4j'
    )

def main():
    gds = GraphDataScience(NEO4J_URI, NEO4J_AUTH, database='neo4j')
    print(f"Connected to Neo4j database version {gds.version()}")
    while True:
        game_title = input("Enter a game title (or 'quit' to exit): ")
        if game_title == "quit":
            break
        else:
            games = game_recommendations(gds, game_title)
            if len(games) == 0:
                print(f"No recommendations for {game_title}")
            else:
                print(games)
    gds.close()

if __name__ == "__main__":
    main()