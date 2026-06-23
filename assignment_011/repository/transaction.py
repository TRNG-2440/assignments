from datetime import date
import os
from typing import List

from dotenv import load_dotenv
from pydantic import TypeAdapter

from exceptions import FilePathNotSpecifiedError
from models.transaction import (
    TransactionDAO,
    TransactionFilterParams,
)
from utils import append_records_to_json, read_json_file, write_all_records_to_json

load_dotenv()


class TransactionRepository:
    def __init__(self) -> None:
        self._file_path = os.getenv("TRANSACTIONS_DATA")
        self._key = os.getenv("TRANSACTIONS_DATA_KEY")

    def create_transactions(self, transactions: List[TransactionDAO]) -> None:
        if self._file_path and self._key:
            append_records_to_json(
                self._file_path,
                self._key,
                [trnx.model_dump_json() for trnx in transactions],
            )
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for TRANSACTIONS_DATA or key not specified!"
            )

    def get_transactions(
        self, user_id: str, params: TransactionFilterParams
    ) -> List[TransactionDAO]:
        all_transactions_all_users: List[TransactionDAO] = self._read_all()
        filtered_trnxs: List[TransactionDAO] = [
            trnx
            for trnx in all_transactions_all_users
            if type(self)._construct_condition(trnx, user_id, params)
        ]
        return filtered_trnxs

    def is_trnx(self, id: str) -> bool:
        all_transactions_all_users: List[TransactionDAO] = self._read_all()
        return any((trnx for trnx in all_transactions_all_users if trnx.id == id))

    def is_trnx_owner_user(self, user_id: str, id: str) -> bool:
        all_transactions_all_users: List[TransactionDAO] = self._read_all()
        return any(
            (
                trnx
                for trnx in all_transactions_all_users
                if trnx.id == id and trnx.user_id == user_id
            )
        )

    def delete_trnx(self, id: str) -> None:
        all_transactions_all_users: List[TransactionDAO] = self._read_all()
        filtered_trnxs: List[TransactionDAO] = [
            trnx for trnx in all_transactions_all_users if trnx.id != id
        ]
        if self._file_path and self._key:
            write_all_records_to_json(
                self._file_path,
                self._key,
                [trnx.model_dump_json() for trnx in filtered_trnxs],
            )
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for TRANSACTIONS_DATA or key not specified!"
            )

    def get_budget_transactions(
        self, user_id: str, budget_start_date: date, budget_end_date: date
    ) -> List[TransactionDAO]:
        all_transactions_all_users: List[TransactionDAO] = self._read_all()
        filtered_trnxs: List[TransactionDAO] = [
            trnx
            for trnx in all_transactions_all_users
            if (trnx.user_id == user_id)
            and (budget_start_date <= trnx.transaction_date < budget_end_date)
        ]
        return filtered_trnxs

    @staticmethod
    def _construct_condition(
        trnx: TransactionDAO, user_id: str, params: TransactionFilterParams
    ) -> bool:
        return (trnx.user_id == user_id) and (
            params.start_date <= trnx.transaction_date <= params.end_date
        )

    def _read_all(self) -> List[TransactionDAO]:
        if self._file_path and self._key:
            data = read_json_file(self._file_path, self._key)
            adapter = TypeAdapter(list[TransactionDAO])
            all_transactions: List[TransactionDAO] = adapter.validate_python(data)
            return all_transactions
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for TRANSACTIONS_DATA or key not specified!"
            )
