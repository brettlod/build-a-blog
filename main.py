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

            self.redirect("/")
        else:
            error="we need both a title and a blog post!"
            self.render_newpost(title, post, error)

class ViewPostHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        self.write(self.render(template, **kw))


    def get(self, id):
        PostID = Post.get_by_id(int(id))
        # title = title.get_by_id(PostID)
        # post = post.get_by_id(PostID)

        if PostID == None:
            error="we need both a title and a blog post!"
            title="Nothing Here"
            self.render("main.html", title=title, post=error, error=error)
        else:
            self.render("main.html", title=PostID, post=PostID)

    # def Post.get_by_id


app = webapp2.WSGIApplication([
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
