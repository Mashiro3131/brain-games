import mysql.connector
import contextlib
import functools
import bcrypt
import random
import string
import colorama
from colorama import Fore
colorama.init(autoreset=True)
import datetime
import hashlib



class Database:
    def __init__(self, host, port, user, password, database):
        self.config = {
            '127.0.0.1': host,
            '3306': port,
            'root': user,
            'root': password,
            'brain_games_db': database,
            'buffered': True,
            'autocommit': True
        }

    @contextlib.contextmanager
    def connect(self):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            connection.close()

    def with_connection(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with self.connect() as cursor:
                return func(self, cursor, *args, **kwargs)
        return wrapper
    
    @with_connection
    def create_database(self, cursor):
        try:  
            
            # Create Database braingames_db
            create_database_braingames_query = ("""
                CREATE DATABASE IF NOT EXISTS `braingames_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
            """)
            
            cursor.execute(create_database_braingames_query)
            print(Fore.GREEN + "Database `braingames_db` created successfully")
        
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error creating database: {error}")

    @with_connection
    def create_database_structure(self, cursor):
        try:
            # Use Database braingames_db
            use_database_braingames_query = ("""
            cursor.execute("USE `braingames_db`;")
            """)
            
            cursor.execute(use_database_braingames_query)
            
            # Table Results
            create_table_results_query = ("""
                CREATE TABLE IF NOT EXISTS `results` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `user_id` int(11) NOT NULL,
                    `exercise` varchar(50) NOT NULL,
                    `date_hour` datetime NOT NULL,
                    `duration` time NOT NULL,
                    `nbtrials` int(11) NOT NULL,
                    `nbok` int(11) NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
                );
            """)
            
            cursor.execute(create_table_results_query)
            
            # Table Roles
            create_table_roles_query = ("""
                CREATE TABLE IF NOT EXISTS `roles` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `name` varchar(50) NOT NULL,
                    PRIMARY KEY (`id`)
                );
            """)
            
            cursor.execute(create_table_roles_query)
            
            # Table Users
            create_table_users_query = ("""
                CREATE TABLE IF NOT EXISTS `users` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                    `pseudo` varchar(50) NOT NULL,
                    `password` varchar(255) DEFAULT NULL,
                    `role_id` int(11) NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
                );
            """)
            
            cursor.execute(create_table_users_query)
            
            print(Fore.GREEN + "Tables `results`, `roles`, and `users` created successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error creating tables: {error}")
            
    @with_connection
    def insert_roles(self, cursor):
        try:
            # Insert Roles
            insert_roles_query = ("""
                INSERT INTO `roles` (`id`, `name`) VALUES
                (1, 'student'),
                (2, 'teacher');
                (3, 'guest');
                (4, 'admin');
            """)
            
            cursor.execute(insert_roles_query)
            
            print(Fore.GREEN + "Roles inserted successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error inserting roles: {error}")

    @with_connection
    def insert_users(self, cursor):
        try:
            # Insert Users # passwords will be hashed
            insert_users_query = ("""
                INSERT INTO `users` (`id`, `pseudo`, `password`, `role_id`) VALUES
                (1, 'student1', 'Stud3ntPass', 1),
                (2, 'guestuser', 'gue5tP@ss', 3),
                (3, 'adminuser', 'Adm1n$ecure', 4),
                (4, 'teacher1', 'Teach3rPwd', 2),
                (5, 'student2', 'Pass4Stud', 1),
                (6, 'guest2', 'GuestPass123', 3),
                (8, 'teacher2', 'T3acherSec', 2);
            """)
            
            cursor.execute(insert_users_query)
            
            print(Fore.GREEN + "Users inserted successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error inserting users: {error}")
            
    @with_connection
    def insert_results(self, cursor):
        try:
            # Insert Results
            insert_results_query = ("""
                INSERT INTO `results` (`id`, `user_id`, `exercise`, `date_hour`, `duration`, `nbtrials`, `nbok`) VALUES
                (1, 1, 'GEO01', '2021-05-25 12:00:00', '00:10:00', 5, 3),
                (2, 2, 'INFO02', '2021-05-26 14:30:00', '00:15:00', 6, 4),
                (3, 3, 'INFO05', '2021-05-27 09:45:00', '00:20:00', 4, 4),
                (4, 4, 'GEO01', '2021-05-28 11:00:00', '00:10:00', 3, 2),
                (5, 1, 'INFO02', '2021-05-29 10:15:00', '00:18:00', 5, 5),
                (6, 2, 'INFO05', '2021-05-30 13:20:00', '00:12:00', 7, 6),
                (7, 3, 'GEO01', '2021-05-31 16:00:00', '00:10:00', 5, 3),
                (8, 4, 'INFO02', '2021-06-01 08:30:00', '00:15:00', 6, 6),
                (9, 1, 'INFO05', '2021-06-02 12:00:00', '00:20:00', 4, 3);
            """)
            
            cursor.execute(insert_results_query)
            
            print(Fore.GREEN + "Results inserted successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error inserting results: {error}")
            
    @with_connection
    def save_game_results(self, cursor, pseudo, exercise, duration, nbtrials, nbok):
        try:
            
            user_check_query = """
                SELECT id 
                FROM users 
                WHERE pseudo = %s
            """
            
            cursor.execute(user_check_query, (pseudo,))
            user = cursor.fetchone()
            
            if user is None:
                insert_user_query = ("""
                    INSERT INTO users (pseudo, role_id)
                    VALUES (%s, 3)
            """)
                
                
                cursor.execute(insert_user_query, (pseudo,))
                user_id = cursor.lastrowid
            else:
                user_id = user[0]
                
            record_match_outcome_query = ("""
                INSERT INTO results (user_id, exercise, date_hour, duration, nbtrials, nbok)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            
            values = (user_id, exercise, datetime.datetime.now(), duration, nbtrials, nbok)
            cursor.execute(record_match_outcome_query, values)
            
            print(Fore.GREEN + f"Game match result has been saved successfully for {pseudo}.")
            
        except mysql.connector.Error as error:
            print(Fore.RED + f"Failed to save game match: {error}")



    """
        the role id will be defined by the user's choice of occupation in le new_login.py file, 
        if he chooses occupation of student, it will give the student the role 1
        if he chooses teacher it will be role 2
        if he doesn't log in and starts playing it will create a random guest name with role 3 of guest

    """
    
    @with_connection
    def register_user(self, cursor, pseudo, password):
        try:
            # Hash a password for the first time, with a randomly-generated salt
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert User
            insert_user_query = ("""
                INSERT INTO `users` (`pseudo`, `password`, `role_id`) VALUES
                (%s, %s, 1);
            """)
            
            cursor.execute(insert_user_query, (pseudo, hashed))
            
            print(Fore.GREEN + f"User {pseudo} registered successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error registering user: {error}")
    
    
    
    
    @with_connection
    def fetch_game_statistics(self, cursor, pseudo=None, exercise=None, start_date=None, end_date=None, page=1, page_size=20):
        try:
            # Building the WHERE clause
            where_clauses = []
            params = []
            if pseudo:
                where_clauses.append("users.pseudo = %s")
                params.append(pseudo)
            if exercise:
                where_clauses.append("results.exercise = %s")
                params.append(exercise)
            if start_date:
                where_clauses.append("results.date_hour >= %s")
                params.append(start_date)
            if end_date:
                where_clauses.append("results.date_hour <= %s")
                params.append(end_date)

            where_statement = " AND ".join(where_clauses) if where_clauses else "1=1"

            # Pagination setup
            offset = (page - 1) * page_size
            limit_statement = "LIMIT %s OFFSET %s"
            params.extend([page_size, offset])

            # Construct and execute the main query
            main_query = f"""
                SELECT users.pseudo, results.exercise, results.date_hour, results.duration, results.nbtrials, results.nbok
                FROM results
                JOIN users ON users.id = results.user_id
                WHERE {where_statement}
                ORDER BY results.date_hour DESC
                {limit_statement}
            """
            cursor.execute(main_query, params)
            results = cursor.fetchall()

            # Construct and execute the count query
            count_query = f"""
                SELECT COUNT(*)
                FROM results
                JOIN users ON users.id = results.user_id
                WHERE {where_statement}
            """
            cursor.execute(count_query, params[:-2])  # Exclude pagination parameters
            total = cursor.fetchone()[0]

            return results, total

        except mysql.connector.Error as error:
            print(Fore.RED + f"Error fetching results: {error}")
            return [], 0

    # @with_connection
    # def fetch_game_statistics(self, cursor, pseudo=None, exercise=None, start_date=None, end_date=None, page=1, page_size=20):
    #     results = []
    #     total = None
    #     try:
    #         # Fetch Results
    #         fetch_results_query = ("""
    #             SELECT `pseudo`, `exercise`, `date_hour`, `duration`, `nbtrials`, `nbok`
    #             FROM `results` 
    #             JOIN `users` ON `users`.`id` = `results`.`user_id`
    #             WHERE 1=1
    #         """)

    #         params = []
    #         if pseudo:
    #             fetch_results_query += " AND `pseudo` = %s"
    #             params.append(pseudo)
    #         if exercise:
    #             fetch_results_query += " AND `exercise` = %s"
    #             params.append(exercise)
    #         if start_date:
    #             fetch_results_query += " AND `date_hour` >= %s"
    #             params.append(start_date)
    #         if end_date:
    #             fetch_results_query += " AND `date_hour` <= %s"
    #             params.append(end_date)
                
    #         fetch_results_query += " ORDER BY `date_hour` DESC"
            
    #         # Pagination 
    #         offset = (page - 1) * page_size
    #         fetch_results_query += " LIMIT %s OFFSET %s"
    #         params.append(page_size, offset)
            
    #         cursor.execute(fetch_results_query, params)
    #         results = cursor.fetchall()
            
    #         # Fetch Total
    #         fetch_total_query = ("""
    #             SELECT COUNT(*)
    #                 FROM results r
    #                 INNER JOIN users u ON r.user_id = u.id
    #                 WHERE 1 = 1
    #         """)
            
    #         if pseudo or exercise or start_date or end_date:
    #             fetch_total_query += fetch_results_query.split("WHERE")[1].replace("LIMIT %s OFFSET %s", "")
    #             cursor.execute(fetch_total_query, tuple(params[:-2]))  # Exclure les paramètres de pagination
    #             total = cursor.fetchone()[0]
        
    #         print(Fore.GREEN + f"Results fetched successfully")
            
    #     except mysql.connector.Error as error:
    #         print(Fore.RED + f"Error fetching results: {error}")
            
    #     return results, total

          
    @with_connection
    def check_user_is_logged(self, cursor, pseudo, password):
        try:
            # Check User
            check_user_query = ("""
                SELECT `password` FROM `users` WHERE `pseudo` = %s;
            """)
            
            cursor.execute(check_user_query, (pseudo,))
            
            user = cursor.fetchone()
            
            if user:
                hashed = user[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed):
                    print(Fore.GREEN + f"User {pseudo} logged in successfully")
                    return True
                else:
                    print(Fore.RED + f"User {pseudo} failed to log in")
                    return False
            else:
                print(Fore.RED + f"User {pseudo} failed to log in")
                return False
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error checking user: {error}")
            
    @with_connection
    def update_game_result(self, cursor, pseudo, exercise, date_hour, duration, nbok, nbtrials, new_duration, new_nbok, new_nbtrials):
        try:
            # Retrieve the user_id for the given pseudo
            user_id_query = "SELECT id FROM users WHERE pseudo = %s"
            cursor.execute(user_id_query, (pseudo,))
            user_id_result = cursor.fetchone()

            if not user_id_result:
                print(Fore.YELLOW + "Aucun utilisateur trouvé avec ce pseudo.")
                return
            user_id = user_id_result[0]

            # Attempt to update the specific game result
            update_query = """
            UPDATE results 
            SET duration = %s, nbok = %s, nbtrials = %s 
            WHERE user_id = %s AND exercise = %s AND date_hour = %s
            """
            update_values = (new_duration, new_nbok, new_nbtrials, user_id, exercise, date_hour)

            cursor.execute(update_query, update_values)
            if cursor.rowcount == 0:
                print(Fore.YELLOW + "Aucun enregistrement correspondant trouvé pour mise à jour.")
            else:
                print(Fore.GREEN + f"{cursor.rowcount} ligne(s) mise(s) à jour.")

        except mysql.connector.Error as error:
            print(Fore.RED + f"Échec de la mise à jour du résultat du jeu : {error}")
 
    @with_connection
    def update_game_result_by_id(self, cursor, result_id, new_duration, new_nbok, new_nbtrials):
        try:
            update_query = """
            UPDATE results 
            SET duration = %s, nbok = %s, nbtrials = %s 
            WHERE id = %s
            """
            update_values = (new_duration, new_nbok, new_nbtrials, result_id)
            cursor.execute(update_query, update_values)

            if cursor.rowcount == 0:
                print(Fore.YELLOW + "Aucun enregistrement correspondant trouvé pour mise à jour.")
            else:
                print(Fore.GREEN + f"{cursor.rowcount} ligne(s) mise(s) à jour.")

        except mysql.connector.Error as error:
            print(Fore.RED + f"Échec de la mise à jour du résultat du jeu : {error}") 
 
                        
    # @with_connection
    # def update_game_results(self, cursor, pseudo, exercise, date_hour, duration, nbtrials, nbok, new_duration, new_nbok, new_nbtrials):
    #     try:
    #         # Retrieve the user_id for the given pseudo
    #         user_id_query = "SELECT id FROM users WHERE pseudo = %s"
    #         cursor.execute(user_id_query, (pseudo,))
    #         user_id_result = cursor.fetchone()

    #         if not user_id_result:
    #             print(Fore.YELLOW + "Aucun utilisateur trouvé avec ce pseudo.")
    #             return
    #         user_id = user_id_result[0]

    #         # Check if the specific game result exists
    #         check_query = """
    #         SELECT COUNT(*) 
    #         FROM results 
    #         WHERE user_id = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s
    #         """
    #         cursor.execute(check_query, (user_id, exercise, date_hour, duration, nbok, nbtrials))
    #         (match_count,) = cursor.fetchone()

    #         # If the row exists, update it
    #         if match_count > 0:
    #             update_query = """
    #             UPDATE results 
    #             SET duration = %s, nbok = %s, nbtrials = %s 
    #             WHERE user_id = %s AND exercise = %s AND date_hour = %s
    #             """
    #             update_values = (new_duration, new_nbok, new_nbtrials, user_id, exercise, date_hour)

    #             cursor.execute(update_query, update_values)
    #             if cursor.rowcount == 0:
    #                 print(Fore.YELLOW + "No matching record found for update.")
    #             else:
    #                 print(Fore.GREEN + f"{cursor.rowcount} line(s) updated.")
    #         else:
    #             print(Fore.YELLOW + "No matching line found for update.")

    #     except mysql.connector.Error as error:
    #         print(Fore.RED + f"Failed to update game result: {error}")


    @with_connection
    def logout_user(self, cursor, pseudo):
        try:
            # Check User
            check_user_query = ("""
                SELECT `pseudo` FROM `users` WHERE `pseudo` = %s;
            """)
            
            cursor.execute(check_user_query, (pseudo,))
            
            user = cursor.fetchone()
            
            if user:
                print(Fore.GREEN + f"User {pseudo} logged out successfully")
                return True
            else:
                print(Fore.RED + f"User {pseudo} failed to log out")
                return False
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error checking user: {error}") 
           
    @with_connection
    def register_user(self, cursor, pseudo, password, role_id):
        try:
            # Check if user already exists
            check_user_query = ("""
                SELECT COUNT(*) FROM `users` WHERE `pseudo` = %s;
            """)
            cursor.execute(check_user_query, (pseudo,))
            result = cursor.fetchone()
            if result[0] > 0:
                print(Fore.RED + f"Username {pseudo} is already taken")
                return False
            else:
                print(Fore.GREEN + f"Username {pseudo} is available")

            # Hash a password for the first time, with a randomly-generated salt
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert User
            insert_user_query = ("""
                INSERT INTO `users` (`pseudo`, `password`, `role_id`) VALUES
                (%s, %s, %s);
            """)

            cursor.execute(insert_user_query, (pseudo, hashed, role_id))

            print(Fore.GREEN + f"User {pseudo} has successfully been created. Enjoy the game!")
            return True
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error registering user: {error}")
            return False
       
     
    # this will create a guest user with a random name with the prefix guest and a random number between 1 and 1000
    @with_connection       
    def guest_user(self, cursor):
        try:
            # Insert User
            insert_user_query = ("""
                INSERT INTO `users` (`pseudo`, `role_id`) VALUES
                ('guest' + CAST(RAND() * 1000 AS CHAR), 3);
            """)
            
            cursor.execute(insert_user_query)
            
            print(Fore.GREEN + f"Guest user registered successfully")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error registering guest user: {error}")
        
        
    @with_connection
    def check_if_user_exits(self, cursor, pseudo):
        try:
            # Check User
            check_user_query = ("""
                SELECT `pseudo` FROM `users` WHERE `pseudo` = %s;
            """)
            
            cursor.execute(check_user_query, (pseudo,))
            
            user = cursor.fetchone()
            
            if user:
                print(Fore.GREEN + f"User {pseudo} exists")
                return True
            else:
                print(Fore.RED + f"User {pseudo} does not exist")
                return False
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error checking user: {error}")
            
            
            
            
            
            
    """ LOGIN / REGISTER / GUEST / LOGOUT """
    
    def login_user(self, cursor, pseudo, password):
        try:
            # Query to find user by pseudo
            user_query = "SELECT id, password FROM users WHERE pseudo = %s"
            cursor.execute(user_query, (pseudo,))
            user = cursor.fetchone()

            # Check if user exists
            if user:
                user_id, hashed_password = user
                # Verify the password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    print(Fore.GREEN + "Login successful.")
                    
                    # Return the user id
                    return user_id
                else:
                    # Incorrect password
                    print(Fore.RED + "Incorrect password.")
                    return None
            else:
                # User not found
                print(Fore.RED + "User not found.")
                return None

        except mysql.connector.Error as error:
            print(Fore.RED + f"Error during login: {error}")
            return None    


    @with_connection
    def register_user(self, cursor, pseudo, password, role_id):
        try:
            # Checks if the user already exists
            if self.is_user_exist(cursor, pseudo):
                print(Fore.RED + "Username already taken.")
                return False

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert new user (Database insertion)
            insert_user_query = """
                INSERT INTO users (pseudo, password, role_id) VALUES (%s, %s, %s)
            """
            cursor.execute(insert_user_query, (pseudo, hashed_password, role_id))

            print(Fore.GREEN + "User registered successfully.")
            return True

        except mysql.connector.Error as error:
            print(Fore.RED + f"Error registering user: {error}")
            return False
    
    @with_connection
    def is_user_exist(self, cursor, pseudo):
        """Check if a user already exists in the database."""
        check_user_query = "SELECT 1 FROM users WHERE pseudo = %s"
        cursor.execute(check_user_query, (pseudo,))
        return cursor.fetchone() is not None
    
    
    @with_connection
    def continue_as_guest(self, cursor):
        try:
            # Generate a unique guest username with a hash-like style
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            guest_username = f"guest{hashlib.md5(random_str.encode()).hexdigest()[:10]}"

            # Generate a random password
            guest_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            # Create guest account with a default guest role (assuming role_id for guest is 3)
            if self.register_user(cursor, guest_username, guest_password, role_id=3):
                print(Fore.GREEN + f"Guest account created. Username: {guest_username}, Password: {guest_password}")
                return guest_username, guest_password
            else:
                print(Fore.RED + "Failed to create guest account.")
                return None, None

        except mysql.connector.Error as error:
            print(Fore.RED + f"Error in guest account creation: {error}")
            return None, None