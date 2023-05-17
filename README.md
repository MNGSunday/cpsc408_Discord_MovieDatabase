# cpsc408_Discord_MovieDatabase
## Submission Info
### Group members:
- Christopher Youn, Student ID:
- Gabriel Garcia, Student ID:
- Connor Martindale, Student ID:
- Marc Domingo, Student ID: 2346778
### Course Info:
- Course: CPSC 408-01
- Assignment: Final Project

## Set Up

**NOTE: It takes a bit of work to set up everything**

1. Create discord bot in discord developer dashboard and invite bot to your server
2. Check out `CONTRIBUTING.md` to set up environment
3. Start up mysql server and create MovieBot database in mysql shell

```shell
mysql> create database MovieBot;
mysql> use MovieBot;
```

4. load MovieBot database

```shell
mysql> source ./dump.sql
```

5. Run `src/bot.py`
6. Run commands in discord

## Requirements

We explicitly defined how we satisfied the requirements for easy grading.

1. Print/display records from your database/tables.

One example of many:

```python
# src/moviebot/dao/movies_dao.py
def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Movie]:
    with self.db.cursor(named_tuple=True) as cursor:
        cursor.execute(
            "SELECT * FROM movies_with_director_composer_studio ORDER BY movieID LIMIT %s, %s;",
            (offset, limit),
        )
        return PaginatedData[Movie](
            data=[
                Movie.from_named_tuple(movie_named_tuple)
                for movie_named_tuple in cursor.fetchall()
            ],
            offset=offset,
            limit=limit,
            total=self.count(),
            paginate=self.list,
        )
```

Accessed through frontend through `/list movies` command

2. Query for data/results with various parameters/filters

```python
# src/moviebot/dao/movies_dao.py
def get_movies(
    self,
    genre: str = None,
    min_budget: int = 0,
    max_budget: int = 2147483647,
    min_critic_score: int = 0,
    max_critic_score: int = 100,
    min_viewer_score: int = 0,
    max_viewer_score: int = 100,
    offset: int = 0,
    limit: int = 5,
) -> PaginatedData[Movie]:
    with self.db.cursor(named_tuple=True) as cursor:
        filters = [
            "budget >= %s",
            "budget <= %s",
            "criticScore >= %s",
            "criticScore <= %s",
            "viewerScore >= %s",
            "viewerScore <= %s",
        ]
        filter_values: List[Any] = [
            min_budget,
            max_budget,
            min_critic_score,
            max_critic_score,
            min_viewer_score,
            max_viewer_score,
        ]
        if genre is not None:
            filters.append("genre = %s")
            filter_values.append(genre)

        cursor.execute(
            f"SELECT COUNT(*) as total FROM movies_with_director_composer_studio WHERE {' AND '.join(filters)} ORDER BY movieID;",
            filter_values,
        )
        res = cursor.fetchone()
        if res is None:
            raise ValueError("No count returned")
        total = res.total

        cursor.execute(
            f"SELECT * FROM movies_with_director_composer_studio WHERE {' AND '.join(filters)} ORDER BY movieID;",
            filter_values,
        )
        return PaginatedData[Movie](
            data=[
                Movie.from_named_tuple(movie_named_tuple)
                for movie_named_tuple in cursor.fetchall()
            ],
            offset=offset,
            limit=limit,
            total=total,
            paginate=lambda offset, limit: self.get_movies(genre, offset, limit),
        )
```

Accessed through frontend through `/recommendMovies by_filters <genre> <minBudget> <maxBudget> <minCriticScore> <maxCriticScore> <minViewerScore> <maxViewerScore>`

Note: arguments above are optional

3. Create a new record

```python
# src/moviebot/dao/reviews_dao.py
def create(self, username: str, movie_id: int, score: int, text: str):
    with self.db.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO Reviews (username, movieID, score, text, deleted) VALUES (%s, %s, %s, %s, %s);",
                (username, movie_id, score, text, 0),
            )
            cursor.execute(
                "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                (
                    username,
                    "Insert",
                    f"Inserted review with id: {cursor.lastrowid}",
                ),
            )
            self.db.commit()
        except mysql.connector.Error as error:
            self.db.rollback()
            raise RuntimeError("Couldn't insert review and rolled back: ", error)
        if cursor.lastrowid is None:
            raise ValueError("Couldn't fetch last inserted movie review")
        return Review(
            review_id=cursor.lastrowid,
            username=username,
            movie_id=movie_id,
            score=score,
            text=text,
            deleted=False,
        )
```

Accessed through frontend through `/create review <movieID> <score> <text>`

4. Delete records (soft delete function would be ideal)

```python
# src/moviebot/dao/reviews_dao.py
def delete(self, username: str, review_id: int) -> None:
    with self.db.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE Reviews SET deleted = 1 WHERE reviewID = %s AND deleted = 0;",
                (review_id,),
            )
            cursor.execute(
                "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                (
                    username,
                    "Delete",
                    f"Deleted review with id: {review_id}",
                ),
            )
            self.db.commit()
        except mysql.connector.Error as error:
            self.db.rollback()
            raise RuntimeError("Couldn't delete review and rolled back: ", error)
```

Accessed through frontend through `/delete review <reviewId>`

5. Update records

```python
# src/moviebot/dao/reviews_dao.py
def update(self, username: str, review_id: int, new_text: str):
    with self.db.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE Reviews SET text = %s WHERE reviewID = %s AND deleted = 0;",
                (new_text, review_id),
            )
            cursor.execute(
                "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                (
                    username,
                    "Update",
                    f"Updated review with id: {cursor.lastrowid}",
                ),
            )
            self.db.commit()
        except mysql.connector.Error as error:
            self.db.rollback()
            raise RuntimeError("Couldn't update review and rolled back: ", error)
        updated_review = self.get_by_id(review_id)
        if updated_review is None:
            raise ValueError(f"Couldn't fetch updated review with id {review_id}")
        return updated_review
```

Accessed through frontend through `/update review <reviewId> <newText>`

6. Make use of transactions (commit & rollback)

All write operations use transactions to also write to the log table.

```python
# src/moviebot/dao/reviews_dao.py
def update(self, username: str, review_id: int, new_text: str):
    with self.db.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE Reviews SET text = %s WHERE reviewID = %s AND deleted = 0;",
                (new_text, review_id),
            )
            cursor.execute(
                "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                (
                    username,
                    "Update",
                    f"Updated review with id: {cursor.lastrowid}",
                ),
            )
            self.db.commit()
        except mysql.connector.Error as error:
            self.db.rollback()
            raise RuntimeError("Couldn't update review and rolled back: ", error)
        updated_review = self.get_by_id(review_id)
        if updated_review is None:
            raise ValueError(f"Couldn't fetch updated review with id {review_id}")
        return updated_review
```

7. Generate reports that can be exported (excel or csv format)

```python
# src/moviebot/commands/export.py
async def export(self, ctx: discord.ApplicationContext, entity: str):
    data = None

    if entity == "movies":
        data = self.bot.movies_dao.list(limit=1000)
    elif entity == "actors":
        data = self.bot.actors_dao.list(limit=1000)
    elif entity == "directors":
        data = self.bot.directors_dao.list(limit=1000)
    elif entity == "composers":
        data = self.bot.composers_dao.list(limit=1000)
    elif entity == "songs":
        data = self.bot.songs_dao.list(limit=1000)
    elif entity == "studios":
        data = self.bot.studios_dao.list(limit
```
