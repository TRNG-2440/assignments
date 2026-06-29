from dataclasses import asdict
from typing import List, Optional

from psycopg import DatabaseError

from models.member import Member, MemberCreate, MemberResponse
from exceptions import MemberExistsError, MemberHasLoansError, MemberNotFoundError
from models.model import Loan


class MemberService:
    def __init__(self, member_repo, loan_repo) -> None:
        self._member_repo = member_repo
        self._loan_repo = loan_repo

    def get_all(self) -> List[MemberResponse]:
        members: List[Member] = self._member_repo.get_all()
        return type(self)._convert_to_responses(members)

    def get_by_id(self, member_id) -> MemberResponse:
        member: Optional[Member] = self._member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id, "No record found!")
        return type(self)._convert_to_response(member)

    def create(self, member: MemberCreate) -> MemberResponse:
        member_with_email: Member = self._member_repo.get_by_email(member.email)
        if member_with_email:
            raise MemberExistsError(member.email, "Member already exists!")
        created_member = self._member_repo.create(
            member.name, member.email, member.join_date
        )
        if not created_member:
            raise DatabaseError
        return type(self)._convert_to_response(created_member)

    def update(self, member_id: int, update_member: MemberCreate) -> MemberResponse:
        member: Optional[Member] = self._member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id, "No record found!")
        updated_member = self._member_repo.update(
            member_id, update_member.name, update_member.email, update_member.join_date
        )
        if not updated_member:
            raise DatabaseError()
        return type(self)._convert_to_response(updated_member)

    def delete_by_id(self, member_id) -> None:
        member: Optional[Member] = self._member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id, "No record found!")
        loans: List[Loan] = self._loan_repo.get_by_member_id(member_id)
        if loans:
            raise MemberHasLoansError(member_id, "This member has borrowed books!")
        self._member_repo.delete(member_id)

    @classmethod
    def _convert_to_responses(cls, members: List[Member]) -> List[MemberResponse]:
        return [cls._convert_to_response(member) for member in members]

    @staticmethod
    def _convert_to_response(member: Member) -> MemberResponse:
        member_dict = asdict(member)
        return MemberResponse.model_validate(member_dict)
