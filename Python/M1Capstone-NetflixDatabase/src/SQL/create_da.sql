CREATE USER $user WITH PASSWORD '$pwd' ;
GRANT CONNECT ON DATABASE $db_name TO $user ;
GRANT USAGE ON SCHEMA public TO $user ;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO $user ;

INSERT INTO db_users (username, user_type)
VALUES ('$user', 'DA');