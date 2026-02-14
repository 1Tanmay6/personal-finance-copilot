from pathlib import Path
from functools import wraps

from ..core import get_logger
from ..core.database.database import Database
logger = get_logger(__name__)


class DataService:
    """
    Data Service is a mixture of all the data resource related module.
    """
    def __init__(self, db: Database):
        self.db = db


if __name__ == '__main__':
    import time
    
    @DataService.db_exists
    def sample():
        st = time.time()
        time.sleep(2)
        en = time.time()
        print(f"Time Elapsed {en-st}")

    sample()