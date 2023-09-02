from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_chapters(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Chapters (
        id SERIAL PRIMARY KEY,
        chapter_name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)
    
    async def add_chapters(self, chapter_name):
        sql = "INSERT INTO Chapters (chapter_name) VALUES($1) returning *"
        return await self.execute(sql, chapter_name, fetchrow=True)

    async def select_all_chapters(self):
        sql = "SELECT * FROM Chapters"
        return await self.execute(sql, fetch=True)
    
    async def create_table_categories(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Categories (
        id SERIAL PRIMARY KEY,
        cat_name VARCHAR(255) NOT NULL,
        chapter_id INTEGER NOT NULL
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_infomation(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Infomation (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        caption text NOT NULL,
        photos text NOT NULL,
        video text NULL
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_infomation2(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Infomation2 (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        caption text NOT NULL,
        photos text NOT NULL
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_infomation3(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Aks_info (
        id SERIAL PRIMARY KEY,
        caption text NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_infomation4(self):
        sql = """
        CREATE TABLE IF NOT EXISTS register_text (
        id SERIAL PRIMARY KEY,
        caption text NOT NULL
        );  
        """
        await self.execute(sql, execute=True)

    async def delete_info4(self, title):
        sql = "DELETE FROM register_text WHERE title=$1"
        return await self.execute(sql, title, execute=True)
    
    async def update_infomation4(self, id, caption):
        sql = "UPDATE register_text SET caption=$2 WHERE id=$1 returning *"
        return await self.execute(sql, id, caption, fetchrow=True)

    async def add_infomation4(self, caption):
        sql = "INSERT INTO register_text (caption) VALUES($1) returning *"
        return await self.execute(sql, caption, fetchrow=True)

    async def select_all_infomation4(self):
        sql = "SELECT * FROM register_text"
        return await self.execute(sql, fetchrow=True)

    async def create_table_register_info(self):
        sql = """
        CREATE TABLE IF NOT EXISTS RegInfor (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name text NOT NULL,
        last_name text NOT NULL,
        phone text NOT NULL,
        date text NULL
        );
        """
        await self.execute(sql, execute=True)

    async def delete_reginfor(self):
        await self.execute("DELETE FROM RegInfor WHERE TRUE", execute=True)
    
    async def select_all_register_info(self):
        sql = "SELECT * FROM RegInfor"
        return await self.execute(sql, fetch=True)
    
    async def select_register_info(self, **kwargs):
        sql = "SELECT * FROM RegInfor WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_register_info(self, user_id, name, last_name, phone, date=None):
        sql = "INSERT INTO RegInfor (user_id, name, last_name, phone, date) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, user_id, name, last_name, phone, date, fetchrow=True)


    async def delete_info3(self, title):
        sql = "DELETE FROM Aks_info WHERE title=$1"
        return await self.execute(sql, title, execute=True)
    
    async def update_infomation3(self, id, caption):
        sql = "UPDATE Aks_info SET caption=$2 WHERE id=$1 returning *"
        return await self.execute(sql, id, caption, fetchrow=True)

    async def add_infomation3(self, caption):
        sql = "INSERT INTO Aks_info (caption) VALUES($1) returning *"
        return await self.execute(sql, caption, fetchrow=True)

    async def select_all_infomation3(self):
        sql = "SELECT * FROM Aks_info"
        return await self.execute(sql, fetchrow=True)


    async def delete_info2(self, title):
        sql = "DELETE FROM Infomation2 WHERE title=$1"
        return await self.execute(sql, title, execute=True)
    
    async def add_infomation2(self, title, caption, photos, video=None):
        sql = "INSERT INTO Infomation2 (title, caption, photos) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, title, caption, photos, video, fetchrow=True)

    async def select_all_infomation2(self):
        sql = "SELECT * FROM Infomation2"
        return await self.execute(sql, fetch=True)

    async def delete_info(self, title):
        sql = "DELETE FROM Infomation WHERE title=$1"
        return await self.execute(sql, title, execute=True)
    
    async def add_infomation(self, title, caption, photos, video=None):
        sql = "INSERT INTO Infomation (title, caption, photos, video) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, title, caption, photos, video, fetchrow=True)

    async def select_all_infomation(self):
        sql = "SELECT * FROM Infomation"
        return await self.execute(sql, fetch=True)


    async def add_categories(self, cat_name, chapter_id):
        sql = "INSERT INTO Categories (cat_name, chapter_id) VALUES($1, $2) returning *"
        return await self.execute(sql, cat_name, chapter_id, fetchrow=True)

    async def select_all_categories(self):
        sql = "SELECT * FROM Categories"
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
