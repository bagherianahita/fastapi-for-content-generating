import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

class Settings(BaseSettings):
    auth_secret_key: str = "change-me-in-production"
    auth_algorithm: str = "HS256"
    database_url: str = "sqlite:///./workout_app.db"
    api_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class Base(DeclarativeBase):
    pass


workout_routine = Table(
    "workout_routine",
    Base.metadata,
    Column("workout_id", ForeignKey("workouts.id"), primary_key=True),
    Column("routine_id", ForeignKey("routines.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    workouts = relationship("Workout", back_populates="owner")
    routines = relationship("Routine", back_populates="owner")


class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workouts")
    routines = relationship("Routine", secondary=workout_routine, back_populates="workouts")


class Routine(Base):
    __tablename__ = "routines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="routines")
    workouts = relationship("Workout", secondary=workout_routine, back_populates="routines")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.api_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class WorkoutCreate(BaseModel):
    name: str
    description: str = ""


class RoutineCreate(BaseModel):
    name: str


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed_demo_data() -> None:
    """Create demo user and sample workouts for employer quick-start."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "demo").first()
        if user:
            return
        user = User(username="demo", hashed_password=hash_password("demo123"))
        db.add(user)
        db.commit()
        db.refresh(user)
        db.add(Workout(name="Morning Run", description="5 km easy pace", owner_id=user.id))
        db.add(Workout(name="Upper Body", description="Bench, rows, shoulders", owner_id=user.id))
        db.add(Routine(name="Weekday Plan", owner_id=user.id))
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup_seed() -> None:
    seed_demo_data()


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=8)
    return jwt.encode(payload, settings.auth_secret_key, algorithm=settings.auth_algorithm)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.auth_secret_key, algorithms=[settings.auth_algorithm])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(username=user_in.username, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": create_token({"sub": user.username}), "token_type": "bearer"}


@app.get("/workouts")
def list_workouts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Workout).filter(Workout.owner_id == user.id).all()


@app.post("/workouts", status_code=status.HTTP_201_CREATED)
def create_workout(body: WorkoutCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    workout = Workout(name=body.name, description=body.description, owner_id=user.id)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


@app.get("/routines")
def list_routines(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Routine).filter(Routine.owner_id == user.id).all()


@app.post("/routines", status_code=status.HTTP_201_CREATED)
def create_routine(body: RoutineCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    routine = Routine(name=body.name, owner_id=user.id)
    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine
