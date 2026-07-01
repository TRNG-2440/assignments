import psycopg
from psycopg.rows import dict_row
from typing import Optional
from datetime import date

from db_util import get_conn_string
from dao import MemberRecord


class MemberDAO:
    def __init__(self):
        self.conn_string = get_conn_string()

    def _map_row(self, row) -> MemberRecord:
        return MemberRecord(
            member_id=row["member_id"],
            full_name=row["full_name"],
            email=row["email"],
            join_date=row["join_date"]
        )

    def create(self, full_name: str, email: str, join_date: date) -> MemberRecord:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    INSERT INTO library.members (
                        full_name,
                        email,
                        join_date
                    )
                    VALUES (%s, %s, %s)
                    RETURNING member_id, full_name, email, join_date
                """, (full_name, email, join_date))
                row = cursor.fetchone()
                return self._map_row(row)

    def get_by_id(self, member_id: int) -> Optional[MemberRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT member_id, full_name, email, join_date
                    FROM library.members
                    WHERE member_id = %s
                """, (member_id,))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def get_all(self) -> list[MemberRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    SELECT member_id, full_name, email, join_date
                    FROM library.members
                    ORDER BY member_id
                """)
                rows = cursor.fetchall()
                return [self._map_row(row) for row in rows]

    def update(
        self,
        member_id: int,
        full_name: str,
        email: str,
        join_date: date
    ) -> Optional[MemberRecord]:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    UPDATE library.members
                    SET full_name = %s,
                        email = %s,
                        join_date = %s
                    WHERE member_id = %s
                    RETURNING member_id, full_name, email, join_date
                """, (full_name, email, join_date, member_id))
                row = cursor.fetchone()
                return self._map_row(row) if row else None

    def delete(self, member_id: int) -> bool:
        with psycopg.connect(self.conn_string) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                    DELETE FROM library.members
                    WHERE member_id = %s
                    RETURNING member_id
                """, (member_id,))
                return cursor.fetchone() is not None