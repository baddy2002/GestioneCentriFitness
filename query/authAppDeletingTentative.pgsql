DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_permission;
DROP TABLE IF EXISTS auth_group_permissions;



SELECT conname
FROM pg_constraint
WHERE confrelid = 'auth_user'::regclass;

select * from auth_user
select * from auth_group
select * from auth_permission
select * from auth_group_permission
select * from auth_user_groups
select * from auth_user_user_permissions
sel
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name
FROM
    pg_constraint
WHERE
    contype = 'f';



                """
                CREATE TABLE auth_user (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE NULL,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    first_name VARCHAR(30) NOT NULL,
                    last_name VARCHAR(30) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
                );
                CREATE TABLE auth_group (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) UNIQUE NOT NULL
                );
                """,
                """
                CREATE TABLE auth_permission (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id) ON DELETE CASCADE,
                    codename VARCHAR(100) NOT NULL
                );
                """,
                """
                CREATE TABLE auth_group_permissions (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
                    permission_id INTEGER NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE auth_user_groups (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    group_id INTEGER NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE
                );
                """