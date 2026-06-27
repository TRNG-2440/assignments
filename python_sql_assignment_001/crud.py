from models import *
from fastapi import HTTPException

def endpoints(app, genre, book, member, loan):
    @app.post("/genres", status_code=201, response_model=GenreResponse)
    def create_genre(g: GenreCreate):
        genre_id = genre.create(g.name)
        return GenreResponse(genre_id=genre_id, name=g.name)
    
    @app.post("/books", status_code=201, response_model=BookResponse)
    def create_book(b: BookCreate):
        book_id = book.create(b.title, b.author, b.publication_year, b.genre_id, b.copy_count)
        return BookResponse(book_id=book_id, title=b.title, author=b.author, publication_year=b.publication_year, genre_id=b.genre_id, copy_count=b.copy_count)
     
    @app.post("/members", status_code=201, response_model=MemberResponse)
    def create_member(m: MemberCreate):
        member_id = member.create(m.full_name, m.email, m.join_date)
        return MemberResponse(member_id=member_id, full_name=m.full_name, email=m.email, join_date=m.join_date)
        
    @app.post("/loans", status_code=201, response_model=LoanResponse)
    def create_loan(l: LoanCreate):   
        loan_id = loan.create(l.book_id, l.member_id, l.loan_date, l.due_date)
        return LoanResponse(loan_id=loan_id, book_id=l.book_id, member_id=l.member_id, loan_date=l.loan_date, due_date=l.due_date)

    @app.get("/genres", status_code=200, response_model=list[GenreResponse])
    def get_all_genres():
        genres = genre.get_all()
        return [
            GenreResponse(
                genre_id=g[0], 
                name=g[1]
            )
            for g in genres
        ]
    
    @app.get("/books", status_code=200, response_model=list[BookResponse])

     
    @app.get("/members", status_code=200, response_model=list[MemberResponse])
        
    @app.get("/loans", status_code=200, response_model=list[LoanResponse])
