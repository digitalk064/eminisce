# Eminisce Web Application for Library Management
### Part of Eminisce Group's CSIT321 Final Year Project<br>Topic: Biometric Authentication<br>Made with Django and Django Rest Framework. <br>Languages: Python, HTML, JavaScript
This is the web application part of our group's final year project: a library management suite that supports borrowing books using biometric authentication, particularly fingerprint scanning and facial recognition. Also included is the API (using Django Rest Framework) for the Android application to access. 

The web application is designed for three user groups: _library users_, _librarians_, and _administrators_.

**Library users** can login to their accounts and view what books they're borrowing, deadlines for returning books, reserved books, their outstanding fines (to pay them), etc. Additionally, they can view their history of borrowed and returned books, plus view their history of fines. They can also browse the library's catalog (with filtering options) and choose to reserve a book that is unavailable at the time.

**Librarians** can login to their accounts and manage many aspects of the library such as the catalog, book loans, fines, etc. They can review the catalog and add, remove, or edit books at will. They can review all current and past loans and manually edit the due date or mark them as returned. Librarians also manage library users' accounts: They can create, edit, remove a library user's account. They can upload, edit or remove the biometric data (fingerprint and face) of a user. ( They can add, edit,, or remove fees charged to a library user's account.

**Administrators** has superuser access to Django's control panel, as well as all the functionalities of a librarian.

## Live demo
You can try the web application using our cloud hosted website: https://214.thebottom.top/ or on HerokuApp: https://eminisce.herokuapp.com/
Some accounts you can try:

**Administrator:** username: admin password: admin  
**Librarian:** username: johnwatson password: johnwatson  
**Library user:** username: 20213344 password: 20213344  

## Instructions
 Please find here our User Manual PDF file: [Eminisce_User_Manual.pdf](docs/Eminisce_User_Manual.pdf)  
 ***Read from page 4 for instructions on setting up the Web Application.***
 ***IMPORTANT: After following step 8, Section 2.1 in the PDF, please activate your Django virtual environment, cd to the root of the project folder and run the following command:*** `python manage.py collectstatic`.
 
## Developers
Lead: **Le Vu Nguyen Khanh**  
**Tran Thanh Dat**  
**Sonia Surasa D/O Sivaprakash**
