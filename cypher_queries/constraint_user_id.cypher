// constraint user_id
create constraint user_id if not exists for (u:User) require u.userId is unique