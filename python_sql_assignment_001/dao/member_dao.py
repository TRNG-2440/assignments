from datetime import date
from typing import List
from psycopg.rows import class_row

from db.database import DatabaseManager
from model import Member
from logger import logger


class MemberDAO:
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def create(self, full_name: str, email: str, join_date: date) -> Member:
        """
        Insert a new member record into the database.

        :param full_name: The full name of the member.
        :type full_name: str
        :param email: The email address of the member.
        :type email: str
        :param join_date: The date the member joined the library.
        :type join_date: date
        :returns: The newly created Member object with its assigned ID and all fields.
        :rtype: Member
        :raises ValueError: If the insert operation returns no result.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Member)) as cur:
                    query = """INSERT INTO member(name, email, join_date) 
                        VALUES(%s, %s, %s) 
                        RETURNING member_id, name, email, join_date"""
                    result = cur.execute(
                        query, (full_name, email, join_date)
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while creating new record for {email}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_by_id(self, member_id) -> Member:
        """
        Retrieve a single member record by its primary key.

        :param member_id: The primary key of the member to fetch.
        :returns: The Member object matching the given ID.
        :rtype: Member
        :raises ValueError: If no member record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Member)) as cur:
                    query = """SELECT member_id, name, email, join_date
                        FROM member WHERE member_id = %s"""
                    result = cur.execute(query, (member_id,)).fetchone()

                    if not result:
                        logger.error(f"No record found for member_id: {member_id}")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def get_all(self) -> List[Member]:
        """
        Retrieve all member records from the database.

        :returns: A list of all Member objects stored in the member table.
        :rtype: List[Member]
        :raises ValueError: If no member records are found or the table is empty.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Member)) as cur:
                    query = """SELECT member_id, name, email, join_date
                        FROM member"""
                    result = cur.execute(query).fetchall()

                    if not result:
                        logger.error("No records found!")
                        raise ValueError("Error encountered on db operation!")
                    return result

    def update(self, member_id, full_name, email, join_date) -> Member:
        """
        Update all fields of an existing member record.

        :param member_id: The primary key of the member to update.
        :param full_name: The new full name to assign to the member.
        :type full_name: str
        :param email: The new email address to assign to the member.
        :type email: str
        :param join_date: The new join date to assign to the member.
        :type join_date: date
        :returns: The updated Member object reflecting all new field values.
        :rtype: Member
        :raises ValueError: If no member record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=class_row(Member)) as cur:
                    query = """UPDATE member 
                                SET name = %s,
                                    email = %s,
                                    join_date = %s
                                WHERE member_id = %s 
                                RETURNING member_id, name, email, join_date"""
                    result = cur.execute(
                        query,
                        (full_name, email, join_date, member_id),
                    ).fetchone()

                    if not result:
                        logger.error(
                            f"Error encountered while updating member_id: {member_id}!"
                        )
                        raise ValueError("Error encountered on db operation!")
                    return result

    def delete(self, member_id) -> None:
        """
        Delete a member record from the database by its primary key.

        Permanently removes the row from the member table. A ValueError is
        raised if the given ID does not match any existing record, detected
        by checking the cursor's rowcount after execution.

        :param member_id: The primary key of the member to delete.
        :returns: None
        :raises ValueError: If no member record is found for the given ID.
        """
        with self._db_manager.get_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    query = "DELETE FROM member WHERE member_id = %s"
                    cur.execute(query, (member_id,))

                    if cur.rowcount == 0:
                        logger.error(f"No record found for member_id: {member_id}")
                        raise ValueError("Error encountered on db operation!")
