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

def write_file(habits_list: list):
    with open('my_habits.csv','w') as f:
        for count, line in enumerate(habits_list,1): 
            if count == len(habits_list):   #The intention here is to cut the \n of the last line
                f.write(f'{line}')
                break
            f.write(f'{line}\n')
        f.close()
    print("You've saved your file succesfully")
    return