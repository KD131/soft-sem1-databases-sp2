// most played games
match (g:Game)<-[r:PLAY]-(u:User)
return
    g.title as title,
    count(u) as userBase,
    round(sum(r.hours)) as playtime,
    avg(r.hours) as avgPlaytime
order by userBase desc
limit 10