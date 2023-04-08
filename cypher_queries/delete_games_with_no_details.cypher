// delete games with no details
match (g:Game)
where g.appId is null
detach delete g