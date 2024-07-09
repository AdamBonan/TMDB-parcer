import requests


class Tmdb_API:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }

        self._authentication()

    def _authentication(self):
        url = f"{self.BASE_URL}/authentication"
        data_json = requests.get(url, headers=self.headers).json()

        if not data_json.get("success", False):
            status_message = data_json.get("status_message", data_json)
            raise ValueError(status_message)

    def configuration_details(self):
        url = f"{self.BASE_URL}/configuration"
        response = requests.get(url, headers=self.headers)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def discover_movie(self,
                       params: dict,
                       tv: bool = False) -> dict:
        if tv:
            url = f"{self.BASE_URL}/discover/tv"
        else:
            url = f"{self.BASE_URL}/discover/movie"

        response = requests.get(url, headers=self.headers, params=params)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def details_movie(self,
                      movie_id: int,
                      tv: bool = False,
                      append_to_response: str = None) -> dict:
        if tv:
            url = f"{self.BASE_URL}/tv/{movie_id}"
        else:
            url = f"{self.BASE_URL}/movie/{movie_id}"

        response = requests.get(url, headers=self.headers, params={"append_to_response": append_to_response})
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def movie_credits(self,
                      movie_id: int,
                      tv: bool = False) -> dict:
        if tv:
            url = f"{self.BASE_URL}/tv/{movie_id}/credits"
        else:
            url = f"{self.BASE_URL}/movie/{movie_id}/credits"

        response = requests.get(url, headers=self.headers)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def content_rating(self, series_id):
        url = f"{self.BASE_URL}/tv/{series_id}/content_ratings"

        response = requests.get(url, headers=self.headers)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def tv_series_details(self,
                          series_id: int,
                          season_number: int):
        url = f"{self.BASE_URL}/tv/{series_id}/season/{season_number}"

        response = requests.get(url, headers=self.headers)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")

    def genres_movie_list(self, tv: bool = False):
        if tv:
            url = f"{self.BASE_URL}/genre/tv/list"
        else:
            url = f"{self.BASE_URL}/genre/movie/list"

        response = requests.get(url, headers=self.headers)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            status_message = data_json.get("status_message", data_json)
            status_code = data_json.get("status_code", "unknown")
            raise ValueError(f"{status_message}. Status code: {status_code}")