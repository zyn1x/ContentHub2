# ContentHub2

A Twitter/X-like content sharing web application built with Django 5.2.

## Features

- **Posts** — Create, edit, and delete posts with text, images, and videos
- **Hashtags** — Automatically extracted from post text; click any `#tag` to browse its feed
- **Likes** — Like or unlike posts with instant count update (no page reload)
- **Comments** — Threaded comment section on every post; authors can delete their own
- **Search** — Search across post text and hashtags
- **Auth** — Register, login, logout with Django's built-in authentication
- **Pagination** — 10 posts per page on all feeds
- **File validation** — Images: jpg, jpeg, png, gif · Videos: mp4, webm · Max 10 MB per file
- **Admin panel** — Full Django admin for all models

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Django 5.2 LTS                      |
| Database   | SQLite3 (default)                   |
| Auth       | `django.contrib.auth`               |
| Media      | Local filesystem (`MEDIA_ROOT`)     |
| Frontend   | HTML5, CSS3, Vanilla JavaScript     |
| Images     | Pillow                              |

## Project Structure

```
ContentHub2/
├── manage.py
├── requirements.txt
├── contenthub/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Main app
│   ├── models.py            # Post, Like, Comment, Hashtag
│   ├── views.py             # All views
│   ├── forms.py             # PostForm, CommentForm, CustomUserCreationForm
│   ├── urls.py
│   ├── admin.py
│   └── templatetags/
│       └── core_extras.py   # |render_hashtags filter
├── templates/core/
│   ├── base.html
│   ├── feed.html
│   ├── post_detail.html
│   ├── post_form.html
│   ├── post_confirm_delete.html
│   ├── search_results.html
│   ├── hashtag_feed.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── partials/
│       ├── post_card.html
│       └── comment.html
└── static/css/
    └── style.css
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ContentHub2.git
cd ContentHub2
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## URL Reference

| URL                        | View              | Auth required |
|----------------------------|-------------------|---------------|
| `/`                        | Feed              | No            |
| `/post/create/`            | Create post       | Yes           |
| `/post/<pk>/`              | Post detail       | No            |
| `/post/<pk>/edit/`         | Edit post         | Owner only    |
| `/post/<pk>/delete/`       | Delete post       | Owner only    |
| `/post/<pk>/like/`         | Like toggle (POST)| Yes           |
| `/post/<pk>/comment/`      | Add comment       | Yes           |
| `/comment/<pk>/delete/`    | Delete comment    | Owner only    |
| `/hashtag/<name>/`         | Hashtag feed      | No            |
| `/search/`                 | Search            | No            |
| `/register/`               | Register          | No            |
| `/login/`                  | Login             | No            |
| `/logout/`                 | Logout            | Yes           |
| `/admin/`                  | Django admin      | Superuser     |

## Environment Notes

- `DEBUG = True` and `SECRET_KEY` are set to development values in `settings.py`. Change both before any production deployment.
- SQLite is used by default. For production, switch to PostgreSQL or another database in `settings.py`.
- Uploaded media files are stored in the `media/` directory. This directory is not included in version control (see `.gitignore`).

## .gitignore

Make sure your `.gitignore` includes at minimum:

```
venv/
__pycache__/
*.pyc
db.sqlite3
media/
.env
```

---

Built by **Dikshant Sharma**
