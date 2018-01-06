from google.appengine.ext import ndb

class CommentsData(ndb.Model):
    comment_page_id = ndb.IntegerProperty()
    comment_string = ndb.StringProperty(repeated=True)

class BlogpostData(ndb.Model):
    post_title = ndb.StringProperty()
    post_preview = ndb.StringProperty()
    post_link = ndb.StringProperty()
    post_date = ndb.DateProperty().auto_now_add

def blogAsHTML():
    post_query = BlogpostData.query().iter();
    if news_query == None:
        return "<p> No posts yet. </p>"

    html_string = ""
    while (post_query.has_next()):
        blog_item = post_query.next();
        html_string += "<hr> <a class = 'blog_title' href =\"" + blog_item.blog_link + "\"><h2>" + blog_item.blog_title + "</h2></a>"
        html_string += " <p class= 'blog_preview' >" + blog_item.blog_preview + "</p>"
        html_string += "<p class='blog_link'> <a href=\"" + blog_item.blog_link + "\"> Read More...</a></p>"
    return html_string

def constructBlogListHTML():
    html_string = "<ol>\n"
    for i in range(0, len(blog_list)):
        blog_post = blog_list[i]
        html_string += "<li>" + blog_post.listString(i) + "</li>"
    html_string += "</ol>"
    return html_string

class Blogpost:
    def __init__ (self, blog_title, blog_preview, blog_link, blog_date):
        self.blog_title = blog_title
        self.blog_preview = blog_preview
        self.blog_link = blog_link
        self.blog_date = blog_date

    def store(self):
        new_blog_entry = BlogpostData(blog_title = self.blog_title, blog_preview = self.blog_preview, blog_link = self.blog_link, blog_date = self.blog_date)
        new_blog_entry.put()

    def listString(self, page_id):
        return "<a href='post?page_id=" + str(page_id) + "'>" + self.title + "</a>"

    def commentsAsHTML(self, page_id, new_comment):
        comments_query = CommentsData.query(CommentsData.comment_page_id == page_id)
        comments_data = comments_query.get()
        if comments_data == None:
            if new_comment == None:
                return "<p>No comments yet</p>"
            else:
                comment_list = [ new_comment ]
                comments_data = CommentsData(comment_page_id = page_id,
                                             comment_string = comment_list)
                comments_data.put()
                return "<p>" + new_comment + "</p>"
        else:
            if new_comment != None:
                comments_data.comment_string.append(new_comment)
            html_string = ""
            for comment in comments_data.comment_string:
                html_string += "<p>" + comment + "</p>"
            if new_comment != None:
                comments_data.put()
            return html_string

blog_list = [
    BlogPost(
        "My Google CSSI Experience",
        "This is short description of my CSSI experience")
]
