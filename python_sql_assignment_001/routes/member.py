from typing import List

from fastapi import APIRouter, Depends, status

from models.member import MemberCreate, MemberResponse
from dependencies import get_member_service
from services import MemberService


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[MemberResponse])
def get_all(
    member_service: MemberService = Depends(get_member_service),
) -> List[MemberResponse]:
    return member_service.get_all()


@router.get(
    "/{member_id}", status_code=status.HTTP_200_OK, response_model=MemberResponse
)
def get_by_id(
    member_id: int,
    member_service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    return member_service.get_by_id(member_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MemberResponse)
def create(
    member: MemberCreate,
    member_service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    return member_service.create(member)


@router.put(
    "/{member_id}", status_code=status.HTTP_200_OK, response_model=MemberResponse
)
def update(
    member_id: int,
    member: MemberCreate,
    member_service: MemberService = Depends(get_member_service),
) -> MemberResponse:
    return member_service.update(member_id, member)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    member_id: int,
    member_service: MemberService = Depends(get_member_service),
) -> None:
    return member_service.delete_by_id(member_id)
