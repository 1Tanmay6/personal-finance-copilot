from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text, insert, select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from .models import Base
from ..config import DB_LOCATION
from ...core import get_logger

logger = get_logger(__name__)

class Database:
    """
    Manages asynchronous database connections and lifecycle.

    Responsibilities:
    - Create async SQLAlchemy engine
    - Provide session factory
    - Initialize tables
    - Perform integrity checks
    """
    def __init__(self):
        """
        Initialize the async database engine.
        """
        logger.info("Initializing database engine")
        self._engine = create_async_engine(self.get_db_url(), echo=False)

    def get_db_url(self):
        """
        Build the SQLite async database URL.

        Returns:
            str: Database connection string.
        """
        return f"sqlite+aiosqlite:///{DB_LOCATION}"

    def get_session(self):
        """
        Create an AsyncSession factory.

        Returns:
            sessionmaker: Configured async SQLAlchemy session maker.
        """
        AsyncSessionLocal = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        return AsyncSessionLocal\
    
    async def insert_one(self, model, record: dict):
        """
        Insert a single record into a table.

        Args:
            model: SQLAlchemy model class
            record (dict): Column-value mapping

        Returns:
            Result object from SQLAlchemy execution
        """
        if not record:
            logger.warning("Empty record provided for insert.")
            return None

        async with self.get_session()() as session:
            async with session.begin():
                result = await session.execute(insert(model).values(**record))

        logger.info(f"Inserted 1 record into {model.__tablename__}")
        return result

    async def bulk_insert(self, model, records: list[dict]):
        """
        Generic bulk insert utility.

        Args:
            model: SQLAlchemy model class
            records (list[dict]): List of row dictionaries
        """
        if not records:
            logger.warning("No records provided for bulk insert.")
            return

        async with self.get_session()() as session:
            async with session.begin():
                await session.execute(insert(model), records)

        logger.info(f"Inserted {len(records)} records into {model.__tablename__}")

    async def verify_insert(self, model: any, ref_no: str):

        async with self.get_session()() as session:
            result = await session.execute(
                select(model).where(model.ref_no == ref_no)
            )

            return result.scalar_one_or_none()

    async def integrity_check(self):
        """
        Run SQLite integrity check.

        Returns:
            str: Result of integrity check ("ok" if healthy).
        """
        async with self._engine.connect() as conn:
            result = await conn.execute(text("PRAGMA integrity_check;"))
            return result.scalar()

    async def init_db(self):
        """
        Create all database tables defined in SQLAlchemy models.
        """
        try:
            async with self._engine.begin() as conn:
                logger.info("Connected to database, creating tables")
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Completed the database creation successfully")
        except Exception as e:
            logger.error("Failed to initialise database stopping the engine")

    async def db_check(self):
        """
        Verify database existence and integrity.

        - Creates database if missing
        - Runs integrity check
        - Raises error if corrupted
        """
        try:
            if Path(DB_LOCATION).expanduser().resolve().is_file():
                logger.debug(f"DB exists at location: {DB_LOCATION}")
                status = await self.integrity_check()
            else:
                logger.warning(f"DB does not exists at location: {DB_LOCATION}")
                logger.info("Creating a empty database at the given location.")
                status = await self.integrity_check()
                await self.init_db()

            if status != "ok":
                raise RuntimeError("Database corrupted!")
            else:
                logger.info("Database integrity check complete ready to go")
                
        except Exception as e:
            raise Exception("Database checking or creation is having some problems, please try again or contact the developer (developer note pls leave a issue on github or email)")
if __name__ == '__main__':
    database = Database()

    import asyncio

    asyncio.run(database.db_check())
