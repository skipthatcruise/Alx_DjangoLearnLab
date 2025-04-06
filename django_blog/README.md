# Django Blog Project

This is a Django-based blog project that allows users to create, read, update, and delete (CRUD) blog posts. It includes user authentication features such as registration, login, and profile management.

## Features

- User authentication with registration, login, and logout.
- Create, read, update, and delete blog posts.
- Only authenticated users can create, edit, or delete their posts.
- Posts can be viewed publicly.

## Setup Instructions

1. Clone the repository: 
    ```bash
    git clone <repo_url>
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Start the development server:
    ```bash
    python manage.py runserver
    ```
5. Visit `http://127.0.0.1:8000` in your browser to access the site.

## How to Use

- Navigate to `/register/` to create a new account.
- Use `/login/` to log in.
- Use `/posts/` to view blog posts, `/posts/new/` to create new posts, and `/posts/<id>/edit/` to edit existing posts.
- Only the author of a post can edit or delete it.

## License

MIT License
