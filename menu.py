from simple_term_menu import TerminalMenu
import time
import sys
import calendar
import datetime
import os
from getch import getch

def display_calendar():

   current_date = datetime.datetime.now()
   year = current_date.year
   month = current_date.month
   selected_day = current_date.day
   confirmed_day = None


   while True:
       os.system("cls" if os.name == "nt" else "clear")
       cal = calendar.monthcalendar(year, month)
       month_name = calendar.month_name[month]
       print(f"\n{'—' * 30}")
       print(f"{month_name} {year}".center(30))
       print(f"{'—' * 30}")
       print("Mo Tu We Th Fr Sa Su")

       for week in cal:
           for i, day in enumerate(week):
               if day == 0:
                   print("  ", end=" ")

               elif (
                   confirmed_day
                   and day == confirmed_day
                   and year == current_date.year
                   and month == current_date.month
               ):
                   print(f"\033[1;32m{day:2}\033[0m", end=" ")

               elif day == selected_day:
                   print(f"\033[1;31m{day:2}\033[0m", end=" ")
               else:
                   print(f"{day:2}", end=" ")
           print()

       print(f"{'—' * 30}")
       print("Arrows to navigate, p to select, q to quit")

       key = getch()

       if key == "\x1b":
           getch()
           direction = getch()
           if direction == "A":  # Up: previous month
               month -= 1
               if month < 1:
                   month = 12
                   year -= 1

               max_day = calendar.monthrange(year, month)[1]

               if selected_day > max_day:
                   selected_day = max_day

           elif direction == "B":  # Down: next month
               month += 1
               if month > 12:
                   month = 1
                   year += 1

               max_day = calendar.monthrange(year, month)[1]

               if selected_day > max_day:
                   selected_day = max_day

           elif direction == "C":
               selected_day += 1
               max_day = calendar.monthrange(year, month)[1]
               if selected_day > max_day:
                   selected_day = 1
                   month += 1
                   if month > 12:
                       month = 1
                       year += 1

           elif direction == "D":
               selected_day -= 1
               if selected_day < 1:
                   month -= 1
                   if month < 1:
                       month = 12
                       year -= 1

                   selected_day = calendar.monthrange(year, month)[1]

       elif key == "p":
           confirmed_day = selected_day
           os.system("cls" if os.name == "nt" else "clear")
           return selected_day, month, year

       elif key.lower() == "q":
           return None, None, None

class Menu:
   def __init__(self):
       pass

   def main_menu(self):
       print("\033[32mThis is attendance app project. Choose from Menu:\033[0m")
       time.sleep(1.5)
       os.system('cls' if os.name == 'nt' else 'clear')

       options = ["Add new Student", "Mark Attendance", "Change Attendace","Print single student's attendance",
                  "Print class's attendance ",
                  "Exit"]

       int_option = self.option_menu(options)

       if int_option == 5:
           print("Thank for using our App :)")
           sys.exit(0)

       return int_option


   def option_menu(self, options_list):
       options_menu = TerminalMenu(options_list, multi_select=False)
       choice_show = options_menu.show()
       return choice_show


   def add_new_students(self):
       print("Enter new student name: ")
       name = input()
       try:
           with open("students.txt", "a") as file:
               file.write(name + "\n")
           return 1
       except FileNotFoundError:
           print("Add students first")
           time.sleep(1)
           os.system('cls' if os.name == 'nt' else 'clear')
           return None

   def day_choose_fun(self):
       date = display_calendar()
       return date

   def student_choose_fun(self, students_list):
       # add option to parse from pickle file
       student_choos_menu = TerminalMenu(students_list, multi_select=False)
       student_choice_show = student_choos_menu.show()
       # print(student_choice_show.chosen_menu_entries)
       return student_choice_show

   def attendance_input_fun(self):
       attendance_options = ["Present", "Absent", "Tardy"]
       console_attendance_menu = TerminalMenu(attendance_options, multi_select=False)
       attendance_options_show = console_attendance_menu.show()
       # print(attendance_options_show)

       # print(attendance_options_show.chosen_menu_entries)

       return attendance_options_show