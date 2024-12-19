from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SECRET_KEY = "00ee71fe28f197ddb9e35a26f61bb1969be1a6d3472e34cd8b08fb3b8278bf5a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# SQLite 配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./main.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 加密與驗證
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 用戶數據庫模型
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="FE")
    disabled = Column(Boolean, default=False)


# Pydantic 模型
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: Optional[str] = "FE"
    disabled: Optional[bool] = False


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "FE"


class Token(BaseModel):
    access_token: str
    token_type: str


# 創建數據表
Base.metadata.create_all(bind=engine)


# 工具函數
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 依賴
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db, username: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_role(db, username: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.username == username).first().role


def authenticate_user(db, username: str, password: str) -> Optional[UserDB]:
    user = get_user(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# FastAPI 應用程序
app = FastAPI()


# 登入
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[SessionLocal, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


# 創建新用戶
@app.post("/users/", response_model=User)
def create_user(
    user: UserCreate,
    db: Annotated[SessionLocal, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    role = get_user(db, username).role
    if role not in ["FE", "Admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    hashed_password = get_password_hash(user.password)
    new_user = UserDB(
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 更新用戶信息
@app.put("/users/{username}", response_model=User)
def update_user(
    username: str,
    user: UserCreate,
    db: Annotated[SessionLocal, Depends(get_db)],
):
    db_user = get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.full_name = user.full_name
    db_user.role = user.role
    db_user.hashed_password = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


# 讀取當前用戶信息
@app.get("/users/me/", response_model=User)
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[SessionLocal, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, username)
    if not user:
        raise credentials_exception
    return user
