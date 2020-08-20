
# Casting Agency

The project is to simulate a casting agency. This includes having actors and movies and assigning actors to movies.

## Database
containes two tables Movie with attriutes realse_date, title and an id, and the tables Actor with attriutes age, gender, name and id. 
## Authentication & Authorization
To login or set up an account, go to the following url: 

```
https://fouz.us.auth0.com/authorize?audience=capstoneApi&response_type=token&client_id=B6WTJQmdVNv5xgSm51kbbZw2WLI0YLfW&redirect_uri=https://ne-ya-ha-ha-ha.herokuapp.com/
```

After login you will see an access_token in the url path.

```
https://ne-ya-ha-ha-ha.herokuapp.com//#access_token=<ACCESS_TOKEN>&expires_in=7200&token_type=Bearer
```

There are three roles within the API. ***Casting Assistant***, ***Casting Director*** and ***Executive Producer***. The logins for the three roles has been provided in the separate notes 

The url for the API:
```
https://ne-ya-ha-ha-ha.herokuapp.com/
```
