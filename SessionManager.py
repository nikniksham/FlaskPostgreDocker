from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.PostgreConfig import DB_HOST, DB_USER, DB_NAME, DB_PASS, DB_PORT


eng = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')
Session = sessionmaker(bind=eng)