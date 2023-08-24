## ``````````````````````````````````````````````````````````````````
## AFRAS ( Automated Face Recognition Attendance System)            `
##                                                                  `
## ``````````````````````````````````````````````````````````````````


# Import the face_recognition library for face recognition tasks
# Import the cv2 (OpenCV) library for working with images and videos
# Import the tkinter library for creating graphical user interfaces (GUI)
# Import the Image and ImageTk modules from PIL to work with images and display them in the UI
# Import the threading module for managing threads in a multi-threaded environment to perform tasks concurrently, like capturing frames and UI updates
# Import the datetime module for working with date and time information
# Import the pandas library to read employee data from a CSV file
# Import the os module to navigate the file system, read directories, and handle paths
# Import the smtplib module for sending emails using the Simple Mail Transfer Protocol (SMTP)
# Import MIMEMultipart and MIMEText from email.mime.multipart and email.mime.text
# Import the firebase_admin library to connect to the Firebase Realtime Database
# Import the credentials and db modules from firebase_admin
# ------------------------------------------------------------------------------------------
import face_recognition
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import datetime
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import firebase_admin
from firebase_admin import credentials, db
# ------------------------------------------------------------------------------------------


# Initialize Firebase credentials and JSON and URL
# ------------------------------------------------------------------------------------------
cred = credentials.Certificate("/Users/susovanpatra/Desktop/PycharmProjects/AttendanceSystem/aams-ef4ed-firebase-adminsdk-j0ctz-5778e7a033.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://aams-ef4ed-default-rtdb.firebaseio.com/"
})
# Here I am loading the credentials for my Firebase project using the 
# "credentials.Certificate" function. The JSON file is providing me the information such 
# as the private key, project ID, and other authentication details that will allow me to 
# securely connect to my Firebase project.

# Then I am using the initialize_app function from the firebase_admin module to initialize 
# the  Firebase application. 
# ------------------------------------------------------------------------------------------




# I am setting up a way to keep track of recognized employees and update their first 
# recognition time. For that I am initializing a few variables.
# ------------------------------------------------------------------------------------------
capturing = False
recognized_employees = {}  # Define the dictionary globally
email_addresses = []  # Define email_addresses as a global variable

# The "capturing" variable is used to control whether it is currently capturing frames for 
# recognition. I am tarting with it set to False, meaning not capturing frames initially.

# The dictionary "recognized_employees" will store information about employees who have been 
# recognized.

# An empty list named "email_addresses" to store email addresses associated with recognized 
# employees.
# ------------------------------------------------------------------------------------------


# Loading employee data from CSV file
# ------------------------------------------------------------------------------------------
ef = pd.read_csv('Employee.csv')
empno = ef["Employee No"].tolist()
firstname = ef["First Name"].tolist()
lastname = ef["Last Name"].tolist()     
email_addresses = ef["Email"].tolist()  
n = len(empno)
emp_encod = []

# Here I am extracting Employee_No, First_Name, Last_Name, Email_Address from the csv file 
# ------------------------------------------------------------------------------------------



# Loading employee face encodings from images in the Dataset folder
# ------------------------------------------------------------------------------------------

encoding_dict = {}
dataset_path = "Dataset"

for person_folder in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_folder)
    encodings = []

    for item in os.listdir(person_path):
        item_path = os.path.join(person_path, item)
        
        if os.path.isfile(item_path) and item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image = face_recognition.load_image_file(item_path)
            encoding = face_recognition.face_encodings(image)  # All face encodings in the image
            encodings.extend(encoding)

    if encodings:  # Only add if there are valid encodings
        encoding_dict[person_folder] = encodings

# At first I am loading the unique facial features of employees from images stored in the 
# "Dataset" folder.

# "encoding_dict" will store the face encodings of employees for recognition purposes.
# Here the path structure I have used is - 
# Dataset - Person1 - person1_image1
#                     person1_image2
#                     ...
#           Person2 - person2_image1
#                     person2_image2
#                     ...

# Then iterate through the file and if it has an image extension like .png, .jpg, .jpeg, or .gif:
# Then it is being loaded using "face_recognition.load_image_file".
# Then I am extracting the facial encoding(s) from the image using "face_recognition.face_encodings".
# The "encoding" variable contains a list of facial encodings, which represent unique 
# features of faces.
# These encodings will be used later to compare with captured faces for employee recognition.
# ------------------------------------------------------------------------------------------



# Buttons in the UI
# ------------------------------------------------------------------------------------------
# Start Recognition Button Click
def start_recognition():
    global capturing
    capturing = True
    capture_thread_instance = threading.Thread(target=capture_thread)
    capture_thread_instance.start()  # Start the capture thread

