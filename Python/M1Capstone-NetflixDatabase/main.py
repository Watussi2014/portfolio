from src import db_setup, config, login
from simple_term_menu import TerminalMenu
import sys


def main_menu(db: db_setup.DbManager) -> None:
    """
    Print out a menu based on the usertype of the user connected to the database.
    """
    print(f"Welcome {db.user}, your are connected to the {db.db_name} database.")
    if db.get_usertype() == "admin":
        options = ["Open psql shell", "Add user", "Exit"]
        main_menu = TerminalMenu(options)
        menu_entry = main_menu.show()

        match menu_entry:
            case 0:
                db.open_shell()
            case 1:
                print("What type of user do you want to add ?")
                user_choice = ["Data Scientist", "Data Analyst"]
                user_menu = TerminalMenu(user_choice)
                user_entry = user_menu.show()
                match user_entry:
                    case 0:
                        db.create_user("DS")
                    case 1:
                        db.create_user("DA")
            case 2:
                sys.exit()

    else:
        options = ["Open psql shell", "Exit"]
        main_menu = TerminalMenu(options)
        menu_entry = main_menu.show()

        match menu_entry:
            case 0:
                print("open shell")
                db.open_shell()
            case 1:
                sys.exit()


def main():
    config.get_config()
    config_db = db_setup.access_config("DATABASE")
    server_url = config_db["server_url"]
    port = config_db["port"]
    db_name = config_db["db_name"]
    creditentials = login.prompt_login()

    postgre = db_setup.DbManager(
        creditentials[0], creditentials[1], server_url, port, "postgres"
    )

    if login.can_createdb(postgre) and not postgre.db_exist(db_name):
        print("Creating database...")
        postgre.init_db(db_name)
        db = db_setup.DbManager(
            creditentials[0], creditentials[1], server_url, port, db_name
        )
        db.init_table()
        db.populate_table()
        while True:
            main_menu(db)
    else:
        db = db_setup.DbManager(
            creditentials[0], creditentials[1], server_url, port, db_name
        )
        while True:
            main_menu(db)


if __name__ == "__main__":
    main()
