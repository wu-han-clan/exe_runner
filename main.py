#!/usr/bin/python3

import sqlite3
import subprocess

class App:
    def __init__(self):
        print("Hello user welcome to the app!\n")
        print("Here's what you can do with the app\n")
        text = input("Press enter to continue: ")
        if text == "":
            subprocess.run("clear")

        # If this is the best way to do this print statement its fking hideous
        # But am sure that there exists a better way

        print(
'''
OPTIONS:\n
[1] Display list of games.\n
[2] Add game.\n
[3] Delete game.\n
[4] HelpMe.\n
'''
)


    def connect_to_db(self):
        try:
            conn = sqlite3.connect('utils/test1.db')
            return conn
        except:
            print("Failed to connect to database!\n")


    def create_table(self):
        conn = self.connect_to_db()
        conn.execute('''CREATE TABLE IF NOT EXISTS GAMES
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
            TITLE       TEXT        NOT NULL,
            PATH        TEXT        NOT NULL);''')
        print("Table created successfully\n")


    def add_to_table(self, title, path):
        conn = self.connect_to_db()
        conn.execute("INSERT INTO GAMES (title, path) VALUES (?,?)",(title, path))
        conn.commit()
        print("Records saved succesfully!\n")


    def remove_from_table(self, game_id):
        if game_id not in self.get_game_ids():
            print("You can't remove an ID that doesnt exist!\n")
        else:
            conn = self.connect_to_db()
            conn.execute(f"DELETE FROM GAMES WHERE ID = ?", (game_id,))
            conn.commit()
            print(f"Successfully deleted ID = {game_id} from the database!\n")


    def see_table_contents(self):
        cursor = self.connect_to_db().execute("SELECT id, title, path from GAMES") 
        for row in cursor:
            print("\n")
            print("ID = ", row[0])
            print("TITLE = ", row[1])
            print("PATH = ", row[2])
            print("\n")


    def get_game_ids(self):
        cursor = self.connect_to_db().execute("SELECT id from GAMES")
        for ids in cursor:
            return list(ids)


    def run_game(self, num):
        cursor = self.connect_to_db().execute("SELECT id, title, path from GAMES")
        for row in cursor:
            if num == row[0]:
                print(f"Running {row[1]}\n")
                subprocess.run(f"wine {row[2]}", shell=True)
    
    
def main():
    app = App()
    app.connect_to_db()

    # try block cause infinite loops (can't even be broken with ctrl+c, had to kill the terminal)
    # this counter variable was introduced as a hotfix
    counter = 3 

    running = True

    while running: 

        try:
            u_input = int(input("Enter the number you want: "))
        except:
            counter -= 1
            print("You need to enter a number!\n")
            if counter == 0:
                running = False 
            continue
        if u_input == 1:
            app.see_table_contents()
            try:
                u_input = int(input("Enter the number of a game you'd like to play: "))
            except:
                counter -= 1
                print("You didn't enter a number!\n")
                if counter == 0:
                    running = False

            if u_input not in app.get_game_ids():
                print("You entered a number that doesn't do shit")
            app.run_game(u_input)            
            

        elif u_input == 2:
            print("So you would like to add a game\n")
            app.add_to_table(input("Enter the game title: "), input("Enter the path to executable: "))
            subprocess.run("clear")


        elif u_input == 3:
            print("So u'd like to delete stuff a\n")
            u_input = input("(yes/no): ")

            if u_input == 'yes' or u_input == 'y':
                app.remove_from_table(input("Enter the games ID: "))


        elif u_input == 4:
            subprocess.run("clear")
            print(
'''If you somehow managed to fuck up the database\n
this will help you get back on track.\n''')

            print(
'''Would you like to create the database table?\n 
(it will not override existing table if it exists!\n''')

            u_input = input("(yes/no): ")
            if u_input == 'yes' or u_input == 'y':
                app.create_table()




if __name__ == '__main__':
    main()
