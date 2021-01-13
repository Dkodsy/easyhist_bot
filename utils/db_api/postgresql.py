import asyncpg
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.IP,
        )
        return cls(pool)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT NOT NULL,
            Name varchar(255) NOT NULL,
            start_time timestamp,
            PRIMARY KEY (id)
            );
        """
        await self.pool.execute(sql)

    async def add_user(self, id: int, name: str, start_time):
        sql = """
        INSERT INTO Users(id, Name, start_time) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, id, name, start_time)

    async def select_start_time(self, id):
        sql = '''
        SELECT start_time FROM users WHERE id=$1
        '''
        return await self.pool.fetchval(sql, id)


'''
    Оставлю, на случай, если вернусь к идее с отложенными сообщениями
    async def add_text(self, post: str):
        sql = """
        INSERT INTO Posts(Post) VALUES ($1)
        """
        await self.pool.execute(sql, post)


    async def create_table_posts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Posts (
            id SERIAL,
            Post text,
            PRIMARY KEY (id)
            );
        """
        await self.pool.execute(sql)
'''
