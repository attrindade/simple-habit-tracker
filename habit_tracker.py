""" 
A simple habit tracker
by: André Trevisol Trindade

to-do list: develop the better habit_line design for the csv 

current design -> |habit_name;initial_date;0;1;1;0;1;0;1| 

(after initial_date there is the checks for every day past it,'0' for no, '1' for yes I did the habit)

"""

from datetime import date, datetime, timedelta

def creates_new_habit():
    #Creates a new habit
    #Creates a string (a line) that is composed of what will be inserted in 'my_habits.csv'
    ## RETURN : habit_line(str), line with data separated with semicolon
    
    today = date.today()
    habit_line = [] #This list will be filled with 0's (didn't do the habit) and 1's (did it)
                    #It will also have a tuple (habit_name,habit_date) in the [0] position

    habit_name = input("What's the name of your habit? ") #name

    while True:
        habit_date = datetime.strptime(input("When did you started it? Use the date format ddmmyyyy"),"%d%m%Y")
        habit_date = habit_date.date() #first date
        if habit_date > today:
            print("Please, insert a date that is not in the future")
            continue
        else:
            habit_line.append((habit_name,habit_date))
            break

    while habit_date <= today:
        check_date = input(f"Did you do your habit during {habit_date.strftime('%d.%m.%Y')}? (Y/N) ")
        if check_date == "y" or check_date =="Y":
            habit_line.append((1))
            habit_date += timedelta(1)
        elif check_date == "n" or check_date =="N":
            habit_line.append((0))
            habit_date += timedelta(1)
        else:
            print("Please, answer the question with 'Y' or 'N'")
            continue
    
    return habit_line

def checking_process(habits_list: list):
    #This function makes possible for the user to choose which habit he wants to do a checking
    #The index of the habit line in the list is stored to replace that line
    #After chosing, the function 'check_habit' is called 
    ## RETURN : new_habit_list (list), with the new habits list containing the cheks

    show_habits(habits_list)

    while True:
        choosen_index = int(input("Which habit would you like to check? "))
        if choosen_index in range(len(habits_list)):
            new_habit_line = check_habit(habits_list[choosen_index])
            break
        else:
            print("Please choose a valid habit's number")
            continue

    new_habits_list = []
    
    for i in range(len(habits_list)):
        if i == int(choosen_index):
            new_habits_list.append(new_habit_line)
        else:
            new_habits_list.append(habits_list[i])
    
    return new_habits_list

def check_habit(habit_line: str):
    #This function will count the amount of 0's and 1's and compare it to the initial date
    #If the amount is less than the deltatime(difference) between intial_date and today it means
    #that it is missing checks, and the function will ask for them
    ## RETURN : habit_line (str), (1) a new one if there are new checks
    ##                            (2) or the same one if there were no new checks

    habit_line = habit_line.split(';')

    h_d_year = int(habit_line[1][4:]) #Extraction of date specifics from the habit line
    h_d_month = int(habit_line[1][2:4])
    h_d_day = int(habit_line[1][0:2])

    habit_date = date(h_d_year,h_d_month,h_d_day)
    today = date.today() + timedelta(1) # Here I do a small correction so today can be counted as 1 entire
                                        # day in the difference calculus below. If the person checked already for today
                                        # and I don't do this correction, the amount of checks will be 3 (from 21 to 23, 
                                        # today) and the amount of days between 21 and 23 will be 2, not 3 as I want it 
                                        # to be, counting the day 23 as a "full day"
    checks_count = len(habit_line[2:])
    dif_today_initial = (today - habit_date).days

    if dif_today_initial == checks_count:
        print("Well done, you already checked even for today!")
    else:
        while checks_count < dif_today_initial:
            checking_date = habit_date + timedelta(checks_count) # Here I use the problem with the counting as stated
                                                                # above in my favor. As the checks count will always be
                                                                # 1 number above the difference, in this checking part
                                                                # the check setted to next day the amount of checks
                                                                # Quite complicate, but I will make easier in next versions
            check = input(f"Did you do your habit during {checking_date.strftime('%d.%m.%Y')}? (Y/N) ")
            if check == "y" or check =="Y":
                habit_line.append(('1'))
                checking_date += timedelta(1)
            elif check == "n" or check =="N":
                habit_line.append(('0'))
                checking_date += timedelta(1)
            else:
                print("Please, answer the question with 'Y' or 'N'")
                continue

            checks_count += 1

    habit_line = ';'.join(habit_line)
    return habit_line

