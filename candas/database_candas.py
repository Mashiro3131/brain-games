import mysql.connector

def get_db_connection():
    # Établir une connexion au serveur MySQL
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='root'
    )

    cursor = conn.cursor()

    # Créer une base de données
    cursor.execute("CREATE DATABASE IF NOT EXISTS MADBPY")

    # Utiliser cette base de données
    cursor.execute("USE MADBPY")

    # Créer une table

    cursor.execute('''
    CREATE TABLE if not exists partie (
        id INT PRIMARY KEY AUTO_INCREMENT, 
        Exercise VARCHAR(255) NOT NULL,
        Pseudo VARCHAR(255) NOT NULL,
        DateHour DATETIME NOT NULL,
        Duration TIME NOT NULL,
        NbTrials INT NOT NULL,
        NbOk INT NOT NULL
    )
    ''')
    
    return conn, cursor

def save_game_result(pseudo, exercise, duration, nb_trials, nb_success):
    # connection db
    conn, cursor = get_db_connection()

    # pour insertion les donnees
    query = '''
    INSERT INTO partie (Exercise, Pseudo, DateHour, Duration, NbTrials,NbOk)
    VALUES (%s, %s, NOW(), %s, %s, %s)
    '''
    values = (exercise, pseudo, duration, nb_trials,nb_success)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def get_game_results(pseudo=None, exercise=None, start_date=None, end_date=None):
    conn, cursor = get_db_connection()

    # pour obtenir les valeurs de table 'partie'
    query = "SELECT Pseudo AS 'Élève', DateHour AS 'Date Heure', Duration AS 'Temps', Exercise AS 'Exercice', NbOk AS 'nb OK' , NbTrials AS 'nb Total' FROM partie WHERE 1=1"

    # pour cree les parametres
    params = []

    # les filtres, Lorsque l'un de ces paramètres est indiqué, la requête est filtrée en fonction de ces paramètres.
    # par ex: resultats = database.get_game_results(pseudo=pseudo)
    if pseudo:
        query += " AND Pseudo = %s"
        params.append(pseudo)
    if exercise:
        query += " AND Exercise = %s"
        params.append(exercise)
    if start_date:
        query += " AND DateHour >= %s"
        params.append(start_date)
    if end_date:
        query += " AND DateHour <= %s"
        params.append(end_date)

    # execute le requete
    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def delete_game_result(Pseudo,Exercise,DateHour,Duration,NbOk,NbTrials):
    conn, cursor = get_db_connection()

    # script pour delete
    query = "DELETE FROM partie WHERE Pseudo = %s AND Exercise = %s AND DateHour = %s AND Duration = %s AND NbOk = %s AND NbTrials = %s"
    try:
        cursor.execute(query, (Pseudo, Exercise, DateHour, Duration,NbOk,NbTrials))
        conn.commit()
        print(f"{cursor.rowcount} ligne est supprimé")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()


def update_game_result(Pseudo, Exercise, DateHour, Duration, NbOk, NbTrials, new_duration, new_nb_ok, new_nb_trials):
    conn, cursor = get_db_connection()

    # d'abord on va verifier, cette ligne est existe ou pas dans bd
    check_query = "SELECT COUNT(*) FROM partie WHERE Pseudo = %s AND Exercise = %s AND DateHour = %s AND Duration = %s AND NbOk = %s AND NbTrials = %s"
    cursor.execute(check_query, (Pseudo, Exercise, DateHour, Duration, NbOk, NbTrials))
    (match_count,) = cursor.fetchone()

    # si il y a une ligne on va modifier
    if match_count > 0:
        update_query = "UPDATE partie SET Duration = %s, NbOk = %s, NbTrials = %s WHERE Pseudo = %s AND Exercise = %s AND DateHour = %s"
        update_values = (new_duration, new_nb_ok, new_nb_trials, Pseudo, Exercise, DateHour)

        try:
            cursor.execute(update_query, update_values)
            conn.commit()
            print(f"{cursor.rowcount} ligne est mise à jour")
        except mysql.connector.Error as err:
            print("Error:", err)
    else:
        print("Aucune ligne correspondante trouvée pour mise à jour.")

    cursor.close()
    conn.close()



def get_all_exercise_names():
    conn, cursor = get_db_connection()

    query = "SELECT DISTINCT Exercise FROM partie"
    cursor.execute(query)
    exercises = cursor.fetchall()

    exercise_names = [exercise[0] for exercise in exercises]
    return exercise_names

    cursor.close()
    conn.close()


