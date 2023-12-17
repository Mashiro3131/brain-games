""" Database SQL Structure :

-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Sam 16 Décembre 2023 à 13:05
-- Version du serveur :  5.7.11
-- Version de PHP :  5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `brain_games_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `results`
--

CREATE TABLE IF NOT EXISTS `results` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `exercise` varchar(50) NOT NULL,
  `date_hour` datetime NOT NULL,
  `duration` time NOT NULL,
  `nbtrials` int(11) NOT NULL,
  `nbok` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Contenu de la table `results`
--

INSERT INTO `results` (`id`, `user_id`, `exercise`, `date_hour`, `duration`, `nbtrials`, `nbok`) VALUES
(1, 1, 'GEO01', '2023-12-04 00:00:00', '00:02:00', 2, 1),
(3, 1, 'INFO05', '2023-12-04 00:00:00', '00:02:00', 2, 1),
(4, 1, 'GEO01', '2023-12-04 00:00:00', '00:02:00', 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

CREATE TABLE IF NOT EXISTS `roles` (
`id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'eleve'),
(2, 'enseignant');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
`id` int(11) NOT NULL,
  `pseudo` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Contenu de la table `users`
--

INSERT INTO `users` (`id`, `pseudo`, `password`, `role_id`) VALUES
(1, 'NME', '1234', 1);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `results`
--
ALTER TABLE `results`
 ADD PRIMARY KEY (`id`), ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `roles`
--
ALTER TABLE `roles`
 ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
 ADD PRIMARY KEY (`id`), ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `results`
--
ALTER TABLE `results`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `roles`
--
ALTER TABLE `roles`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `results`
--
ALTER TABLE `results`
ADD CONSTRAINT `results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `users`
--
ALTER TABLE `users`
ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


"""



import contextlib
import mysql.connector
import colorama
import datetime
from colorama import Fore, Style



colorama.init(autoreset=True)



class DatabaseConnection:
    def __init__(self, host, port, user, password, database):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
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



# Creating an instance of DatabaseConnection
db_connection = DatabaseConnection('127.0.0.1', '3306', 'root', 'root', 'brain_games_db')