# Stop Recognition Button Click
def stop_recognition():
    global capturing
    capturing = False

# Exit Button Click
def exit_app():
    global capturing
    capturing = False
    root.destroy()

    print("Attendance system stopped.")
# ------------------------------------------------------------------------------------------



# Create the UI
# ------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Real-Time Face Recognition")

video_label = tk.Label(root)
video_label.pack()

names_label = tk.Label(root, text="Recognized Employees:")
names_label.pack()

start_button = tk.Button(root, text="Start Recognition", command=start_recognition)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recognition", command=stop_recognition)
stop_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack()
# ------------------------------------------------------------------------------------------



# Reference to the 'attendance' node in the Firebase Realtime Database
# ------------------------------------------------------------------------------------------
attendance_ref = db.reference('attendance')

# My Firebase Realtime Database Tree looks like - 
# FirebaseAccount
#     - attendance
#         - date     (it need to be exact date like 2022-08-28)
#             - Person_No
# 
# So right now I am in attendance     
# ------------------------------------------------------------------------------------------



# Capture thread Function 
# ------------------------------------------------------------------------------------------

def capture_thread():
    global capturing, recognized_employees, email_addresses
    camera = cv2.VideoCapture(0)
    while capturing:
        return_value, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        uk_encode = face_recognition.face_encodings(frame_rgb)
        
        if len(uk_encode) > 0:
            recognized_names = []

            for encoding in uk_encode:
                for person_folder, known_encodings in encoding_dict.items():
                    found = False
                    for known_encoding in known_encodings:
                        if face_recognition.compare_faces([known_encoding], encoding, tolerance=0.5)[0]:
                            recognized_names.append(person_folder)
                            found = True
                            break
                    if found:
                        break
            
            # Get the current date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Update the recognized_employees and attendance records
            for person_folder in recognized_names:
                if person_folder not in recognized_employees:
                    recognized_employees[person_folder] = True
                    emp_index = empno.index(int(person_folder.replace("Person", "")))
                    email = email_addresses[emp_index]
                    recognized_full_name = f"{firstname[emp_index]} {lastname[emp_index]}"
                    print(f"Recognized: {recognized_full_name}")
                    
                    # Update attendance records in the database
                    person_id = person_folder.replace("Person", "")
                    attendance_ref_child = attendance_ref.child(f"{current_date}/Person{person_id}")
                    attendance_ref_child.push().set({"time": datetime.datetime.now().strftime("%H:%M:%S")})
            
            # Convert the frame to Tkinter format and display in the UI
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            video_label.config(image=frame_tk)
            video_label.image = frame_tk
    
    camera.release()

# The `capture_thread` function runs in a separate thread to capture frames, performs face recognition,
# and update attendance records and the UI display concurrently.

# It is using the camera to capture frames and convert them to RGB format.
# And then it identifies faces in the captured frames and compare their encodings with 
# known encodings.
# If a recognized face is detected, the it will update attendance records and the recognized 
# employees list.

# This function continuously captures frames and performs recognition while the `capturing` 
# flag is True.
# ------------------------------------------------------------------------------------------


# Starting the UI loop
# ------------------------------------------------------------------------------------------
root.mainloop()
# ------------------------------------------------------------------------------------------





# Initializing credentials for the email 
# ------------------------------------------------------------------------------------------
smtp_server = "smtp.gmail.com"                  # SMTP server address
smtp_port = 587                                 # SMTP port
sender_email = "xxxxxxxxxxxxxxx@gmail.com"      # Sender Email
sender_app_password = "xxxxxxxxxxxxxxxx"        # App password

# Here I Have used app_password as it was unable to send mail using the password directly
# An app password is a 16-digit passcode that gives less secure apps or devices permission 
# to access your Google Account. 
# ------------------------------------------------------------------------------------------



# Sending Email Notification to the Employee
# ------------------------------------------------------------------------------------------
def send_email(name, recipient_email):
    # Creating message for the employee
    subject = "Attendance Recorded"
    body = f"Hello {name},\n\nYour attendance has been recorded.\n\nBest regards,\nThe AFRAS"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    # Sending email using app password
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_app_password)  # Use app password here
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# It will send a mail to the employee saying -
#
# Hello Susovan, 
# Your attendance has been recorded.
#
# Best regards,
# The AFRAS
#
# Here the AAMS stands for Automated Face Recognition Attendance System
# ------------------------------------------------------------------------------------------
