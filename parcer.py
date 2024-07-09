import json
import argparse

from TMDB import Tmdb_API
from movies_db import Database


# Open config
with open('config.json') as file:
    config = json.load(file)

# Auth TMDB API
TOKEN = config.get("token", None)
tmdb = Tmdb_API(TOKEN)


def get_movie_ids(year: int, genre_ids: str = None, total_pages: int = 0) -> list[int]:
    if total_pages == 0:
        data_json = tmdb.discover_movie({
            "primary_release_year": year,
            "with_genres": genre_ids
        })
        total_pages = data_json.get("total_pages", 0)

    if total_pages > 500: total_pages = 500

    movies_ids = []
    for number_page in range(1, total_pages+1):
        results = tmdb.discover_movie({
            "primary_release_year": year,
            "with_genres": genre_ids,
            "page": number_page
        }).get("results")

        for movie in results:
            movies_ids.append(movie.get("id", 0))

    return movies_ids


def get_tv_ids(year: int, genre_ids: str = None, total_pages: int = 0) -> list[int]:
    if total_pages == 0:
        data_json = tmdb.discover_movie({
            "first_air_date_year": year,
            "with_genres": genre_ids
        }, tv=True)
        total_pages = data_json.get("total_pages", 0)

    tv_ids = []
    for number_page in range(1, total_pages+1):
        results = tmdb.discover_movie({
            "first_air_date_year": year,
            "with_genres": genre_ids,
            "page": number_page
        }, tv=True).get("results")

        for tv in results:
            tv_ids.append(tv.get("id", 0))

    return tv_ids


def main():

    # Argparce
    parser = argparse.ArgumentParser()

    parser.add_argument("release_date", type=int, help="The release date of the movie")
    parser.add_argument("-g", "--genre", type=str, help="The genre of the movie, Default = None", default=None, metavar="")
    parser.add_argument("-n", "--name", type=str, help="Name database, Default = movie", default="movie", metavar="")

    args = parser.parse_args()
    year = args.release_date
    name_db = args.name
    genre_ids = args.genre

    # Database
    genre_movie_list = tmdb.genres_movie_list().get("genres")
    genre_tv_list = tmdb.genres_movie_list(tv=True).get("genres")
    genre_configurations = genre_movie_list + genre_tv_list
    db = Database(name_db, genre_configurations)

    configuration_image = tmdb.configuration_details().get("images")
    movie_ids = get_movie_ids(year, genre_ids, total_pages=1)
    tv_ids = get_tv_ids(year, genre_ids, total_pages=1)

    # Movie id to data to database
    print(len(movie_ids))
    n = 0
    for movie_id in movie_ids:
        n += 1
        print(n)
        append_to_response = ['title', 'genres', 'poster_path', 'overview', 'release_date', 'production_countries','production_companies', 'releases', 'tagline', 'runtime']
        movie_data = tmdb.details_movie(movie_id, append_to_response=",".join(append_to_response))

        # Get poster url
        base_url = configuration_image.get("base_url", "http://image.tmdb.org/t/p/")
        poster_size = configuration_image.get("poster_sizes", "original")[-1]
        poster_path = movie_data.get("poster_path", "")
        movie_data["poster_path"] = f"{base_url}{poster_size}{poster_path}"

        # Get certification US
        certification = None
        for country in movie_data.get("releases").get("countries"):
            if country.get("iso_3166_1") == "US":
                certification = country.get("certification")
                break
        movie_data["certification"] = certification

        # Get country of original
        element = movie_data.get("origin_country")[0] if 0 <= 0 < len(movie_data.get("origin_country")) else None
        movie_data["origin_country"] = element

        # Cast, Director, Producer, Writer
        credit = tmdb.movie_credits(movie_id)

        producers, writers, directors = [], [], []
        for crew in credit.get("crew"):
            job = crew.get("job")

            # Director
            if job == "Director":
                directors.append(crew)
            # Producers
            elif job == "Producer" or job == "Associate Producer" or job == "Executive Producer":
                producers.append(crew)
            # Writer
            elif job == "Writer" or job == "Novel" or job =="Screenplay":
                writers.append(crew)

        movie_data["credits"] = {
            "cast": credit.get("cast")[:10],
            "crew": {
                "director": directors,
                "producers": producers,
                "writers": writers
            }
        }

        db.add_movie_data(movie_data)

    # Tv id to data
    for tv_id in tv_ids:
        append_to_response = ['title', 'genres', 'poster_path', 'overview', 'release_date', 'production_countries', 'production_companies', 'tagline', 'runtime']
        tv_data = tmdb.details_movie(tv_id, tv=True, append_to_response=",".join(append_to_response))

        # Get poster url
        base_url = configuration_image.get("base_url", "http://image.tmdb.org/t/p/")
        poster_size = configuration_image.get("poster_sizes", "original")[-1]
        poster_path = tv_data.get("poster_path", "")
        tv_data["poster_path"] = f"{base_url}{poster_size}{poster_path}"

        # Get certification US
        content_rating = tmdb.content_rating(tv_id)
        certification = None
        for country in content_rating.get("results"):
            if country.get("iso_3166_1") == "US":
                certification = country.get("rating")
                break
        tv_data["certification"] = certification

        # Get country of original
        element = tv_data.get("origin_country")[0] if 0 <= 0 < len(tv_data.get("origin_country")) else None
        tv_data["origin_country"] = element

        # Cast, Director, Producer, Writer
        credit = tmdb.movie_credits(tv_id, tv=True)

        producers, writers, directors = [], [], []
        for crew in credit.get("crew"):
            job = crew.get("job")

            # Director
            if job == "Director":
                directors.append(crew)
            # Producers
            elif job == "Producer" or job == "Associate Producer" or job == "Executive Producer":
                producers.append(crew)
            # Writer
            elif job == "Writer" or job == "Novel" or job == "Screenplay":
                writers.append(crew)

        tv_data["credits"] = {
            "cast": credit.get("cast")[:10],
            "crew": {
                "director": directors,
                "producers": producers,
                "writers": writers
            }
        }

        # Add episodes in season
        for season in tv_data.get("seasons"):
            season_number = season.get("season_number")
            episodes = tmdb.tv_series_details(tv_id, season_number).get("episodes")
            season["episodes"] = episodes

        db.add_tv_data(tv_data)
        n += 1
        print(n)


if __name__ == "__main__":
    main()