# (CREATE) Insert results
def record_match_outcome(pseudo, exercise, duration, nbtrials, nbok):
    try:
        with db_connection.connect() as cursor:
            
            # Regarde si l'utilisateur existe déjà dans la base de données
            user_check_query = """
                SELECT id 
                FROM users 
                WHERE pseudo = %s
            """
            
            # Exécute la requête
            cursor.execute(user_check_query, (pseudo,))
            user = cursor.fetchone()

            # Si l'utilisateur n'existe pas, on le crée
            if user is None:
                # Insère le nouvel utilisateur dans la table users (momentanément, on lui attribue le rôle (1) d'élève par défaut)
                insert_user_query = """
                    INSERT INTO users (pseudo, role_id) 
                    VALUES (%s, %s)
                """
                
                # Exécute la requête
                cursor.execute(insert_user_query, (pseudo, 1))
                user_id = cursor.lastrowid
            
            # Si l'utilisateur existe déjà, on récupère son user_id
            else:
                user_id = user[0]

            # On insère le résultat dans la table results
            record_match_outcome_query = '''
                INSERT INTO results (user_id, exercise, date_hour, duration, nbtrials, nbok)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            
            # Exécute la requête
            values = (user_id, exercise, datetime.datetime.now(), duration, nbtrials, nbok)
            cursor.execute(record_match_outcome_query, values)

            # Si tout se passe bien, on affiche un message que l'enregistrement s'est bien passé
            print(Fore.GREEN + f"Game result is saved successfully for {pseudo}.")
            
    except mysql.connector.Error as error:
        # Si une erreur se produit, on affiche un message d'erreur comme quoi l'enregistrement a échoué, rien n'est enregistré dans la base de données
        print(Fore.RED + f"Failed to save game data: {error}")


# (READ) Fetch results
def fetch_game_statistics(pseudo=None, exercise=None, start_date=None, end_date=None, page=1, page_size=20):
    results = []
    total = None
    try:
        with db_connection.connect() as cursor:
            # Requête de base pour récupérer les valeurs de la table 'results' et les joindre avec la table 'users'
            load_data_query = """
                SELECT u.pseudo AS 'Élève', r.date_hour AS 'Date Heure', r.duration AS 'Temps',
                    r.exercise AS 'Exercice', r.nbok AS 'nb OK', r.nbtrials AS 'nb Total' 
                FROM results r
                INNER JOIN users u ON r.user_id = u.id
                WHERE 1 = 1
            """

            # Création des paramètres
            params = []

            # Filtres
            if pseudo:
                # on ajoute des LIKE SQL avec f"%{laValeur}%" pour pouvoir faire des recherches partielles
                load_data_query += " AND u.pseudo LIKE %s" 
                params.append(f"%{pseudo}%")
            if exercise:
                load_data_query += " AND r.exercise LIKE %s"
                params.append(f"%{exercise}%")
            if start_date:
                load_data_query += " AND r.date_hour LIKE %s"
                params.append(f"%{start_date}%")
            if end_date:
                load_data_query += " AND r.date_hour LIKE %s"
                params.append(f"%{end_date}%")

            # Pagination
            offset = (page - 1) * page_size
            load_data_query += " LIMIT %s OFFSET %s"
            params.extend([page_size, offset])

            # Exécution de la requête pour récupérer les résultats
            cursor.execute(load_data_query, tuple(params))
            results = cursor.fetchall()

            # Requête pour récupérer le nombre total d'enregistrements
            count_query = """
                SELECT COUNT(*)
                FROM results r
                INNER JOIN users u ON r.user_id = u.id
                WHERE 1 = 1
            """
            if pseudo or exercise or start_date or end_date:
                count_query += load_data_query.split("WHERE")[1].replace("LIMIT %s OFFSET %s", "")
            cursor.execute(count_query, tuple(params[:-2]))  # Exclure les paramètres de pagination
            total = cursor.fetchone()[0]
            
            print(Fore.GREEN + f"Statistiques de jeu récupérées avec succès.")

    except mysql.connector.Error as error:
        print(Fore.RED + f"Échec de la récupération des statistiques de jeu : {error}")

    return results, total



# (UPDATE) Update results
def update_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials, new_duration, new_nbok, new_nbtrials):
    try:
        with db_connection.connect() as cursor:
            # Retrieve the user_id for the given pseudo
            user_id_query = "SELECT id FROM users WHERE pseudo = %s"
            cursor.execute(user_id_query, (pseudo,))
            user_id_result = cursor.fetchone()

            if not user_id_result:
                print(Fore.YELLOW + "Aucun utilisateur trouvé avec ce pseudo.")
                return
            user_id = user_id_result[0]

            # Check if the specific game result exists
            check_query = """
            SELECT COUNT(*) 
            FROM results 
            WHERE user_id = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s
            """
            cursor.execute(check_query, (user_id, exercise, date_hour, duration, nbok, nbtrials))
            (match_count,) = cursor.fetchone()

            # If the row exists, update it
            if match_count > 0:
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
            else:
                print(Fore.YELLOW + "Aucune ligne correspondante trouvée pour mise à jour.")

    except mysql.connector.Error as error:
        print(Fore.RED + f"Échec de la mise à jour du résultat du jeu : {error}")



# (DELETE) Delete results
def remove_match_record(pseudo, exercise, date_hour, duration, nbok, nbtrials):
    try:
        with db_connection.connect() as cursor:
            # First, retrieve the user_id for the given pseudo
            user_id_query = "SELECT id FROM users WHERE pseudo = %s"
            cursor.execute(user_id_query, (pseudo,))
            user_id_result = cursor.fetchone()

            if not user_id_result:
                print(Fore.YELLOW + "Aucun utilisateur trouvé avec ce pseudo.")
                return
            user_id = user_id_result[0]

            # Now, delete the record from the results table
            delete_query = """
            DELETE FROM results 
            WHERE user_id = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s
            """
            delete_values = (user_id, exercise, date_hour, duration, nbok, nbtrials)
            cursor.execute(delete_query, delete_values)

            if cursor.rowcount == 0:
                print(Fore.YELLOW + "Aucun enregistrement correspondant trouvé pour suppression.")
            else:
                print(Fore.GREEN + f"{cursor.rowcount} ligne(s) supprimée(s)")

    except mysql.connector.Error as error:
        print(Fore.RED + f"Échec de la suppression du résultat du jeu : {error}")
        
        

# Get all exercise names
def retrieve_exercise_catalog():
    try:
        with db_connection.connect() as cursor:
            query = "SELECT DISTINCT exercise FROM results"
            cursor.execute(query)
            exercises = cursor.fetchall()

            exercise_names = [exercise[0] for exercise in exercises]
            return exercise_names
    except mysql.connector.Error as error:
        print(Fore.RED + f"Failed to get exercise names: {error}")
        return []


