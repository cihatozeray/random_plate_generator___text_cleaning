# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 00:16:57 2020
Modified on Wed Jan 27 23:25 2021

@author: Cihat Özeray
"""

import string
import random
import time
import sys


def read_files():
    """
    Reads from existing .txt files and collects them into a dictionary
    There are 81 files all in the same file wih the module
    """

    files_all = {}

    for i in range(1, 82):
        file_name = str(i) + ".txt"
        handle = open(file_name, "r", encoding="utf8")
        temp = handle.read()
        handle.close()
        files_all[i] = temp

    return files_all


def data_cleansing(files_all):
    """
    takes input as a dictionary of text files
    output as a dictionary representing provinces where province code
    is the key and has list of tuples for licence plate constraints
    """

    #There was some special cases where data had to be cleansed,
    #but the source stays untouched!
    cleansed_files = {}
    for i in files_all.keys():
        temp = files_all[i]
        temp = temp.split()

        if i == 7: # for Antalya (Private Plates)
            del temp[:29]

        if i == 26:# for Eskisehir (Numbers in tax administration were causing problems...
            temp = ["İKİ" if i == str(2) else i for i in temp] #.. for a later algorithm)

        if i == 45: # for Manisa (Private Plates)
            del temp[:11]

        if i == 55: # for Samsun (One of the letters was also missing and added here)
            del temp[:138]  # Also the numbers are removed again from the tax admn
            temp = ["ON DOKUZ" if i == str(19) else i for i in temp]
            index = temp.index("7250")
            temp.insert(index, "T")

        if i == 73: # for Sırnak (Had a lot of letters missing)
            j = -1   # But the letters are added in the safest way possible
            while j >= -len(temp):
                if temp[j].isnumeric() and temp[j-1].isnumeric():
                    temp.insert(j, temp[j-2])
                j -= 1

        del temp[:14] # Removing headers from all lists

        #Removing tax administration places since they were causing a lot of inconsistency:
        k = 6
        while k < len(temp):
            while not temp[k].isnumeric():
                del temp[k]
            k += 7
        # Creating the plate boundary tuples:
        temp = [[temp[i+2], temp[i+3], temp[i+4], temp[i+5]] for i in \
                range(0, len(temp)-6, 7)]

        if i == 20: # for Denizli (Private Plates)
            del temp[25:]#(It was easier to fix these ones after creating the tuples)

        if i == 28: # for Giresun (Private Plates)
            del temp[-1:]

        if i == 59: # for Tekirdag (Private Plates)
            del temp[-2]

        if i == 8: # for Artvin
            temp[44][3] = temp[44][2]
            temp[44][2] = temp[44][0]

        #private plates are removed (maximum length of chars will be 3)
        temp = [j for j in temp if len(j[0]) <= 3 and len(j[2]) <= 3]

        cleansed_files[i] = temp # Adding regional plates to the dict - list of tuples

    return cleansed_files



def generate_string_range():
    """
    Generates a string list to represent a range
    returns: List of strings
    """

    # from "A" to "ZZZ",  an ordered list is created for representing a string range
    # illegal letters are removed
    not_allowed = ["X", "W", "Q"]
    upper = [i for i in list(string.ascii_uppercase) if i not in not_allowed]
    string_list = upper.copy()

    for i in upper:
        for j in upper:
            temp = i + j
            string_list.append(temp)
    for i in upper:
        for j in upper + ["I", "O"]:
            for k in upper:
                temp = i + j + k
                string_list.append(temp)

    return string_list


def generate_random_plate(cleansed_files, string_list):
    """
    generates a random plate within designated regulations
    returns: String
    """

    province = random.randint(1, 81)
    district = random.randint(0, len(cleansed_files[province])-1)
    constraint = cleansed_files[province][district]

    lower_boundary = string_list.index(constraint[0])
    upper_boundary = string_list.index(constraint[2])
    plate_middle = string_list[random.randint(lower_boundary, upper_boundary)]

    plate_end_int = random.randint(int(constraint[1]), int(constraint[3]))

    province, plate_end = str(province), str(plate_end_int)
    province = "0" + province if len(province) == 1 else province

    plate = province + " " + plate_middle + " " + plate_end

    return plate


def test_letters(cleansed_files, string_list):
    """
    Prints all of the strings available
    It is useful to test if data is missing or misread
    """

    for i in cleansed_files.keys():
        for j in cleansed_files[i]:
            for k in string_list[string_list.index(j[0]) : string_list.index(j[2]) + 1]:
                plate = str(i) + " " + k + " "
                print(plate)


def test_numbers(cleansed_files):
    """
    Prints start and end points of the number range
    It is useful to test if data is missing or misread
    """

    for i in cleansed_files.keys():
        for j in cleansed_files[i]:
            if not j[1].isnumeric() or not j[3].isnumeric():
                print("ERROR")
            plate = str(i)  + " " + str(j[1]) + " " + str(j[3])
            print(plate)


def main():
    """
    main function:
        Calls necessary functions to print a random plate
        has tests for data acquisition and cleansing
        has a test for time it takes to execute
    """

    enter = ""
    while enter == "":

        t_0 = time.time()

        global FILES_ALL
        global CLEANSED_FILES
        global STRING_LIST

        if "FILES_ALL" not in globals():
            FILES_ALL = read_files()

        if "CLEANSED_FILES" not in globals():
            CLEANSED_FILES = data_cleansing(FILES_ALL)

        if "STRING_LIST" not in globals():
            STRING_LIST = generate_string_range()

        if "test_letters" in sys.argv:
            test_letters(CLEANSED_FILES, STRING_LIST)

        if "test_numbers" in sys.argv:
            test_numbers(CLEANSED_FILES)

        if "test_time" in sys.argv:
            t_1 = time.time()
            time_diff = str(t_1 - t_0)
            print("\n" + time_diff)

        plate = generate_random_plate(CLEANSED_FILES, STRING_LIST)
        print("\n" + plate)

        enter = input("\nPress 'Enter' for a new plate or a random letter to exit:  ")


if __name__ == "__main__":
    main()
