"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views



# Home page
app.add_url_rule('/', 'home', view_func=views.home)
app.add_url_rule('/app', 'app_view', view_func=views.app_view)

# Oauth2
app.add_url_rule('/auth/google/', 'google_auth', view_func=views.GoogleAuthView.as_view('google_auth'))


# apis
app.add_url_rule('/api/v1/word_index/', view_func=views.WordIndexAPI.as_view('list_index'))
app.add_url_rule('/api/v1/word_list/<key>', view_func=views.WordListAPI.as_view('word_list'))

# apis for bookmarks
app.add_url_rule('/api/v1/bookmarks/', view_func=views.BookmarkAPI.as_view('bookmark_list'))
app.add_url_rule('/api/v1/bookmarks/<id>', view_func=views.BookmarkAPIDelete.as_view('delete_bookmark'))

# Admin pages
app.add_url_rule('/admin', view_func=views.AdminView.as_view('admin_view'))

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

