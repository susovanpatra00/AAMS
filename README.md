# AFRAS
# Automated Face Recognition Attendance System

This is a face recognition based attendance system that can automatically mark attendance by recognizing faces from a camera feed.

# Overview
Uses OpenCV and face_recognition library to detect and recognize faces
Captures frames from webcam feed and compares face encodings with known encodings from image dataset
Maintains a dictionary of recognized employees and updates attendance records in Firebase Realtime Database
Sends email notifications to employees when their attendance is marked
User interface built with Tkinter for starting, stopping and exiting the system

# Requirements
Python 3.x
OpenCV
face_recognition
Tkinter
PIL
pandas
firebase_admin
Credentials JSON for Firebase project
