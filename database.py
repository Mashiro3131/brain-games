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



# Insert results
# Insert results
def record_match_outcome(pseudo, exercise, duration, nbtrials, nbok):
    try:
        with db_connection.connect() as cursor:
            # Check if user exists
            user_check_query = "SELECT id FROM users WHERE pseudo = %s"
            cursor.execute(user_check_query, (pseudo,))
            user = cursor.fetchone()

            if user is None:
                # User doesn't exist, so create a new user
                insert_user_query = "INSERT INTO users (pseudo, role_id) VALUES (%s, %s)"
                cursor.execute(insert_user_query, (pseudo, 1))
                user_id = cursor.lastrowid
            else:
                # User exists, get the user_id
                user_id = user[0]

            # Insert the game result into the results table
            insert_result_query = '''
            INSERT INTO results (user_id, exercise, date_hour, duration, nbtrials, nbok)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            values = (user_id, exercise, datetime.datetime.now(), duration, nbtrials, nbok)
            cursor.execute(insert_result_query, values)

    except mysql.connector.Error as error:
        print(Fore.RED + f"Failed to save game data: {error}")


def fetch_game_statistics(pseudo=None, exercise=None, start_date=None, end_date=None):
    try:
        with db_connection.connect() as cursor:
            # to retrieve values from the 'results' table
            load_data_query = "SELECT pseudo AS 'Élève', date_hour AS 'Date Heure', duration AS 'Temps', exercise AS 'Exercice', nbok AS 'nb OK' , nbtrials AS 'nb Total' FROM results WHERE 1=1"

            # create parameters
            params = []

            # filters, when any of these parameters are specified, the query is filtered based on these parameters.
            # e.g. results = load_results(pseudo=pseudo)
            if pseudo:
                load_data_query += " AND pseudo = %s"
                params.append(pseudo)
            if exercise:
                load_data_query += " AND exercise = %s"
                params.append(exercise)
            if start_date:
                load_data_query += " AND date_hour >= %s"
                params.append(start_date)
            if end_date:
                load_data_query += " AND date_hour <= %s"
                params.append(end_date)

            # execute the query
            cursor.execute(load_data_query, params)
            results = cursor.fetchall()

    except mysql.connector.Error as error:
        print(Fore.RED + f"Failed to fetch game statistics: {error}")

    return results


def delete_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials):
    try:
        with db_connection.connect() as cursor:
            # script for delete
            query = "DELETE FROM results WHERE pseudo = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s"
            cursor.execute(query, (pseudo, exercise, date_hour, duration, nbok, nbtrials))
            db_connection.commit()
            print(f"{cursor.rowcount} row is deleted")
    except mysql.connector.Error as err:
        print("Error:", err)


def update_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials, new_duration, new_nb_ok, new_nb_trials):
    try:
        with db_connection.connect() as cursor:
            # first we will check if this row exists in the database
            check_query = "SELECT COUNT(*) FROM results WHERE pseudo = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s"
            cursor.execute(check_query, (pseudo, exercise, date_hour, duration, nbok, nbtrials))
            (match_count,) = cursor.fetchone()

            # if there is a row, we will update it
            if match_count > 0:
                update_query = "UPDATE results SET duration = %s, nbok = %s, nbtrials = %s WHERE pseudo = %s AND exercise = %s AND date_hour = %s"
                update_values = (new_duration, new_nb_ok, new_nb_trials, pseudo, exercise, date_hour)

                cursor.execute(update_query, update_values)
                db_connection.commit()
                print(f"{cursor.rowcount} row is updated")
            else:
                print("No matching row found for update.")

    except mysql.connector.Error as error:
        print(Fore.RED + f"Failed to update game result: {error}")



def get_all_exercise_names():
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


