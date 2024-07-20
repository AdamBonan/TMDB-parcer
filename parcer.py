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


def main(year, name_db, genre_ids):

    # Database
    db = Database(name_db)

    # Base configuration image
    configuration_image = tmdb.configuration_details().get("images")
    base_url_image = configuration_image.get("base_url", "http://image.tmdb.org/t/p/")
    base_poster_size = configuration_image.get("poster_sizes", "original")[-1]

    movie_ids = get_movie_ids(year, genre_ids)
    tv_ids = get_tv_ids(year, genre_ids)

    # Movie id to data to database
    for movie_id in movie_ids:
        # Get movie data
        append_to_response = ['title', 'genres', 'poster_path', 'release_date', 'releases']
        movie_data = tmdb.details_movie(movie_id, append_to_response=",".join(append_to_response))

        # Get poster url
        poster_path = movie_data.get("poster_path", "")
        movie_data["poster_path"] = f"{base_url_image}{base_poster_size}{poster_path}"

        # Get genre_id
        if not movie_data.get("genres", []):
            movie_data["genre_id"] = None
        else:
            movie_data["genre_id"] = movie_data.get("genres")[0].get("id", None)

        # Get production_company
        details_movie = tmdb.details_movie(movie_id)
        if not details_movie.get("production_companies", []):
            movie_data["production_company"] = None
        else:
            movie_data["production_company"] = details_movie.get("production_companies")[0].get("name", None)

        db.add_movie_data(movie_data)

    # Tv id to data
    for tv_id in tv_ids:
        # Get tv data
        append_to_response = ['title', 'genres', 'poster_path', 'release_date', 'production_companies']
        tv_data = tmdb.details_movie(tv_id, tv=True, append_to_response=",".join(append_to_response))

        # Get poster url
        poster_path = tv_data.get("poster_path", "")
        tv_data["poster_path"] = f"{base_url_image}{base_poster_size}{poster_path}"

        # Get genre_id
        if not tv_data.get("genres", []):
            tv_data["genre_id"] = None
        else:
            tv_data["genre_id"] = tv_data.get("genres")[0].get("id", None)

        # Get production_company, number_of_seasons, number_of_episodes
        details_tv = tmdb.details_movie(tv_id, tv=True)

        if not details_tv.get("production_companies", []):
            tv_data["production_company"] = None
        else:
            tv_data["production_company"] = details_tv.get("production_companies")[0].get("name")

        tv_data["number_of_seasons"] = details_tv.get("number_of_seasons", None)
        tv_data["number_of_episodes"] = details_tv.get("number_of_episodes", None)

        db.add_tv_data(tv_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("release_date", type=int, help="The release date of the movie")
    parser.add_argument("-g", "--genre", type=str, help="The genre of the movie, Default = None", default=None, metavar="")
    parser.add_argument("-n", "--name", type=str, help="Name database, Default = movie", default="movie", metavar="")
    args = parser.parse_args()

    main(args.release_date, args.name, args.genre)