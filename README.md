# AFRAS (Automated Face Recognition Attendance System)

This is a face recognition based attendance system that can automatically mark attendance by recognizing faces from a camera feed.

## Overview
Uses OpenCV and face_recognition library to detect and recognize faces
Captures frames from webcam feed and compares face encodings with known encodings from image dataset
Maintains a dictionary of recognized employees and updates attendance records in Firebase Realtime Database
Sends email notifications to employees when their attendance is marked
User interface built with Tkinter for starting, stopping and exiting the system

## Requirements
* Python 3.x
* OpenCV
* face_recognition
* Tkinter
* PIL
* pandas
* firebase_admin
* Credentials JSON for Firebase project


## Usage
1. Clone the repository
git clone https://github.com/<username>/face-recognition-attendance

2.  Install requirements
pip install -r requirements.txt

3.  Add employee images in Dataset folder named as PersonID (e.g. Person1, Person2 etc.)
  
4.  Update Employee.csv with employee details (Employee No, Name, Email etc.)

5. Add your Firebase project credentials JSON file
6. Run main.py
7. Click Start Recognition button to initiate face recognition
8. Attendance will be marked automatically in Firebase database
9. Email notifications will be sent to recognized employees


## Customization
* The Capture Thread function contains the core face recognition logic and can be customized as per needs
* User interface can be modified by changing Tkinter components
* Email content and formatting can be customized
* Additional modules like SMS notifications can be added easily but I have used email as it is more professional

## Resources
* OpenCV
* face_recognition
* Firebase Realtime Database
* Tkinter
* email.mime

## File Guide 
* main.py - This is the main function we need to run
* Employee.csv - It contains the details of Employees (Employee_No, First_Name, Last_Name, Email)
* Dataset - Images of the employees according to their Employee_No as folder name (for Employee_No = 1 it is Person1)
