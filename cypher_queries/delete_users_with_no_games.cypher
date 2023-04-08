// delete users with no games
match (u:User)
where not (u)-->(:Game)
detach delete u