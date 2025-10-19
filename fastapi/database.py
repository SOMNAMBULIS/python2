# pip install sqlalchemy

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, text

from models import UserOrm, QuestionOrm, Model
from schemas import UserAdd, QuestionAdd

import os


BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'fastapi.db')    

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
new_session = async_sessionmaker(engine, expire_on_commit=False)






class  DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    
    @classmethod            
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)     
    
    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30),
                UserOrm(name='user3', age=41),
                UserOrm(name='user4', age=42),
                UserOrm(name='user5', age=43),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]

            session.add_all(users)            
            await session.flush() 
            await session.commit()

    @classmethod
    async def add_question(cls):
        async with new_session() as session:
            question = [
                QuestionOrm(name = 'question1',answer = '1',opt1='2', opt2='3'),
                QuestionOrm(name = 'question2',answer = '1',opt1='2', opt2='3'),
                QuestionOrm(name = 'question3',answer = '1',opt1='2', opt2='3')
            ]

            session.add_all(question)
            await session.flush()
            await session.commit()





class UserRepository:
        
    @classmethod
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump() # в словарь
            # print(data)
            user = UserOrm(**data) #
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
    
    @classmethod        
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            
            query = select(UserOrm)
            
            res = await session.execute(query)
            users = res.scalars().all() # -> список
            return users
        
    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id==id)            
            res = await session.execute(query)
            user = res.scalars().first()
            return user
        


class QuestionRepository:
    @classmethod
    async def add_question(cls, question: QuestionAdd) -> int:
        async with new_session() as session:
            data = question.model_dump()
            question = QuestionOrm(**data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.id
