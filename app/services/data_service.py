from pathlib import Path
from functools import wraps
from typing import Literal
from io import BytesIO, StringIO
import pandas as pd

from ..core import get_logger
from ..core.database import Database, Transaction
from ..core.exceptions import WrongFileTypeError

logger = get_logger(__name__)


class DataService:
    """
    Data Service is a mixture of all the data resource related module.
    """
    def __init__(self):
        self.db = Database()

    async def _convert_file_to_df(self, file: str | BytesIO | StringIO) -> pd.DataFrame:
        df: pd.DataFrame
        logger.info("Initializing a intermediate med")
        try:
            if isinstance(file, str) or isinstance(file, StringIO):
                try:
                    df = pd.read_csv(file)
                    logger.info("Successfully loaded the CSV, trying to upload")
                except FileNotFoundError as _:
                    df = pd.read_csv(StringIO(file))
                    logger.info("Successfully loaded the CSV, trying to upload")
            elif isinstance(file, BytesIO):
                logger.warning("Type BytesIO passing")
                raise NotImplementedError("Not yet implemented ByteIO type loading.")
            else:
                raise WrongFileTypeError("The file type provided is not yet compatible")
        except Exception as e:
            logger.error(f"Error loading the CSV: {e}")
            raise Exception("Something went wrong while reading and loading the file")

        return df
    

    async def insert_multiple_transactions(self,
                                           file: str | BytesIO | StringIO | pd.DataFrame, 
                                           mode: None | Literal['ADD', 'OVERWRITE'] = None) -> None:
        if mode == 'ADD':
            pass
        elif mode == 'OVERWRITE':
            pass
        else:
            if isinstance(file, pd.DataFrame):
                df = file
            else:
                df = await self._convert_file_to_df(file=file)

            if df.empty:
                return
            
            df = df.copy()
            records = []
            for _, row in df.iterrows():
                txn_type = "CREDIT" if float(row.get("credit", 0) or 0) > 0 else "DEBIT"

                records.append({
                    "transaction_date": row["transaction_date"],
                    "description": row["description"],
                    "type": txn_type,
                    "closing_balance": row['closing_balance'],
                    "account": row['account'],
                    "ref_no": row["ref_no"],
                    "source": "File",
                    "amount": float(row.get("credit", 0) or 0) if txn_type == 'CREDIT' else float(row.get("debit", 0) or 0)
                })
            await self.db.bulk_insert(model=Transaction, records=records)



if __name__ == '__main__':
    import asyncio
    ds = DataService()

    # asyncio.run(ds.insert_multiple_transactions(file='./data/raw/sample_transactions_raw.csv'))
    print(asyncio.run(ds.db.verify_insert(model=Transaction, ref_no='SBIN698219')).type)