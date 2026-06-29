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
        """
        Retrieve all members and return them as response models.

        :returns: A list of MemberResponse objects for all members in the database.
        :rtype: List[MemberResponse]
        """
        members: List[Member] = self._member_repo.get_all()
        return type(self)._convert_to_responses(members)

    def get_by_id(self, member_id) -> MemberResponse:
        """
        Retrieve a single member by their primary key and return them as a response model.

        :param member_id: The primary key of the member to fetch.
        :returns: A MemberResponse object for the matching member.
        :rtype: MemberResponse
        :raises MemberNotFoundError: If no member record is found for the given ID.
        """
        member: Optional[Member] = self._member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id, "No record found!")
        return type(self)._convert_to_response(member)

    def create(self, member: MemberCreate) -> MemberResponse:
        """
        Create a new member after validating that their email is not already registered.

        :param member: A MemberCreate model containing the new member's details.
        :type member: MemberCreate
        :returns: A MemberResponse object for the newly created member.
        :rtype: MemberResponse
        :raises MemberExistsError: If a member with the same email already exists.
        :raises DatabaseError: If the create operation returns no result.
        """
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
        """
        Update all fields of an existing member record.

        :param member_id: The primary key of the member to update.
        :type member_id: int
        :param update_member: A MemberCreate model containing the updated member details.
        :type update_member: MemberCreate
        :returns: A MemberResponse object reflecting the updated member.
        :rtype: MemberResponse
        :raises MemberNotFoundError: If no member record is found for the given ID.
        :raises DatabaseError: If the update operation returns no result.
        """
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
        """
        Delete a member by their primary key, provided they have no associated loans.

        Verifies the member exists and has no active or historical loan records
        before proceeding with deletion, preventing orphaned loan records.

        :param member_id: The primary key of the member to delete.
        :returns: None
        :raises MemberNotFoundError: If no member record is found for the given ID.
        :raises MemberHasLoansError: If the member has one or more loan records.
        """
        member: Optional[Member] = self._member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id, "No record found!")
        loans: List[Loan] = self._loan_repo.get_by_member_id(member_id)
        if loans:
            raise MemberHasLoansError(member_id, "This member has borrowed books!")
        self._member_repo.delete(member_id)

    @classmethod
    def _convert_to_responses(cls, members: List[Member]) -> List[MemberResponse]:
        """
        Convert a list of Member dataclass instances to a list of MemberResponse models.

        :param members: A list of Member dataclass instances to convert.
        :type members: List[Member]
        :returns: A list of validated MemberResponse objects.
        :rtype: List[MemberResponse]
        """
        return [cls._convert_to_response(member) for member in members]

    @staticmethod
    def _convert_to_response(member: Member) -> MemberResponse:
        """
        Convert a single Member dataclass instance to a MemberResponse model.

        :param member: The Member dataclass instance to convert.
        :type member: Member
        :returns: A validated MemberResponse object.
        :rtype: MemberResponse
        """
        member_dict = asdict(member)
        return MemberResponse.model_validate(member_dict)
