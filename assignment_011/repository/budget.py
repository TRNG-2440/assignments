import os
from typing import Any, List, Tuple

from dotenv import load_dotenv
from pydantic import TypeAdapter

from exceptions import ResourceNotFoundError
from exceptions import FilePathNotSpecifiedError
from models.budget import BudgetDAO, BudgetGoalDAO, GoalType
from utils import append_record_to_json, read_json_file, write_all_records_to_json


load_dotenv()


class BudgetRepository:
    def __init__(self) -> None:
        self._file_path = os.getenv("BUDGET_DATA")
        self._key = os.getenv("BUDGET_DATA_KEY")

    def create_budget(self, new_budget: BudgetDAO) -> None:
        if self._file_path and self._key:
            new_budget.title = self._generate_unique_title(
                new_budget.title, new_budget.user_id
            )
            append_record_to_json(
                self._file_path, self._key, new_budget.model_dump_json()
            )
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )

    def has_budget(self, budget_id: str) -> bool:
        all_budgets: List[BudgetDAO] = self._read_all()
        return any((budget for budget in all_budgets if budget.id == budget_id))

    def is_user_budget_owner(self, user_id: str, budget_id: str) -> bool:
        all_budgets: List[BudgetDAO] = self._read_all()
        return any(
            (
                budget
                for budget in all_budgets
                if budget.user_id == user_id and budget.id == budget_id
            )
        )

    def _generate_unique_title(self, base_title: str, user_id: str) -> str:
        all_budgets = self._read_all()

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

    def get_budget(self, user_id: str, id: str) -> BudgetDAO:
        all_budgets_all_users = self._read_all()
        filtered_budgets = [
            budget
            for budget in all_budgets_all_users
            if budget.user_id == user_id and budget.id == id
        ]
        if len(filtered_budgets) > 1 or len(filtered_budgets) == 0:
            raise ResourceNotFoundError("budget", id)

        return filtered_budgets[0]

    def get_budgets(self, user_id: str) -> List[BudgetDAO]:
        all_budgets_all_users = self._read_all()
        filtered_budgets = [
            budget for budget in all_budgets_all_users if budget.user_id == user_id
        ]
        return filtered_budgets

    def _read_all(self) -> List[BudgetDAO]:
        if self._file_path and self._key:
            data = read_json_file(self._file_path, self._key)
            adapter = TypeAdapter(list[BudgetDAO])
            all_budgets: List[BudgetDAO] = adapter.validate_python(data)
            return all_budgets
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )


class BudgetGoalsRepository:
    def __init__(self) -> None:
        self._file_path = os.getenv("BUDGET_GOALS_DATA")
        self._key = os.getenv("BUDGET_GOALS_DATA_KEY")

    def upsert_budget_goals(self, goals: List[BudgetGoalDAO]) -> List[BudgetGoalDAO]:
        all_budget_all_goals: List[BudgetGoalDAO] = self._read_all()

        existing_goals_map = {
            type(self)._get_goal_type_key(goal): goal for goal in all_budget_all_goals
        }

        merged_goals = []
        for incoming_goal in goals:
            key = type(self)._get_goal_type_key(incoming_goal)

            if key in existing_goals_map:
                original_goal = existing_goals_map[key]
                incoming_goal.id = original_goal.id
                incoming_goal.created_at = original_goal.created_at

            existing_goals_map[key] = incoming_goal
            merged_goals.append(incoming_goal)
        updated_goals_list: List[BudgetGoalDAO] = list(existing_goals_map.values())
        if self._file_path and self._key:
            write_all_records_to_json(
                self._file_path,
                self._key,
                [g.model_dump_json() for g in updated_goals_list],
            )
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )
        return merged_goals

    def get_budget_goals(self, budget_id: str) -> List[BudgetGoalDAO]:
        all_budgets_all_goals = self._read_all()
        filtered_goals = [
            goal for goal in all_budgets_all_goals if goal.budget_id == budget_id
        ]
        return filtered_goals

    @staticmethod
    def _get_goal_type_key(goal: BudgetGoalDAO) -> Tuple[str, str, Any]:
        target_identifier = (
            goal.category.value
            if goal.type == GoalType.EXPENSE and goal.category
            else None
        )
        return (goal.budget_id, goal.type, target_identifier)

    def _read_all(self) -> List[BudgetGoalDAO]:
        if self._file_path and self._key:
            data = read_json_file(self._file_path, self._key)
            adapter = TypeAdapter(list[BudgetGoalDAO])
            all_budgets: List[BudgetGoalDAO] = adapter.validate_python(data)
            return all_budgets
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for BUDGET_DATA or key not specified!"
            )
