import os
import pickle
import time
from menu import Menu
from datetime import datetime

def append_to_line(file_path, line_num, text_to_append):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return

    if 1 <= line_num <= len(lines):
        lines[line_num - 1] = lines[line_num - 1].rstrip('\n') + text_to_append + '\n'
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print(f"Error: Invalid line number: {line_num}. File has {len(lines)} lines.")

def student_list_function(Self_obj):
    student_list = []
    try:
        with open("students.txt", "r") as file:
            for student in file:
                student_list.append(student.strip())
    except FileNotFoundError:
        pass
    return student_list

def main():
    menu = Menu()
    student_list = student_list_function(menu)
    attance_list = []

    try:
        with open('attendance.pkl', 'rb') as file:
            attance_list = pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        attance_list = []

    while True:
        main_menu = menu.main_menu()

        if main_menu == 0:
            z = menu.add_new_students()
            if z == None:
                continue
        elif main_menu == 1:
            while True:
                student_list = student_list_function(menu)
                student_num = menu.student_choose_fun(student_list)
                day = menu.day_choose_fun()
                attendace = menu.attendance_input_fun()

                int_return = student_num, attendace, day
                attance_list.append(int_return)
                append_to_line("students.txt", int(student_num) + 1, " ")

                with open('attendance.pkl', 'wb') as file:
                    pickle.dump(attance_list, file)

                continue_ = input("Do you want to continue? [y/n] ")
                if "y" in continue_.lower():
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                else:
                    break

        elif main_menu == 3:
            try:
                with open('attendance.pkl', 'rb') as file:
                    attance_list = pickle.load(file)
            except (FileNotFoundError, EOFError, pickle.PickleError):
                print("Error: No attendance data found")
                attance_list = []

            student_list = []
            try:
                with open("students.txt", "r") as file:
                    for student in file:
                        student_list.append(student.strip())
            except FileNotFoundError:
                print("Error: File not found")

            student_list = student_list_function(menu)
            student_num = menu.student_choose_fun(student_list)
            found = False
            attendance_options = ["Present", "Absent", "Tardy"]

            for i in range(len(attance_list)):
                for z in attance_list:
                    student_name = ""
                    attendance_options = ["Present", "Absent", "Tardy"]
                    for char in student_list[(attance_list[i][0])]:
                        if char == "(":
                            break
                        else:
                            student_name += char

                x, y, z = attance_list[i][2]
                date = datetime(z, y, x)
                full_weekday = date.strftime("%A")
                day_of_the_weark_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                if attance_list[i][0] == student_num:
                    print(f"{'—' * 15} {student_name} {'—' * 15}")
                    for z in day_of_the_weark_list:
                        if full_weekday == z:
                            print(f"{z}  - \033[32m{attendance_options[(attance_list[i][1])]}\033[0m")
                        else:
                            print(f"{z} - Absent")
                    found = True

            if not found:
                print(f"No present days found for student {student_num}")
            time.sleep(8)
            os.system('cls' if os.name == 'nt' else 'clear')

        elif main_menu == 2:
            try:
                with open('attendance.pkl', 'rb') as file:
                    attance_list = pickle.load(file)
            except (FileNotFoundError, EOFError, pickle.PickleError):
                print("Error: No attendance data found")
                attance_list = []

            student_num = menu.student_choose_fun(student_list)
            student_list = student_list_function(menu)
            new_attendance = menu.attendance_input_fun()
            day = menu.day_choose_fun()

            updated = False
            for i in range(len(attance_list)):
                if attance_list[i][0] == student_num and attance_list[i][2] == day:
                    attance_list[i] = (student_num, new_attendance, day)
                    updated = True
                    break

            if updated:
                with open('attendance.pkl', 'wb') as file:
                    pickle.dump(attance_list, file)
                print(f"Attendance updated for student {student_num} on {day}")
            else:
                print(f"No attendance record found for student {student_num} on {day}")

        elif main_menu == 4:
            try:
                with open('attendance.pkl', 'rb') as file:
                    attance_list = pickle.load(file)
            except (FileNotFoundError, EOFError, pickle.PickleError):
                print("Error: No attendance data found")
                attance_list = []

            day_attendance = {day: {} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
            attendance_options = ["Present", "Absent", "Tardy"]

            for i in attance_list:
                student_name = ""
                for char in student_list[i[0]]:
                    if char == "(":
                        break
                    else:
                        student_name += char
                x, y, z = i[2]
                try:
                    date = datetime(z, y, x)
                    full_weekday = date.strftime("%A")
                    if full_weekday in day_attendance:
                        day_attendance[full_weekday][student_name] = attendance_options[i[1]]
                except:
                    print(f"Invalid date format {i}")
                    continue

            print(f"\n{'—' * 15} Class Attendance for the week {'—' * 15}")
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                students = day_attendance[day]
                if students:
                    print(f"{day} - ", end="")
                    first = True
                    for student, status in students.items():
                        if not first:
                            print(", ", end="")
                        print(f"{student} {status}", end="")
                        first = False
                    print()
                else:
                    print(f"{day} - Nobody")

            time.sleep(7)
            os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    main()