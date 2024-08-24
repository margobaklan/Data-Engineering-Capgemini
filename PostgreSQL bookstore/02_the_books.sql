-- a CTE that identifies books whose titles contain the word "The" in any letter case using
-- RegEx. SELECT retrieves the book titles, corresponding authors, genre, and publication date.

with the_books as (
	SELECT
        b.book_id,
        b.title,
        b.published_date,
        aut.name AS author_name,
        gen.genre_name
    FROM
        books b
    JOIN
        authors aut ON b.author_id = aut.author_id
    JOIN
        genres gen ON b.genre_id = gen.genre_id
  	where
  		b.title ~* 'the'
  		
)
SELECT
    title,
    author_name,
    genre_name AS genre,
    published_date
FROM
    the_books;

