import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                        autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    #
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    #
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_newpost(self, title="", post="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")

        self.render("main.html", title=title, post=post, error=error, posts=posts)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title = title, post = post)
            a.put()

            self.redirect("/")
        else:
            error="we need both a title and a blog post!"
            self.render_newpost(title, post, error)

class NewPost(Handler):
    def render_newpost(self, title="", post="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")

        self.render("newpost.html", title=title, post=post, error=error, posts=posts)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title = title, post = post)
            a.put()
            ID = a.key().id()
            self.redirect("/blog/%s" % str(ID))
        else:
            error="we need both a title and a blog post!"
            self.render_newpost(title, post, error)

class ViewPost(Handler):
    def get(self, id, title="", post="", error=""):
        postID=Post.get_by_id(int(id))
        title=postID.title
        post=postID.post

        self.render("viewpost.html", title=title, post=post, error=error)



app = webapp2.WSGIApplication([
    webapp2.Route('/blog/<id:\d+>', ViewPost),
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
