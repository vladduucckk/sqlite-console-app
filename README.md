# sqlite-console-app
This repository contains a console application for managing the “movie_base” database using SQLite. 
Features

## 1. Database Structure

The application includes three main tables in the SQLite database:

	•	Movies Table (movies):
	•	id (INTEGER, PRIMARY KEY): Unique identifier for each movie.
	•	title (TEXT): The title of the movie.
	•	release_year (INTEGER): The year the movie was released.
	•	genre (TEXT): The genre of the movie.
	•	Actors Table (actors):
	•	id (INTEGER, PRIMARY KEY): Unique identifier for each actor.
	•	name (TEXT): The name of the actor.
	•	birth_year (INTEGER): The year the actor was born.
	•	Movie Cast Table (movie_cast):
	•	movie_id (INTEGER, FOREIGN KEY): ID of the movie.
	•	actor_id (INTEGER, FOREIGN KEY): ID of the actor.
	•	Primary Key: Combination of movie_id and actor_id to create a many-to-many relationship between movies and actors.
---
## 2. Core Functionalities

	•	Add New Records:
	•	Users can add new movies and actors to the database.
	•	When adding a new movie, users can also specify the actors who appeared in it, utilizing the movie_cast table to create the many-to-many relationship.
---
## 3. SQL Queries

	•	JOIN Query: Displays a list of movies along with the names of all actors who starred in each movie. This query uses an INNER JOIN between the movies, movie_cast, and actors tables.
	•	DISTINCT Query: Retrieves a unique list of movie genres without repetitions using the DISTINCT keyword.
	•	Aggregate Functions:
	•	Count Query: Counts the number of movies for each genre using the COUNT function.
	•	Average Query: Finds the average birth year of actors who appeared in movies of a specific genre using the AVG function.
	•	LIKE Query: Searches for movies by a keyword in the title using the LIKE operator for partial string matching.
	•	LIMIT and OFFSET: Implements pagination for movie listings, allowing users to view a limited number of movies with the ability to skip records using OFFSET.
	•	UNION Query: Combines the names of all actors and titles of all movies into one result using the UNION operator.
	•	FOREIGN KEY Query: Establishes relationships between the movies and actors tables via the movie_cast table using foreign keys.
---
## 4. Custom SQLite Function

	•	movie_age(): This custom SQLite function calculates how many years have passed since a movie was released. It takes the release year as an argument and returns the number of years relative to the current year.
---
## Setup

To run the application, you need to:

	1.	Clone this repository.
	2.	Install SQLite if not already installed.
	3.	Run the Python script that initializes the SQLite database and starts the console interface.
---
## Usage

Upon launching the console application, you can:

	•	Add new movies and actors.
	•	View movies with actor details using advanced SQL queries.
	•	Search for movies based on a keyword.
	•	Analyze the data using aggregate functions and custom queries.
