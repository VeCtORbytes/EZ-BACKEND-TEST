from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from cryptography.fernet import Fernet

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
key = Fernet.generate_key()
fernet = Fernet(key)

# Dummy storage
users = {"ops": "password", "client@example.com": "password"}
files = []
client_tokens = {}

class SignupRequest(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: SignupRequest):
    token = fernet.encrypt(user.email.encode()).decode()
    client_tokens[user.email] = token
    return {"encrypted_url": f"/verify-email/{token}"}

@app.get("/verify-email/{token}")
def verify_email(token: str):
    try:
        email = fernet.decrypt(token.encode()).decode()
        return {"message": f"Email {email} verified successfully"}
    except:
        raise HTTPException(status_code=400, detail="Invalid token")

@app.post("/login")
def login(username: str, password: str):
    if users.get(username) == password:
        return {"token": username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/upload")
def upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    if token != "ops":
        raise HTTPException(status_code=403, detail="Only Ops can upload")
    if file.filename.endswith(('.pptx', '.docx', '.xlsx')):
        files.append(file.filename)
        return {"message": "File uploaded"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")

@app.get("/files")
def list_files(token: str = Depends(oauth2_scheme)):
    if token not in client_tokens:
        raise HTTPException(status_code=403, detail="Access denied")
    return {"files": files}

@app.get("/download-file/{assignment_id}")
def download_file(assignment_id: str, token: str = Depends(oauth2_scheme)):
    if token not in client_tokens:
        raise HTTPException(status_code=403, detail="Access denied")
    encrypted_link = fernet.encrypt(assignment_id.encode()).decode()
    return {
        "download-link": f"/secure-download/{encrypted_link}",
        "message": "success"
    }

@app.get("/secure-download/{encrypted_id}")
def secure_download(encrypted_id: str, token: str = Depends(oauth2_scheme)):
    if token not in client_tokens:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        assignment_id = fernet.decrypt(encrypted_id.encode()).decode()
        return {"message": f"File {assignment_id} downloaded"}
    except:
        raise HTTPException(status_code=400, detail="Invalid link")
