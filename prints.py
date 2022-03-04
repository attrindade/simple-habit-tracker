from datetime import date, datetime, timedelta

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

def show_habits(habits_list: list):
    # Prints the habits_list stats
    ## RETURN: None, only prints the habits index and name, row by row
    print()
    print("These are your habits:")
    for habit_index, line in enumerate(habits_list, 1): 
        parts = line.split(';')
        print(f"({habit_index}) {parts[0]}")
    print("(0) Cancel")
    
    return