def deleting_process(habits_list: list):
    #This function makes possible to delete habits from the list
    ## RETURN : habits_list (list), without the deleted index

    show_habits(habits_list)

    while True:
        choosen_index = int(input("Which habit would you like to delete? "))
        if choosen_index in range(len(habits_list)):
            habits_list.pop(choosen_index)
            break
        else:
            print("Please choose a valid habit's number")
            continue

    return habits_list


def show_stats(habits_list: list):
    #Shows in a tabular way name of habits, initial dates, 
    # how many 0's and 1's and how long is the actual streak
    ## RETURN : None, it only prints the habits_list data

    print()
    print(f"{'Name':<16} | {'I. Date':^10} | {'Last Check':^10} | {'did':>5} | {'didnt':>5} | {'C. Streak':>10}")
    print(f"{'-' * 71}")
    for line in habits_list:
        parts = line.split(';')
        name = parts[0]
        date = f"{parts[1][0:2]}/{parts[1][2:4]}/{parts[1][4:]}"
        #Here we create a datetime object with the initial date and add the amount of checks - 1 to the
        # timedelta. The -1 is because the initial date is also counted inside the checks
        last_check = datetime.strptime(parts[1],"%d%m%Y") + timedelta(len(parts[2:-1])) 
        last_check = last_check.strftime('%d/%m/%Y')
        num_0 = 0
        num_1 = 0
        actual_streak = 0
        for i in parts[2:]:
            if i == '0':
                num_0 += 1
                actual_streak = 0
            elif i == '1':
                num_1 += 1
                actual_streak += 1
        print(f"{name:<16} | {date:^10} | {last_check:^10} | {num_0:>5} | {num_1:>5} | {actual_streak:>10}")
    print()
    print(f"I. Date -> Initial date; Did/Didnt -> amount of days you did or didnt do")
    print(f"C. Streak -> Current Streak")
    
    return



def read_file():
    #Reads the my_habits.csv file and returns a list with each line
    ## RETURN : habits_list (list), list containing each line of the my_habits.csv
    habits_list = []

    try:
        habits_list = open('my_habits.csv','r').read().splitlines()
    except FileNotFoundError:
        print("File not found, we will consider that you don't have a file yet.")
        return habits_list

    return habits_list

def show_habits(habits_list: list):
    # Prints the habits_list stats
    ## RETURN: None, only prints the habits index and name, row by row
    print()
    print("These are your habits:")
    for habit_index, line in enumerate(habits_list):
        parts = line.split(';')
        print(f"({habit_index}) {parts[0]}")
    
    return

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
                habits_list.append(creates_new_habit())
            elif choice == "N" or choice == "n":
                print("Have a good day!")
                break
            else:
                print("Please, for 'yes' answer 'Y' and for 'no' answer 'N'")
                continue
    else:
        #In the case the person have at least 1 habit registered
        print(f"You have {num_habits} habit(s) registered.")
        while True:
            # print("~for now the habits list is~")
            # print(habits_list)
            print()
            print("Would you like to:")
            print("(1) do the checking for a habit")
            print("(2) delete a habit")
            print("(3) see the stats of a habit")
            print("(0) exit")
            choice = input("Choice (1, 2, 3 or 0): ")
            if choice == '1':
                habits_list = checking_process(habits_list)
            elif choice == '2':
                habits_list = deleting_process(habits_list)
            elif choice == '3':
                show_stats(habits_list)
            elif choice == '0':
                print("Have a good day!")
                break
            else:
                print("Please, answer with '1', '2', '3' or '0'")
                continue
        return
        #INSERT
            #option to do the checking for one habit 
            #option delete a habit
            #option to see the statistics
            #option to quit, this is the moment where the .csv is saved


if __name__ == "__main__":
    ## TESTS
    habits_list = ["Drink water;17022022;1;0;1;0;0;0;0;0","Run;18022022;1;0;0;1;0;1;1","Read a book;17022022;1;1;1;1;1;1;1"]
    # print(habits_list)
    # show_stats(habits_list)
    # print(check_habit(habits_list))

    start()