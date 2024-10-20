from sqlalchemy import create_engine, Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the Users table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

# Create the SQLAlchemy engine and bind it to the MySQL database
DATABASE_URL = 'mysql+mysqlconnector://root:appa@localhost/library_management'

engine = create_engine(DATABASE_URL)

# Create the session class
Session = sessionmaker(bind=engine)

# Create the tables in the database
Base.metadata.create_all(engine)

print("Table 'users' created successfully.")



