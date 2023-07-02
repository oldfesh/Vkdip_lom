import sqlalchemy as sq
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import db_url_object
from pprint import pprint

class Base(DeclarativeBase): 
    pass

class User(Base):
    """Создаёт класс-отношение для пользователя бота
    :profile_id: уникальный id аккауанта во ВКонтакте
    :anket_id: уникальный id анкет поиска
    :like: по умолчанию False, необходим для изьраных анкет"""
    __tablename__ = 'search_results'

    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)



class DataStore:
    def __init__(self):
        self._engine = self._create_engine_connection()
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._create_tables()

    def _create_engine_connection(self):
        """Создаёт движок сессии"""
        engine = sq.create_engine(db_url_object)
        return engine

    def _create_tables(self): 
        """Создание, либо дроп отношений-классов
        :engine: указатель на бд"""
        # Base.metadata.drop_all(bind=self._engine)
        Base.metadata.create_all(bind=self._engine)

    # добавление записи в бд

    def add_user(self, profile_id: int, worksheet_id: int):
        self._session.add(User(profile_id=profile_id, worksheet_id=worksheet_id))
        self._session.commit()

    # проверка записи в бд 

    def request_id(self, profile_id: int,  worksheet_id: int) -> bool:
        return bool(self._session.query(User).filter(User.profile_id==profile_id, 
                                                User.worksheet_id == worksheet_id).all())

if __name__ == '__main__':
    #create_db()
    eng = DataStore()
    pprint(eng.request_id())

