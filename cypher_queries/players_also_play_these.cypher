// players also play these
match (s:Game {title: $title})<-[:PLAY]-(u:User)-[:PLAY]->(t:Game)
where (s)-->(:Genre)<--(t)
return t.title as title, count(*) as cnt
order by cnt desc
limit 10