from datetime import date, datetime
import inspect
from typing import Annotated, Optional
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator, model_validator

from exceptions.budget import InvalidDateRangeError
from utils import Currency


class BudgetCreate(BaseModel):
    start_date: Annotated[date, Field(description="The start date of the budget")]
    end_date: Annotated[
        date, Field(description="The end date of the budget (exclusive)")
    ]

    title: Optional[str] = Field(
        default=None,
        description=inspect.cleandoc("""
            The title of the product.
            If not specified, set to <Start Month> <Start year> - <End Month> <End year> Budget"""),
    )

    currency_symbol: Optional[str] = Field(
        default=None,
        description=inspect.cleandoc("""
            Currency symbol of selected currency code.
            If not specified or incorrectly specified, set to currency symbol of `currency_code`."""),
    )

    currency_code: Annotated[str, Field(description="ISO 4217 Currency code")]

    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which budget is created",
    )
    last_updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp at which budget is last updated",
    )

    @field_validator("currency_code")
    @classmethod
    def validate_currency_code(cls, v: str) -> str:
        normalized_code = v.upper().strip()

        if normalized_code not in [e.value for e in Currency]:
            raise ValueError(f"'{v}' is not a valid currency country code.")

        return normalized_code

    @model_validator(mode="after")
    def verify_date_order(self) -> "BudgetCreate":
        if self.end_date <= self.start_date:
            raise InvalidDateRangeError(self.start_date, self.end_date)
        return self

    @model_validator(mode="after")
    def set_default_title(self) -> "BudgetCreate":
        if self.title is None:
            start_month = self.start_date.strftime("%B")
            start_year = self.start_date.year
            end_month = self.end_date.strftime("%B")
            end_year = self.end_date.year

            self.title = f"{start_month} {start_year} - {end_month} {end_year} Budget"
        return self

    @model_validator(mode="after")
    def validate_and_set_currency_symbol(self) -> "BudgetCreate":
        expected_currency = Currency(self.currency_code)

        if not self.currency_symbol or self.currency_symbol != expected_currency.symbol:
            self.currency_symbol = expected_currency.symbol

        return self


class BudgetDAO(BaseModel):
    id: Annotated[str, Field(description="Identifier for the budget")] = Field(
        default_factory=lambda: uuid4().hex
    )
    user_id: Annotated[
        str, Field(description="Identifier of the user associated with the budget")
    ]
    title: Annotated[str, Field(description="Title of the budget")]
    start_date: Annotated[date, Field(description="The start date of the budget")]
    end_date: Annotated[
        date, Field(description="The end date of the budget (exclusive)")
    ]
    currency_symbol: Annotated[
        str, Field(description="Currency symbol of the selected currency code")
    ]
    currency_code: Annotated[str, Field(description="ISO 4217 Currency code")]
    created_at: Annotated[
        datetime, Field(description="Timestamp at which budget is created")
    ]
    last_updated_at: Annotated[
        datetime, Field(description="Timestamp at which budget is last updated")
    ]


class BudgetResponse(BaseModel):
    id: Annotated[str, Field(description="Identifier for the budget")]
    title: Annotated[str, Field(description="Title of the budget")]
    start_date: Annotated[date, Field(description="The start date of the budget")]
    end_date: Annotated[
        date, Field(description="The end date of the budget (exclusive)")
    ]
    currency_symbol: Annotated[
        str, Field(description="Currency symbol of the selected currency code")
    ]
    currency_code: Annotated[str, Field(description="ISO 4217 Currency code")]
    created_at: Annotated[
        datetime, Field(description="Timestamp at which budget is created")
    ]
    last_updated_at: Annotated[
        datetime, Field(description="Timestamp at which budget is last updated")
    ]
