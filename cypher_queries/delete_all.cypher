// delete all
:auto match (n)
call {
    with n
    detach delete n
} in transactions