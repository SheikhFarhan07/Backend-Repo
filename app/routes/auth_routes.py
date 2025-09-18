from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.utils.hashing import Hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=schemas.UserResponse)

def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = Hash.bcrypt(user.password)

    # Create new user
    new_user = models.User(
        name=user.name,
        dob=user.dob,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")

def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email"
        )

    if not Hash.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return {"message": "Login successful"}