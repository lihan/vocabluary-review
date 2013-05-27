"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views



# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# apis
app.add_url_rule('/api/v1/word_index/', view_func=views.WordIndexAPI.as_view('list_index'))
app.add_url_rule('/api/v1/word_list/<key>', view_func=views.WordListAPI.as_view('word_list'))

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

