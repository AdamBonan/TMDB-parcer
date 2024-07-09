import sqlite3


class Database:

    def __init__(self, name_db, genre_configurations):
        self.name_db = name_db

        self._create_tables()
        self._add_genre_configurations(genre_configurations)

    def _create_tables(self):
        conn = sqlite3.connect('movie.db')
        cursor = conn.cursor()

        # Create table movie
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY,
                title TEXT,
                release_date TEXT,
                overview TEXT,
                poster_path TEXT,
                runtime INTEGER,
                certification TEXT,
                origin_country TEXT,
                tagline TEXT,
                vote_average REAL
            )
            ''')

        # Create table tv show
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv_shows (
                series_id INTEGER PRIMARY KEY,
                title TEXT,
                release_date TEXT,
                overview TEXT,
                poster_path TEXT,
                certification TEXT,
                origin_country TEXT,
                tagline TEXT,
                vote_average REAL,
                "number_of_seasons" INTEGER,
                "number_of_episodes" INTEGER
            )
            ''')

        # Create companies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY,
                name TEXT,
                origin_country TEXT
            )
            ''')

        # production_companies_movies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_companies_movies (
                company_id INTEGER,
                movie_id INTEGER,
                FOREIGN KEY (company_id) REFERENCES companies (company_id),
                FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
                PRIMARY KEY (company_id, movie_id)
            )
            ''')

        # production_companies_tv_shows
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_companies_tv_shows (
                company_id INTEGER,
                series_id INTEGER,
                FOREIGN KEY (company_id) REFERENCES companies (company_id),
                FOREIGN KEY (series_id) REFERENCES tv_shows (series_id),
                PRIMARY KEY (company_id, series_id)
            )
            ''')

        # Create table genres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                genre_id INTEGER PRIMARY KEY,
                name TEXT
            )
            ''')

        # movie_genres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movie_genres (
                movie_id INTEGER,
                genre_id INTEGER,
                FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres (genre_id),
                PRIMARY KEY (movie_id, genre_id)
            )
            ''')

        # tv_show_genres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv_show_genres (
                series_id INTEGER,
                genre_id INTEGER,
                FOREIGN KEY (series_id) REFERENCES tv_shows (series_id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres (genre_id),
                PRIMARY KEY (series_id, genre_id)
            )
            ''')

        # Create table seasons
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seasons (
                season_id INTEGER PRIMARY KEY,
                series_id INTEGER,
                season_title TEXT,
                air_date TEXT,
                overview TEXT,
                episode_count INTEGER,
                season_number INTEGER,
                vote_average INTEGER,
                FOREIGN KEY (series_id) REFERENCES tv_shows(series_id)
            )
            ''')

        # Create table episodes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                episode_id INTEGER PRIMARY KEY,
                season_id INTEGER,
                episode_title TEXT,
                air_date TEXT,
                overview TEXT,
                episode_number INTEGER,
                runtime INTEGER,
                vote_average INTEGER,
                FOREIGN KEY (season_id) REFERENCES seasons(season_id)
            )
            ''')

        conn.commit()
        conn.close()

    def _add_genre_configurations(self, genre_configurations):
        conn = sqlite3.connect(f'{self.name_db}.db')
        cursor = conn.cursor()

        for genre in genre_configurations:
            cursor.execute('''
                INSERT OR IGNORE INTO genres (
                genre_id,
                name
                ) VALUES (?, ?)
            ''', (genre['id'], genre['name']))

        conn.commit()
        conn.close()

    def add_movie_data(self, movie_data: dict):
        conn = sqlite3.connect(f'{self.name_db}.db')
        cursor = conn.cursor()

        # Add main data
        cursor.execute('''
            INSERT OR IGNORE INTO movies (
            movie_id,
            title,
            release_date,
            overview,
            poster_path,
            runtime,
            certification,
            origin_country,
            tagline,
            vote_average
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            movie_data.get("id"),
            movie_data.get("title"),
            movie_data.get("release_date"),
            movie_data.get("overview"),
            movie_data.get("poster_path"),
            movie_data.get("runtime"),
            movie_data.get("certification"),
            movie_data.get("origin_country"),
            movie_data.get("tagline"),
            movie_data.get("vote_average")
        ))

        # Add genre
        for genre in movie_data.get("genres"):
            cursor.execute("""
            INSERT OR IGNORE INTO movie_genres (
               movie_id,
               genre_id 
            ) VALUES (?, ?)
            """, (
                movie_data.get("id"),
                genre.get("id")
            ))

        # Add companies
        for company in movie_data.get("production_companies"):
            cursor.execute("""
            INSERT OR IGNORE INTO companies (
                company_id,
                name,
                origin_country    
            ) VALUES (?, ?, ?)""", (
                company.get("id"),
                company.get("name"),
                company.get("origin_country")
            ))

            cursor.execute("""
            INSERT OR IGNORE INTO production_companies_movies (
                company_id,
                movie_id
            ) VALUES (?, ?)""", (
                company.get("id"),
                movie_data.get("id")
            ))

        conn.commit()
        conn.close()

    def add_tv_data(self, tv_data: dict):
        conn = sqlite3.connect(f'{self.name_db}.db')
        cursor = conn.cursor()

        # Add main data
        cursor.execute('''
            INSERT OR IGNORE INTO tv_shows (
                series_id,
                title,
                release_date,
                overview,
                poster_path,
                certification,
                origin_country,
                tagline,
                vote_average,
                number_of_seasons,
                number_of_episodes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            tv_data.get("id"),
            tv_data.get("name"),
            tv_data.get("first_air_date"),
            tv_data.get("overview"),
            tv_data.get("poster_path"),
            tv_data.get("certification"),
            tv_data.get("origin_country"),
            tv_data.get("tagline"),
            tv_data.get("vote_average"),
            tv_data.get("number_od_seasons"),
            tv_data.get("number_of_episodes")
        ))

        # Add genre
        for genre in tv_data.get("genres"):
            cursor.execute("""
                INSERT OR IGNORE INTO tv_show_genres (
                    series_id,
                    genre_id 
                ) VALUES (?, ?)
                """, (
                tv_data.get("id"),
                genre.get("id")
            ))

        # Add companies
        for company in tv_data.get("production_companies"):
            cursor.execute("""
                INSERT OR IGNORE INTO companies (
                    company_id,
                    name,
                    origin_country    
                ) VALUES (?, ?, ?)""", (
                company.get("id"),
                company.get("name"),
                company.get("origin_country")
            ))

            cursor.execute("""
                INSERT OR IGNORE INTO production_companies_tv_shows (
                    company_id,
                    series_id
                ) VALUES (?, ?)""", (
                company.get("id"),
                tv_data.get("id")
            ))

        # Add season and epizodes
        for season in tv_data.get("seasons"):
            cursor.execute("""
            INSERT OR IGNORE INTO seasons (
                 season_id,
                 series_id,
                 season_title,
                 air_date,
                 overview,
                 episode_count,
                 season_number,
                 vote_average   
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
                season.get("id"),
                tv_data.get("id"),
                season.get("name"),
                season.get("air_date"),
                season.get("overview"),
                season.get("episode_count"),
                season.get("season_number"),
                season.get("vote_average")
            ))

            # episodes in season
            for episode in season.get("episodes"):
                cursor.execute("""
                INSERT OR IGNORE INTO episodes (
                    episode_id,
                    season_id,
                    episode_title,
                    air_date,
                    overview,
                    episode_number,
                    runtime,
                    vote_average
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
                    episode.get("id"),
                    season.get("id"),
                    episode.get("name"),
                    episode.get("air_date"),
                    episode.get("overview"),
                    episode.get("episode_number"),
                    episode.get("runtime"),
                    episode.get("vote_average")
                ))

        conn.commit()
        conn.close()

