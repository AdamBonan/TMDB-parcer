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

    def discover_movie(self, params: dict) -> dict:
        url = f"{self.BASE_URL}/discover/movie"
        response = requests.get(url, headers=self.headers, params=params)
        data_json = response.json()

        if response.ok:
            return data_json
        else:
            raise ValueError(data_json.get("status_message", data_json))

