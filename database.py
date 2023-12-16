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



import mysql.connector
import colorama
import datetime
from colorama import Fore, Style

colorama.init(autoreset=True)

def open_db():
    return mysql.connector.connect(
        
        host='127.0.0.1',
        port='3306',
        user='root',
        password='root',
        database='brain_games_db',
        buffered=True,
        autocommit=True 
           
    )



db_conn = open_db()



def insert_game_result(pseudo, exercise, duration, nbtrials, nbok):
    try:
        cursor = db_conn.cursor()

        # Check if user exists
        user_check_query = "SELECT id FROM users WHERE pseudo = %s"
        cursor.execute(user_check_query, (pseudo,))
        user = cursor.fetchone()

        if user is None:
            # User doesn't exist, so create a new user
            insert_user_query = "INSERT INTO users (pseudo, role_id) VALUES (%s, %s)"
            cursor.execute(insert_user_query, (pseudo, 1))  # role_id = 1 for student and 2 for teacher
            db_conn.commit()

            # Get the ID of the newly created user
            user_id = cursor.lastrowid
        else:
            # User exists, get the user_id
            user_id = user[0]

        # Insert the game result into the results table
        insert_result_query = '''
        INSERT INTO results (user_id, exercise, date_hour, duration, nbtrials, nbok)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (user_id, exercise, datetime.datetime.now(), nbtrials, nbtrials, nbok)

        cursor.execute(insert_result_query, values)
        db_conn.commit()

    except mysql.connector.Error as error:
        print(Fore.RED + f"Failed to save game data: {error}" + Style.RESET_ALL)
        
    finally:
        cursor.close()


def load_results(pseudo=None, exercise=None, start_date=None, end_date=None):
    try:
        cursor = db_conn.cursor()

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

    finally:
        cursor.close()
        return results


def delete_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials):
    cursor = db_conn.cursor()

    # script for delete
    query = "DELETE FROM results WHERE pseudo = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s"
    try:
        cursor.execute(query, (pseudo, exercise, date_hour, duration, nbok, nbtrials))
        db_conn.commit()
        print(f"{cursor.rowcount} row is deleted")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()


def update_game_result(pseudo, exercise, date_hour, duration, nbok, nbtrials, new_duration, new_nb_ok, new_nb_trials):
    cursor = db_conn.cursor()

    # first we will check if this row exists in the database
    check_query = "SELECT COUNT(*) FROM results WHERE pseudo = %s AND exercise = %s AND date_hour = %s AND duration = %s AND nbok = %s AND nbtrials = %s"
    cursor.execute(check_query, (pseudo, exercise, date_hour, duration, nbok, nbtrials))
    (match_count,) = cursor.fetchone()

    # if there is a row, we will update it
    if match_count > 0:
        update_query = "UPDATE results SET duration = %s, nbok = %s, nbtrials = %s WHERE pseudo = %s AND exercise = %s AND date_hour = %s"
        update_values = (new_duration, new_nb_ok, new_nb_trials, pseudo, exercise, date_hour)

        try:
            cursor.execute(update_query, update_values)
            db_conn.commit()
            print(f"{cursor.rowcount} row is updated")
        except mysql.connector.Error as err:
            print("Error:", err)
    else:
        print("No matching row found for update.")

    cursor.close()


def get_all_exercise_names():
    cursor = db_conn.cursor()

    query = "SELECT DISTINCT exercise FROM results"
    cursor.execute(query)
    exercises = cursor.fetchall()

    exercise_names = [exercise[0] for exercise in exercises]
    return exercise_names


