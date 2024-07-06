from TMDB import Tmdb_API
import json

# Open config
with open('config.json') as file:
    config = json.load(file)

TOKEN = config.get("token", None)
tmdb = Tmdb_API(TOKEN)


def get_movie(year: int, genre_ids: str) -> list[dict]:
    data_json = tmdb.discover_movie({
        "primary_release_year": year,
        "with_genres": genre_ids
    })
    total_pages = data_json.get("total_pages", 0)

    movies = data_json.get("results")
    for number_page in range(2, total_pages+1):
        results = tmdb.discover_movie({
            "primary_release_year": year,
            "with_genres": genre_ids,
            "page": number_page
        }).get("results")

        movies += results

    return movies


def main():

    year = 1999
    genre_ids = "18,19"

    data = get_movie(year, genre_ids)


if __name__ == "__main__":
    main()