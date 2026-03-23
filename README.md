# Hocamı Yıldızla (Rate My Professor)

#### Video Demo: [YOUR_VIDEO_URL_HERE]

## Description:

Hocamı Yıldızla is a web app that allows university students to search for their professors, view ratings and comments from other students, and contribute their own ratings and comments. The name translates to "Rate My Professor" in Turkish, and the entire interface is in Turkish to target Turkish speaking university students.

My motivation behind this project came from wanting to create a localized version of rate my professor platforms specifically for Yildiz Technichal University. Students often rely on word of mouth or social media groups to learn about professors before enrolling in courses or choosing to make a project with a professor. This application provides a centralized, structured platform where students can make more informed decisions about their course selections.

## Project Files

#### app.py

This is the main Flask application file that contains all the route handlers and core logic. The application uses Flask's built in templating system with Jinja2 and implements several key routes:

- `/` (index): The homepage route initializes the database tables if they don't already exist. It creates two tables: "hocalar" (professors) for storing professor information including name, average rating, and number of submissions, and "comments" for storing student comments linked to specific professors via a foreign key relationship.

- `/search`: Handles professor search functionality. It accepts a query "hoca_adi" (professor name), performs a case-insensitive partial match search using SQL's `LIKE` operator, and returns all matching results to the search results template.

- `/result`: Displays information for a specific professor, including their average rating and all comments. This route fetches data from both the "hocalar" and "comments" tables using the professor's ID. If an invalid ID is provided, it flashes an error message and redirects to a page that shows all professors.

- `/rate`: Processes rating submissions via POST request. This route implements a weighted average calculation to update professor ratings. It retrieves the current average rating and submission count, calculates the new average, and updates the hocalar table. It ensures ratings are between 1 and 5.

- `/comment`: Handles comment submissions. It validates that the comment isn't empty, inserts it into the database linked to the correct professor ID, and flashes success/failure messages.

- `/add`: Allows users to add new professors to the database. It first checks if the professor already exists to prevent duplicates, then either creates a new entry or returns the existing professor's `result` page. The name is stored in lowercase to ensure consistency in searches.

The application uses Flask's flash messaging system extensively to provide user feedback for successful operations and errors. All database operations properly commit changes and close connections to prevent resource leaks.

#### helpers.py

This File contains only one function for now, specifically the database connection function `get_db()`. I chose to separate this into its own file to follow the principle of separation of concerns and make the code more modular.

The function gets the PostgreSQL database URL from environment variables and makes a connection using the psycopg2 library. I configured it to use `RealDictCursor`, which returns query results as dictionaries rather than tuples. This choice makes the code more readable and maintainable because I can access columns by name (e.g. result['name']) rather than by index, which makes coding and debugging easier/

#### Templates Folder

The templates folder contains all the Jinja2 HTML templates used for rendering pages. I used Bootstrap 5 for the majority of styling to ensure a responsive, mobile-friendly design without writing extensive custom CSS. The templates include:

- layout.html: A base template that defines the common structure (navbar, CSS animations etc.) that other templates extend
- index.html: The homepage with a search form
- search.html: Displays search results, has a form to add a new professor for when a user doesn't find a given professor
- result.html: Shows professor's average rating and comments with forms for rating and commenting

I chose Bootstrap because it gives a nice appearance with minimal effort, allowing me to focus on functionality rather than spending extensive time on visual design. The small amount of custom CSS was used only for minor tweaks to spacing and alignment.

#### Database Design

The application uses PostgreSQL as its database, which I chose over SQLite for several reasons. First, PostgreSQL is required for deployment on platforms like Render, where the application is hosted. Second, it provides better concurrent access handling, which is important for a multi-user web application. Finally, PostgreSQL offers more robust data types and constraints.

The database schema consists of two tables:

1. `hocalar` (professors): Stores professor names, their average ratings (as floats), and the number of rating submissions. The submissions count is necessary for calculating accurate weighted averages when new ratings are added.

2. `comments`: Stores student comments with a foreign key reference to the professor's ID. This creates a one-to-many relationship where each professor can have multiple comments.


The project taught me valuable lessons about full-stack web development, databases, deployment, and the importance of user feedback in interface design. The experience of taking an application from localhost to deployment was educational and highlighted the differences between development and production environments.
