# SP2 (Graph Databases)
## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Datasets](#2-datasets)
- [3. Data](#3-data)
- [4. Graph algorithms](#4-graph-algorithms)
- [5. Python client application](#5-python-client-application)
- [6. Cypher queries](#6-cypher-queries)
- [7. Actual answers to the questions](#7-actual-answers-to-the-questions)

## 1. Introduction
Hello.

*A lot of this documentation was not required by the assignment. I just felt like writing it partly to describe my annoyances working with this data, and partly to procrastinate answering the questions in the assignment. I meander, sue me.*

I've built a recommendation engine for games on the [Steam](https://store.steampowered.com/) platform using [Neo4j](https://neo4j.com/).

Graph databases are ideal for recommendation engines because you can narrow down nodes that you are close to but currently have no connection with. Like a friend of a friend.

In this case, we try to find games related to game *x* that share a lot of players with game *y*. "Players who play *this* game also play *that* game, so you might like it."

## 2. Datasets
- [Steam Video Games by Tamber](https://www.kaggle.com/datasets/tamber/steam-video-games)
- [Steam Store Games (Clean dataset) by Nik Davis](https://www.kaggle.com/datasets/nikdavis/steam-store-games)

I wanted a dataset that linked games to users, so that I could find shared playerbases, and I found [this dataset](https://www.kaggle.com/datasets/tamber/steam-video-games) by Tamber on Kaggle which does just that. It contains 200,000 interactions between users and games, either playing or purchasing them, with an hour count.

It doesn't provide much data on the games, just the titles and not even a unique id. Trying to make recommendations with just the amount of players would almost always return the same games that have a huge playerbase, e.g. "Dota 2," "Team Fortress 2," and "Counter Strike: Global Offensive."

To add more detail, like genres, I used [this dataset](https://www.kaggle.com/datasets/nikdavis/steam-store-games) by Nik Davis on Kaggle. Because the other dataset only had titles to identify the games, and those titles are wildly inconsistent with this more professional set, matching them up was a pain. I thought of just removing characters like ™ and ®, so that games like "Darkest Dungeon" and "Darkest Dungeon®" and "The Elder Scroll V: Skyrim" with and without the colon would match. Thankfully, there's an [APOC](https://neo4j.com/docs/apoc/current/) function for [cleaning and comparing](https://neo4j.com/docs/apoc/current/misc/text-functions/#text-functions-data-cleaning) strings.

The cleaning took care of some issues, but there were still a lot of games that didn't have a match. Like 1/3 of the dataset. So they had to go. Likewise, with those games gone because they had no details on genres, the users who were only connected to those now deleted games also had to go.

The recommendations are still biased towards more popular games, but adding the condition that the games must also share a genre, wildly improved the relevancy of the recommendations.

There are other datasets that I looked at, and if I had more time and was required to build a more complex engine, then I could've added [tags](https://www.kaggle.com/datasets/trolukovich/steam-games-complete-dataset) as well as [reviews](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam) to the database.

## 3. Data
In the [data folder](/data/) I've included the datasets I used as described above, and an additional DUMP file of the database because I wasn't sure what "snapshots from the database" meant exactly.

## 4. Graph algorithms
I'll level with you, the whole of the recommendation use case is solved with a [normal Cypher query](/cypher_queries/players_also_play_these.cypher), but I needed to include a [graph algorithm](https://neo4j.com/docs/graph-data-science/current/algorithms/), so I went with [Eigenvector centrality](https://neo4j.com/docs/graph-data-science/current/algorithms/eigenvector-centrality/). It is used to find the most *important* nodes based on the nodes connected to it (incoming relationships) and the *weight* of those connections. Here we use the playtime in hours to add importance to the relationship. A node has a higher score if the nodes it's connected to also have a high score.

The result is not much different than just finding the node with [largest playbase or highest playtime](/cypher_queries/most_played_games.cypher), but it's an algorithm as per the assignment requirements.

## 5. Python client application
I decided to built the client application in Python because I knew there were packages for connecting to the database. There are actually two, one for the [Neo4j driver](https://neo4j.com/docs/python-manual/current/) and one for [GDS](https://neo4j.com/docs/graph-data-science-client/current/) specifically. That is the one I used, because it simplifies sending queries, supports the GDS algorithms, and returns [Pandas](https://pandas.pydata.org/) [DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

It's a very simple application. It's a menu with an infinite loop for inputting game titles and receiving recommendations.

I also added the [Eigenvector](#4-graph-algorithms) functionality for finding the most *important* nodes. That took a little wrangling to format correctly.

Given more time, I would've loved to expand the functionality a little more to allow you to select a game from the list of results you just received as the source for new recommendations. You would then input the index number from the list, and it would find new games. Daisy-chaining game recommendations.

Note that the file with the database credentials is ignored and thus not present in the repository.

## 6. Cypher queries
I've included all the queries I made in the [cypher_queries](/cypher_queries/) folder. These include the [import](/cypher_queries/import_csv.cypher) [queries](/cypher_queries/get_more_details.cypher) as well as the more interesting, functional ones, and those related to Graph Data Science (GDS).

Below are the queries for recommendations and most played games.

```cypher
// players also play these
match (s:Game {title: $title})<-[:PLAY]-(u:User)-[:PLAY]->(t:Game)
where (s)-->(:Genre)<--(t)
return t.title as title, count(*) as cnt
order by cnt desc
limit 10
```

```cypher
// most played games
match (g:Game)<-[r:PLAY]-(u:User)
return
    g.title as title,
    count(u) as userBase,
    round(sum(r.hours)) as playtime,
    avg(r.hours) as avgPlaytime
order by userBase desc
limit 10
```

## 7. Actual answers to the questions
1. *What are the advantages and disadvantages of using graph databases and which are the best and worse scenarios for it?*

Like I mentioned in the [introduction](#1-introduction), graph databases are great for highly related data. Social media where users are connected to each other with relationships are a great example. In this case, users are connected to lots of games that they own and play. Games are connected to developers and publishers, as well as different genres. Traversing these relationships are much more efficient in a graph than having to join large tables in SQL.

2. *How would you code in SQL the Cypher statements you developed for your graph algorithms-based query, if the same data was stored in a relational database?*

I honestly don't know exactly. I think it might involve some subqueries because we have to join back into the games table with a list of users.

This almost certainly will not work, but consider it an idea:

```sql
SELECT title, COUNT(*) cnt
FROM games g
    INNER JOIN games_users gu USING(game_id)
    INNER JOIN games_genres gg USING(game_id)
WHERE gu.user_id IN (
    SELECT user_id
    FROM games_users gu
        INNER JOIN games g USING(game_id)
    WHERE title = 'Darkest Dungeon'
)
AND -- something something, they share a genre.
GROUP BY title
ORDER BY cnt DESC
LIMIT 10
```

It would be a mess because we're traversing so many relationships. In a graph database, you just say "both have a connection to the same `:Genre` node."

3. *How does the DBMS you work with organizes the data storage and the execution of the queries?*

Data is stored in nodes. They are essentially linked lists. Each node contains references to its neighbours which makes accessing it very efficient.

Queries will be cached in the database for increased performance if the query is repeated. Probably.

4. *Which methods for scaling and clustering of databases you are familiar with so far?*

**Causal clustering** consists of a group of read/write servers (primaries) where one is the leader and the others are followers, and a group of read-only replicas (secondaries). When a change is performed in the leader, it is replicated to all other servers. If a the leader should go down, the others hold an election to pick the next leader to take over. This ensures uptime on the database server.

**Autonomous clustering** is where the servers can perform both primary and secondary responsibilities. The cluster decides what server does what at any given moment autonomously. This is a newer feaure only available on versions >= 5.