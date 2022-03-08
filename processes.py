from datetime import date, datetime, timedelta
from prints import show_habits

def choose_habit_name():
    #Auxiliary function that asks the user for a name as input and prevent him from
    #using non printable characters and from using less than 1 char and more than 15
    ## RETURN: habit_name (str)

    while True:
        print()
        print("Max 15 and min 1 chars. Only letters, symbols, punctuation and whitespace.")
        habit_name = input("What's the name of your habit? ") #name
        if len(habit_name) > 15 or len(habit_name) < 1:
            print("Max of 15 and min of 1 characters")
            continue
        if not habit_name.isprintable():
            print("Only letters, symbols, punctuation and whitespace.")
            continue
        return habit_name

def choose_habit_date():
    # Asks the user when did the habit started and if it was not started this year the program asks if the
    # the user is sure about using that date because the checking process may take a long time
    ## RETURN : 
    today = date.today()

    while True:
        try:
            habit_date = datetime.strptime(input("When did you started it? Use the date format ddmmyyyy "),"%d%m%Y")
        except ValueError:
            print("Please, enter a valid date")
            continue
        habit_date = habit_date.date() #first date
        if habit_date > today:
            print("Please, insert a date that is not in the future")
            continue
        elif habit_date.year < today.year:
            sure = input("Are you sure about this date? The checking process may take a long time (Y/N)")
            if sure == "y" or sure == "Y":
                pass
            else:
                continue
        return habit_date

def creation_checking(habit_line, habit_date):
    #Do the first checking for this habit, from the initial date (habit_date) until today
    ## RETURN : habit_line (list), now containing the checks for this new habit
    today = date.today()

    while habit_date <= today:
        check_date = input(f"Did you do your habit during {habit_date.strftime('%d.%m.%Y')}? (Y/N) ")
        if check_date == "y" or check_date =="Y":
            habit_line.append('1')
            habit_date += timedelta(1)
        elif check_date == "n" or check_date =="N":
            habit_line.append('0')
            habit_date += timedelta(1)
        else:
            print("Please, answer the question with 'Y' or 'N'")
            continue
    
    return habit_line

def creating_process():
    #Creates a new habit
    #Creates a string (a line) that is composed of what will be inserted in 'my_habits.csv'
    ## RETURN : habit_line(str), line with data separated with semicolon
    
    habit_line = [] #This list will contain habit_name,habit_date,(and a sequence of checks, 0's and 1's)

    habit_name = choose_habit_name()
    habit_date = choose_habit_date()

    habit_line.append(habit_name)
    habit_line.append(habit_date.strftime('%d%m%Y'))

    habit_line = creation_checking(habit_line, habit_date)
    
    return ','.join(habit_line)

def checking_process(habits_list: list):
    #This function makes possible for the user to choose which habit he wants to do a checking
    #The index of the habit line in the list is stored to replace that line
    #After chosing, the function 'check_habit' is called 
    ## RETURN : new_habit_list (list), with the new habits list containing new checks

    show_habits(habits_list)

    while True:
        choosen_index = int(input("Which habit would you like to check? ")) - 1
        #Here i've adjusted the index so we can show the habits starting from 1 instead of 0
        if choosen_index in range(len(habits_list)): 
            new_habit_line = check_habit(habits_list[choosen_index])
            break
        elif choosen_index == -1:
            print("You've exited the checking process")
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

    habit_line = habit_line.split(',')

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
        print()
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

    habit_line = ','.join(habit_line)
    return habit_line

def deleting_process(habits_list: list):
    #This function makes possible to delete habits from the list
    ## RETURN : habits_list (list), without the deleted index

    show_habits(habits_list)

    while True:
        choosen_index = int(input("Which habit would you like to delete? ")) - 1
        if choosen_index in range(len(habits_list)):
            habits_list.pop(choosen_index)
            break
        elif choosen_index == -1:
            print("You've canceled the deleting process.")
            break
        else:
            print("Please choose a valid habit's number")
            continue

    return habits_list
