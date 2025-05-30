
#  Secure File Sharing System – Backend Intern Test

This project is a secure file-sharing system built using **FastAPI** and **MongoDB**. It was developed as part of a back-end internship test, focusing on RESTful API development, user role management, and secure file operations.

##  User Roles

### Ops User
- Login
- Upload `.pptx`, `.docx`, `.xlsx` files only

### Client User
- Sign up (returns an encrypted verification URL)
- Email verification
- Login
- List uploaded files
- Download files using a secure encrypted URL (accessible only by verified client users)

##  Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB (NoSQL)
- **Security**: JWT for authentication, Fernet for URL encryption
- **Email**: Token-based verification
- **Testing**: Postman collection + Pytest support


