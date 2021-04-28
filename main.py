#!/usr/bin/python3

import sqlite3
import subprocess
import re

class App:
    def __init__(self):
        self.create_table()
        print("Hello user welcome to the app!\n")
        print("Here's what you can do with the app\n")
        text = input("Press enter to continue: ")
        if text == "":
            subprocess.run("clear")

        print(
'''
OPTIONS:\n
[1] Display list of games.\n
[2] Add game.\n
[3] Delete game.\n
[4] Run game.\n
[0] QUIT!\n
'''
)


    def connect_to_db(self):
        try:
            conn = sqlite3.connect('utils/test.db')
            return conn
        except:
            print("Failed to connect to database!\n")


    def create_table(self):
        conn = self.connect_to_db()
        conn.execute('''CREATE TABLE IF NOT EXISTS GAMES
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
            TITLE       TEXT        NOT NULL,
            PATH        TEXT        NOT NULL);''')


    def add_to_table(self, title, path):
        conn = self.connect_to_db()
        conn.execute("INSERT INTO GAMES (title, path) VALUES (?,?)",(title, path))
        conn.commit()
        print("Records saved succesfully!\n")


    def remove_from_table(self, game_id):
        if int(game_id) not in self.get_game_ids():
            print("You can't remove an ID that doesnt exist!\n")
        else:
            conn = self.connect_to_db()
            conn.execute("DELETE FROM GAMES WHERE ID = ?", (game_id,))
            conn.commit()
            print(f"Successfully deleted ID = {game_id} from the database!\n")


    def see_table_contents(self):
        cursor = self.connect_to_db().execute("SELECT id, title, path from GAMES") 
        for game_id, title, path in cursor:
            print("\n")
            print("ID = ", game_id)
            print("TITLE = ", title)
            print("PATH = ", path)
            print("\n")


    def get_game_ids(self):
        ids_list = []
        cursor = self.connect_to_db().execute("SELECT id from GAMES")
        for ids in cursor:
            ids_list.append(ids)
        temp = re.sub(r'[\[\]\(\), ]', '', str(ids_list))
        res = [int(i) for i in set(temp)]
        return res 


    def run_game(self, num):
        if num not in self.get_game_ids():
            print("There's no game with that ID\n")
        else:
            cursor = self.connect_to_db().execute("SELECT id, title, path from GAMES")
            for game_id, title, path in cursor:
                if num == game_id:
                    print(f"Running {title}\n")
                    subprocess.run(f"wine {path}", shell=True)
    

def main():
    app = App()
    app.connect_to_db()


    while True:
        try:
            u_input = int(input("Enter a number you want: "))
        except ValueError:
            print("You didn't enter a number!\n")
            continue
        
        if u_input == 1:
            app.see_table_contents()

        elif u_input == 2:
            app.add_to_table(input("Enter game title: "), input("Enter path to exe: "))

        elif u_input == 3:
                app.remove_from_table(int(input("Enter the game ID that you'd like to remove: ")))

        elif u_input == 4:
            try:
                app.see_table_contents()
                app.run_game(int(input("Enter the game number: ")))
            except:
                print("You didn't enter a number!\n")

        elif u_input == 0:
            break



if __name__ == '__main__':
    main()
