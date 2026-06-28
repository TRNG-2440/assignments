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
        return LoanResponse(loan_id=loan_id, book_id=l.book_id, member_id=l.member_id, loan_date=l.loan_date, due_date=l.due_date, return_date=None)

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
    def get_all_books():
        books = book.get_all()
        return [
            BookResponse(
                book_id=b[0],
                title=b[1],
                author=b[2],
                publication_year=b[3],
                genre_id=b[4],
                copy_count=b[5]
            )
            for b in books
        ]
     
    @app.get("/members", status_code=200, response_model=list[MemberResponse])
    def get_all_members():
        members = member.get_all()
        return [
            MemberResponse(
                member_id=m[0],
                full_name=m[1],
                email=m[2],
                join_date=m[3]
            )
            for m in members
        ]

    @app.get("/loans", status_code=200, response_model=list[LoanResponse])
    def get_all_loans():
        loans = loan.get_all()
        return [
            LoanResponse(
                loan_id=l[0],
                book_id=l[1],
                member_id=l[2],
                loan_date=l[3],
                due_date=l[4],
                return_date=l[5]
            )
            for l in loans
        ]

    @app.get("/genres/{genre_id}", status_code=200, response_model=GenreResponse)
    def get_one_genre(genre_id: int):
        g = genre.get_by_id(genre_id)
        if g is None:
            raise HTTPException(status_code=404, detail="Genre not found.")
        return GenreResponse(
            genre_id=g[0],
            name=g[1]
        )
    
    @app.get("/books/{book_id}", status_code=200, response_model=BookResponse)
    def get_one_book(book_id: int):
        b = book.get_by_id(book_id)
        if b is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        return BookResponse(
            book_id=b[0],
            title=b[1],
            author=b[2],
            publication_year=b[3],
            genre_id=b[4],
            copy_count=b[5]
        )
    
    @app.put("/genres/{genre_id}", status_code=201, response_model=GenreResponse)
    def replace_genre(genre_id: int, new_genre: GenreCreate):
        if genre.get_by_id(genre_id) is None:
            raise HTTPException(status_code=404, detail="Genre not found.")

        genre.update(
            genre_id,
            new_genre.name
        )
        
        return GenreResponse(
            genre_id=genre_id,
            name=new_genre.name
        )
    
    @app.put("/books/{book_id}", status_code=201, response_model=BookResponse)
    def replace_book(book_id: int, new_book: BookCreate):
        if book.get_by_id(book_id) is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        
        book.update(
            book_id,
            new_book.title,
            new_book.author,
            new_book.publication_year,
            new_book.genre_id,
            new_book.copy_count
        )

        return BookResponse(
            book_id=book_id,
            title=new_book.title,
            author=new_book.author,
            publication_year=new_book.publication_year,
            genre_id=new_book.genre_id,
            copy_count=new_book.copy_count
        )

    @app.patch("/genres/{genre_id}", status_code=200, response_model=GenreResponse)
    def update_genre(genre_id: int, updated: GenreUpdate):
        existing = genre.get_by_id(genre_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Genre not found.")
        
        name = updated.name if updated.name is not None else existing[1]

        genre.update(
            genre_id,
            name
        )

        return GenreResponse(
            genre_id=genre_id,
            name=name
        )
    
    @app.patch("/books/{book_id}", status_code=200, response_model=BookResponse)
    def update_book(book_id: int, updated: BookUpdate):
        existing = book.get_by_id(book_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Book not found.")
        
        title = updated.title if updated.title is not None else existing[1]
        author = updated.author if updated.author is not None else existing[2]
        publication_year = updated.publication_year if updated.publication_year is not None else existing[3]
        genre_id = updated.genre_id if updated.genre_id is not None else existing[4]
        copy_count = updated.copy_count if updated.copy_count is not None else existing[5]

        book.update(
            book_id,
            title,
            author,
            publication_year,
            genre_id,
            copy_count
        )

        return BookResponse(
            book_id=book_id,
            title=title,
            author=author,
            publication_year=publication_year,
            genre_id=genre_id,
            copy_count=copy_count
        )
    
    @app.delete("/genre/{genre_id}", status_code=204)
    def delete_genre(genre_id: int):
        if genre.get_by_id(genre_id) is None:
            raise HTTPException(status_code=404, detail="Genre not found.")
        
        genre.delete(genre_id)
