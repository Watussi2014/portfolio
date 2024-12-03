CREATE DATABASE "$db_name$"
                        WITH
                        OWNER = $db_user$
                        ENCODING = 'UTF8'
                        LOCALE_PROVIDER = 'libc'
                        CONNECTION LIMIT = -1
                        IS_TEMPLATE = False;