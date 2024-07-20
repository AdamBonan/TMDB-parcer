import sqlite3


class Database:

    def __init__(self, name_db):
        self.name_db = name_db
        self._create_tables()

    def _create_tables(self):
        conn = sqlite3.connect('movie.db')
        cursor = conn.cursor()

        # Create table movie
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                tmdb_id INTEGER PRIMARY KEY,
                tmdb_poster_path TEXT,
                genre_id INTEGER,
                title TEXT,
                production_company TEXT,
                vote REAL,
                release_date TEXT
            )
            ''')

        # Create table tv show
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv_shows (
                tmdb_id INTEGER PRIMARY KEY,
                tmdb_poster_path TEXT,
                genre_id INTEGER,
                title TEXT,
                production_company TEXT,
                vote REAL,
                season_air_date TEXT,
                number_of_seasons INTEGER,
                number_of_episodes INTEGER
            )
            ''')

        conn.commit()
        conn.close()

    def add_movie_data(self, movie_data: dict):
        conn = sqlite3.connect(f'{self.name_db}.db')
        cursor = conn.cursor()

        # Add main data
        cursor.execute('''
            INSERT OR IGNORE INTO movies (
                tmdb_id,
                tmdb_poster_path,
                genre_id,
                title,
                production_company,
                vote,
                release_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            movie_data.get("id", None),
            movie_data.get("poster_path", None),
            movie_data.get("genre_id", None),
            movie_data.get("title", None),
            movie_data.get("production_company", None),
            movie_data.get("vote_average", None),
            movie_data.get("release_date", None)
        ))

        conn.commit()
        conn.close()

    def add_tv_data(self, tv_data: dict):
        conn = sqlite3.connect(f'{self.name_db}.db')
        cursor = conn.cursor()

        # Add main data
        cursor.execute('''
            INSERT OR IGNORE INTO tv_shows (
                tmdb_id,
                tmdb_poster_path,
                genre_id,
                title,
                production_company,
                vote,
                season_air_date,
                number_of_seasons,
                number_of_episodes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            tv_data.get("id", None),
            tv_data.get("poster_path", None),
            tv_data.get("genre_id", None),
            tv_data.get("name", None),
            tv_data.get("production_company", None),
            tv_data.get("vote_average", None),
            tv_data.get("first_air_date", None),
            tv_data.get("number_of_seasons", None),
            tv_data.get("number_of_episodes", None)
        ))

        conn.commit()
        conn.close()


