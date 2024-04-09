import aiohttp
import json


class FilmJournalist:

    def __init__(self, api_key: str):
        self.base_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}'
        self.session = None

    async def session_start(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def session_close(self) -> None:
        if self.session:
            await self.session.close()

    async def get_movie_score(self, movie_title: str):
        url = f'{self.base_url}&query={movie_title}'
        movies = []
        async with self.session.get(url) as request:
            if request.status == 200:
                response = await request.text()
                results = json.loads(response)['results']
                for result in results[:3]:
                    movie = {"name": result["original_title"], "date": result["release_date"], "rating": result["vote_average"]}
                    movies.append(movie)
        return movies




