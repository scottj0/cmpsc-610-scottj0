#!/usr/bin/python

#Author: John Scott
#GitHub: @scottj0
#This work is mine unless otherwise cited.

#This file is the menu for the project.

print ("Welcome to the Spotipy Playlist Generator!")

print("You may choose to create a recently added playlist, or edit an existing one!")

while True:
    print ("What would you like to create?")

    choice = input("Enter your choice: ")

    if choice == "recent":
        exec(open("./recent.py").read()) #executes "recent.py" script

    elif choice == "edit":
        exec(open("./edit.py").read()) #executes "edit.py"

    elif choice == "exit":
        print ("Goodbye!")
        break

    else:
        print ("Not an option.")
