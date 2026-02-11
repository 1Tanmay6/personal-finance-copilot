from pathlib import Path
from functools import wraps

from ..core import get_logger
from ..core.config import DB_LOCATION

logger = get_logger(__name__)


class DataService:
    """
    Data Service is a mixture of all the data resource realted module.
    """
    def __init__(self):
        pass
    
    @staticmethod
    def db_exists(func):
        """
        Sees if the database exists at the given location.  
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Path(DB_LOCATION).expanduser().resolve().is_file():
                logger.debug(f"DB exists at location: {DB_LOCATION}")
            else:
                logger.warning(f"DB does not exists at location: {DB_LOCATION}")
                logger.info("Creating a empty database at the given location.")

            return func(*args, **kwargs)

        return wrapper
    
    def _create_empty_database(self):
        """
        Creates an empty database either at the start of the application or if the database is not found at the location.
        """
        pass


if __name__ == '__main__':
    import time
    
    @DataService.db_exists
    def sample():
        st = time.time()
        time.sleep(2)
        en = time.time()
        print(f"Time Elapsed {en-st}")

    sample()