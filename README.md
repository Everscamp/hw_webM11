To ran your app simply run the main.py file
SQLALCHEMY_DATABASE_URL variable consist the credentials for your postgress db
As a db I used this conatiner 
docker run --name restapi-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

You can access the documentation by this route http://localhost:8000/docs after you start the Uvicorn web sever.