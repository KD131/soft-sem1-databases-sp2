// constraint app_id
create constraint app_id if not exists for (g:Game) require g.appId is unique