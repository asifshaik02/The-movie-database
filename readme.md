# The movie database

using [TMDB](https://www.themoviedb.org/)'s api made this movie database project.  

[Live demo](https://mmdb0.herokuapp.com/)

## setting up

**clone this repo:**

`git clone https://github.com/asifshaik02/The-movie-database.git`

`cd The-movie-database`

**creating virual environment:**

`virtualenv env`

for linux:
`source env/bin/activate`

for windows:
`\env\Scripts\activate.bat`

**Install requirements:**

`pip install -r requirements.txt`

**Api key:**

create an account in [TMDB](https://www.themoviedb.org/) and get an API key.

create a file named `.env` in that file enter:
`TMDB_API_KEY = <your_api_key>`

**Run on local server:**

`python app.py`