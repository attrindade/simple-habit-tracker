""" 
A simple habit tracker
by: André Trevisol Trindade

to-do list: develop a better habit_line design for the csv 

current design -> |habit_name,initial_date,0,1,1,0,1,0,1| 

(after initial_date there is the checks for every day past it,'0' for no, '1' for yes I did the habit)

"""

from processes import check_habit, checking_process, creating_process, deleting_process
from readwrite import read_file, write_file
from prints import show_habits, show_stats

def start():
    #It's the initialization of our habit tracker, it
        #asks the user if he wants to register a new habit if there are no habits being tracked yet
        #asks the user if he wants to check, delete or see stats if there are already registered habits

    habits_list = read_file()
    num_habits = len(habits_list)

    print()
    # print(habits_list)

    if num_habits == 0: 
        #In the case the person doesn't have a file or a registered habit
        print("It seeems like you don't have any habits being tracked yet.")
        while True:
            choice = input("Would you like to register a new habit? (Y/N)")
            if choice == "y" or choice == "Y":
                habits_list.append(creating_process())
                break
            elif choice == "N" or choice == "n":
                print("Have a good day!")
                break
            else:
                print("Please, for 'yes' answer 'Y' and for 'no' answer 'N'")
                continue
    if num_habits > 0:
        #In the case the person have at least 1 habit registered
        print(f"You have {num_habits} habit(s) registered.")
        while True:
            print()
            print("Would you like to: ")
            print("(1) do the checking for a habit")
            print("(2) delete a habit")
            print("(3) see the habits stats")
            print("(4) create a new habit")
            print("(0) save and exit")
            choice = input("Choice (1, 2, 3, 4 or 0): ")
            if choice == '1':
                habits_list = checking_process(habits_list)
            elif choice == '2':
                habits_list = deleting_process(habits_list)
            elif choice == '3':
                show_stats(habits_list)
            elif choice == '4':
                habits_list.append(creating_process())
            elif choice == '0':
                print()
                write_file(habits_list)
                print("Have a good day!")
                break
            else:
                print("Please, answer with '1', '2', '3' or '0'")
                continue
        return

if __name__ == "__main__":
    ## TESTS
    # habits_list = ["Drink water,17022022,1,0,1,0,0,0,0,0","Run,18022022,1,0,0,1,0,1,1","Read a book,17022022,1,1,1,1,1,1,1"]
    # print(habits_list)
    # show_stats(habits_list)
    # print(check_habit(habits_list))
    # write_file(habits_list)
    # creating_process()

    start()