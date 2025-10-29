import threading
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import datetime
import json

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Global variables
task_frames = []

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        print("Couldn't request results. Check your internet connection.")
        return ""

# Function to clear existing tasks
def clear_tasks():
    for frame in task_frames:
        frame.destroy()
    task_frames.clear()

# Function to display to-do list
def display_todo_list():
    clear_tasks()
    try:
        with open("todo_list.txt", "r") as file:
            todo_list = file.readlines()
            if todo_list:
                for index, task in enumerate(todo_list, start=1):
                    task = task.strip()
                    add_task_frame(index, task)
            else:
                list_label.config(text="Your to-do list is empty!")
    except FileNotFoundError:
        list_label.config(text="To-do list file not found!")

# Function to add task to to-do list
def add_task_to_list():
    print("Listening for task...")
    command = recognize_speech()
    if command:
        task = command.replace("add task", "").strip()
        with open("todo_list.txt", "a") as file:
            file.write(task.capitalize() + "\n")
        messagebox.showinfo("Task Added", "Task added to to-do list!")
        display_todo_list()

# Function to delete task from to-do list
def delete_task(task_number):
    try:
        with open("todo_list.txt", "r") as file:
            todo_list = file.readlines()
        with open("todo_list.txt", "w") as file:
            for index, task in enumerate(todo_list, start=1):
                if index != task_number:
                    file.write(task)
        messagebox.showinfo("Task Deleted", f"Task {task_number} deleted!")
        display_todo_list()
    except FileNotFoundError:
        list_label.config(text="To-do list file not found!")

# Function to mark task as done
def mark_task_done(task_number):
    try:
        with open("todo_list.txt", "r") as file:
            todo_list = file.readlines()
        with open("todo_list.txt", "w") as file:
            for index, task in enumerate(todo_list, start=1):
                if index == task_number:
                    task = task.strip() + " - Done\n"
                file.write(task)
        messagebox.showinfo("Task Done", f"Task {task_number} marked as done!")
        display_todo_list()
    except FileNotFoundError:
        list_label.config(text="To-do list file not found!")

# Function to add a frame with task, checkbox, and delete button
def add_task_frame(task_number, task_text):
    frame = tk.Frame(root)
    frame.pack()

    task_label = tk.Label(frame, text=f"{task_number}. {task_text}")
    task_label.pack(side=tk.LEFT)

    done_button = tk.Button(frame, text="Done", command=lambda num=task_number: mark_task_done(num))
    done_button.pack(side=tk.LEFT)

    delete_button = tk.Button(frame, text="Delete", command=lambda num=task_number: delete_task(num))
    delete_button.pack(side=tk.LEFT)

    task_frames.append(frame)

# Function to listen for commands
def listen_for_commands():
        command = recognize_speech()
        if command.startswith("add task"):
            add_task_to_list()
        elif "to-do list" in command:
            display_todo_list()
        elif "clear tasks" in command:
            clear_tasks()
        elif "stop" in command:
            print("Stopping...")
            root.quit()
        elif command.startswith("delete task"):
            task_number = int(command.split()[-1])
            delete_task(task_number)
        elif command.startswith("mark task done"):
            task_number = int(command.split()[-1])
            mark_task_done(task_number)

# Function to add a deadline to a task
def add_deadline_to_task(task_number, deadline):
    try:
        with open("todo_list.txt", "r") as file:
            todo_list = file.readlines()
        with open("todo_list.txt", "w") as file:
            for index, task in enumerate(todo_list, start=1):
                if index == task_number:
                    task = task.strip() + f" - Deadline: {deadline}\n"
                file.write(task)
        messagebox.showinfo("Deadline Added", f"Deadline added to task {task_number}!")
        display_todo_list()
    except FileNotFoundError:
        list_label.config(text="To-do list file not found!")

# Tkinter root setup
root = tk.Tk()
root.title("Speech To-Do List")

list_label = tk.Label(root, text="")
list_label.pack()

# Start listening thread
listening_thread = threading.Thread(target=listen_for_commands)
listening_thread.daemon = True  # Daemonize the thread so it automatically dies when the main program exits
listening_thread.start()

# Run the Tkinter main loop
root.mainloop()
