from fastapi import Depends, FastAPI
import uvicorn

from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv
load_dotenv('../Account/.env')

DB_USER = os.environ.get('db_user')
DB_PW = os.environ.get('db_password')
DB_HOST = os.environ.get('db_host')
DB_SCHEMA = os.environ.get('db')

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:3306/{DB_SCHEMA}'

# Create the SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 구조 연결
Base = declarative_base() 

## Model
# 테이블 객체 생성을 위한 클래스
class User1(Base):
    __tablename__ = "shuttle" # 사용할 테이블 이름

    # Columns
    post_num = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    
class User2(Base):
    __tablename__ = "shuttle_notice" # 사용할 테이블 이름

    # Columns
    post_num = Column(Integer, nullable=False, primary_key=True)
    date = Column(DATE, nullable=False)


def get_user1(db: Session):
    return db.query(User1).all()
    
def get_user2(db: Session):
    return db.query(User2).all()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/shuttle")
def read_users1(db: Session = Depends(get_db)):
    return get_user1(db)
    
@app.get("/2")
def read_users2(db: Session = Depends(get_db)):
    return get_user2(db)

if __name__ == '__main__':
    uvicorn.run("app:app",host='0.0.0.0', port=8888)