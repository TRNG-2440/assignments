import os
from typing import List

from dotenv import load_dotenv
from pydantic import TypeAdapter

from exceptions import FilePathNotSpecifiedError
from models.budget import BudgetDAO
from utils import append_record_to_json, read_json_file


load_dotenv()


class BudgetRepository:
    def __init__(self) -> None:
        self.file_path = os.getenv("BUDGET_DATA")
        self.key = os.getenv("BUDGET_DATA_KEY")

    def create_budget(self, new_budget: BudgetDAO) -> None:
        if self.file_path and self.key:
            new_budget.title = self._generate_unique_title(
                new_budget.title, new_budget.user_id
            )
            append_record_to_json(
                self.file_path, self.key, new_budget.model_dump_json()
            )
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )

    def _generate_unique_title(self, base_title: str, user_id: str) -> str:
        if self.file_path and self.key:
            data = read_json_file(self.file_path, self.key)
            adapter = TypeAdapter(list[BudgetDAO])
            all_budgets: List[BudgetDAO] = adapter.validate_python(data)

            user_budget_titles = {
                budget.title for budget in all_budgets if budget.user_id == user_id
            }

            if base_title not in user_budget_titles:
                return base_title

            counter = 1
            while True:
                new_title = f"{base_title} ({counter})"
                if new_title not in user_budget_titles:
                    return new_title
                counter += 1
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )
