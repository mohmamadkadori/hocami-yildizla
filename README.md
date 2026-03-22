# Hocamı Yıldızla (Rate My Professor)

#### Video Demo: [YOUR_VIDEO_URL_HERE]

#### Description:

**Hocamı Yıldızla** is a web application that allows university students to search for their professors, view ratings and comments from other students, and contribute their own ratings and feedback. The name translates to "Rate My Professor" in Turkish, and the entire interface is in Turkish to serve Turkish-speaking university students.

The motivation behind this project came from wanting to create a localized version of rate-my-professor platforms specifically for Turkish universities. Students often rely on word-of-mouth or informal social media groups to learn about professors before enrolling in courses. This application provides a centralized, structured platform where students can make more informed decisions about their course selections.

## Project Files

### app.py

This is the main Flask application file that contains all the route handlers and core logic. The application uses Flask's built-in templating system with Jinja2 and implements several key routes:

- **`/` (index)**: The homepage route initializes the database tables if they don't already exist. It creates two tables: `hocalar` (professors) for storing professor information including name, average rating, and number of submissions, and `comments` for storing student comments linked to specific professors via a foreign key relationship.

- **`/search`**: Handles professor search functionality. It accepts a query parameter `hoca_adi` (professor name), performs a case-insensitive partial match search using SQL's `LIKE` operator, and returns all matching results to the search results template.

- **`/result`**: Displays detailed information for a specific professor, including their current rating and all comments. This route fetches data from both the `hocalar` and `comments` tables using the professor's ID. If an invalid ID is provided, it flashes an error message and redirects back to search.

- **`/rate`**: Processes rating submissions via POST request. This route implements a weighted average calculation to update professor ratings. It retrieves the current average rating and submission count, calculates the new average using the formula `(avgRating × submissions + newRating) / (submissions + 1)`, and updates the database. Input validation ensures ratings are between 1 and 5.

- **`/comment`**: Handles comment submissions. It validates that the comment isn't empty, inserts it into the database linked to the correct professor ID, and provides user feedback through flash messages.

- **`/add`**: Allows users to add new professors to the database. It first checks if the professor already exists to prevent duplicates, then either creates a new entry or returns the existing professor's page. The name is stored in lowercase to ensure consistency in searches.

The application uses Flask's flash messaging system extensively to provide user feedback for successful operations and validation errors. All database operations properly commit changes and close connections to prevent resource leaks.

### helpers.py

This module contains utility functions, specifically the database connection function `get_db()`. I chose to separate this into its own file to follow the principle of separation of concerns and make the code more modular.

The function retrieves the PostgreSQL database URL from environment variables and establishes a connection using the `psycopg2` library. I specifically configured it to use `RealDictCursor`, which returns query results as dictionaries rather than tuples. This design choice makes the code more readable and maintainable because I can access columns by name (e.g., `result['name']`) rather than by index (e.g., `result[0]`), which is less error-prone and more self-documenting.

### Templates Folder

The templates folder contains all the Jinja2 HTML templates used for rendering pages. I used Bootstrap 5 for the majority of styling to ensure a responsive, mobile-friendly design without writing extensive custom CSS. The templates include:

- **layout.html**: A base template that defines the common structure (navbar, footer, flash message display) that other templates extend
- **index.html**: The homepage with a search form and a form to add new professors
- **search.html**: Displays search results in a clean, organized format
- **result.html**: Shows detailed professor information with forms for rating and commenting

I chose Bootstrap because it provides a professional appearance with minimal effort, allowing me to focus on functionality rather than spending extensive time on visual design. The small amount of custom CSS was used only for minor tweaks to spacing and alignment.

### Database Design

The application uses PostgreSQL as its database, which I chose over SQLite for several reasons. First, PostgreSQL is required for deployment on platforms like Render, where the application is hosted. Second, it provides better concurrent access handling, which is important for a multi-user web application. Finally, PostgreSQL offers more robust data types and constraints.

The database schema consists of two tables:

1. **hocalar** (professors): Stores professor names, their average ratings (as floats), and the number of rating submissions. The submissions count is necessary for calculating accurate weighted averages when new ratings are added.

2. **comments**: Stores student comments with a foreign key reference to the professor's ID. This creates a one-to-many relationship where each professor can have multiple comments.

## Design Decisions

**Weighted Average for Ratings**: Instead of recalculating the average from all individual ratings stored in the database, I implemented an incremental weighted average calculation. This is more efficient because it only requires storing the current average and count, rather than every individual rating. The tradeoff is that we can't later analyze the distribution of ratings, but for this application's scope, the efficiency gain was worth it.

**Turkish Language**: I deliberately chose to build the interface entirely in Turkish. While this limits the international audience, it makes the application more accessible and comfortable for its target users—Turkish university students. Flash messages, form labels, and database content are all in Turkish.

**Case-Insensitive Search**: All professor names are stored in lowercase and searches are converted to lowercase before querying. This prevents duplicate entries with different capitalizations and makes searching more flexible for users.

**Flash Messages**: I used Flask's flash messaging system extensively to provide immediate feedback for all user actions. This improves user experience by confirming successful operations and clearly explaining validation errors.

**Environment Variables**: Sensitive information like the database URL and secret key are stored in environment variables rather than hardcoded. This is a security best practice and makes deployment easier across different environments.

The project taught me valuable lessons about full-stack web development, database design, deployment challenges, and the importance of user feedback in interface design. The experience of taking an application from local development to production deployment was particularly educational and highlighted the differences between development and production environments.
