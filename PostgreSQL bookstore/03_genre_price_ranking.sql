-- ranks books by their price within each genre
-- the highest-priced book in each genre receiving a rank of 1.
SELECT
	title,
	genre_name,
  	price,
	RANK () OVER (
		PARTITION BY genre_id
		ORDER BY
			price
      	DESC
	)
FROM
	 books
INNER JOIN genres USING (genre_id);