#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb

#set up environment for Jinja
#this sets jinja's relative directory to match the directory name(dirname) of
#the current __file__, in this case, main.py
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def constructBlogListHTML():
    post_query = BlogpostData.query().iter();
    if post_query == None:
        return "<p> No posts yet. </p>"

    html_string = ""
    while (post_query.has_next()):
        blog_item = post_query.next();
        html_string += "<hr> <a class = 'blog_title'<h2>" + blog_item.blog_title + "</h2></a>"
        html_string += "<h3 class= 'blog_date' >" + blog_item.blog_date + "</h3>"
        html_string += "<p class= 'blog_preview'>" + blog_item.blog_preview + "</p>"
        html_string +=  "<a href='post?title=" + str(blog_item.blog_title) +"'> Read More... </a>"
    return html_string

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #this is where you reference your HTML file
        template = jinja_environment.get_template('templates/index.html')
        template_variables = {"bloglist": constructBlogListHTML()}
        self.response.out.write(template.render(template_variables))

class PostHandler(webapp2.RequestHandler):
    def get(self):
        # This creates and serves the blog post page
        title = self.request.get('title')
        self.sendResponse(title, None)

    def post(self):
        title = self.request.get('title')
        self.sendResponse(title, self.request.get("comment"))

    def sendResponse(self, title, new_comment):
        template = jinja_environment.get_template('templates/blogpost.html')
        #blogpost_query = BlogpostData.query(BlogpostData.blog_title == title)
        #blogpost_data = blogpost_query.get()

        blogpostHTML = blogpostAsHTML(self, title, new_comment)
        template_variables = {"content": blogpostHTML}
        #                      "date": blogpost_data.blog_date,
        #                      "content": blogpost_data.blog_content,
        #                      "comments": commentHTML }
        self.response.out.write(template.render(template_variables))

class BlogpostData(ndb.Model):
    #page_id = ndb.IntegerProperty()
    blog_title = ndb.StringProperty()
    blog_date = ndb.StringProperty()
    blog_content = ndb.StringProperty()
    blog_preview = ndb.StringProperty()
    blog_link = ndb.StringProperty()
    comment_string = ndb.StringProperty(repeated=True)

class Blogpost:

    def __init__ (self, blog_title, blog_date, blog_content, blog_preview, blog_link, comment_string):
        self.blog_title = blog_title
        self.blog_date = blog_date
        self.blog_content = blog_content
        self.blog_preview = blog_preview
        self.blog_link = blog_link
        self.comment_string = comment_string

    def listString(self, title):
        return "<a href='post?title'>" + self.blog_title + "</a>"

    def store(self):
        post_query = BlogpostData.query();
        new_blog_entry = BlogpostData(
                                      blog_title = self.blog_title,
                                      blog_date = self.blog_date,
                                      blog_content = self.blog_content,
                                      blog_preview = self.blog_preview,
                                      blog_link = self.blog_link,
                                      comment_string = self.comment_string)
        new_blog_entry.put()


#class CommentsData(ndb.Model):
#    blog_title = ndb.StringProperty()
#    comment_string = ndb.StringProperty()
def blogpostAsHTML(self, title, new_comment):
    post_query = BlogpostData.query(BlogpostData.blog_title == title)
    post_data = post_query.get()
    html_string = ""
    html_string += "<hr> <a class = 'blog_title'<h2>" + post_data.blog_title + "</h2></a>"
    html_string += "<h3 class= 'blog_date' >" + post_data.blog_date + "</h3>"
    html_string += "<p class= 'blog_preview'>" + post_data.blog_content + "</p>"
    logging.info("here is the comment data" + str(BlogpostData.comment_string))
    if post_data.comment_string == None:
        if new_comment == None:
            logging.info("thinks there are no comments at all")
            html_string+="<p style=color:black> No comments yet </p>"
        else:
            logging.info("thinks there is one comment submitted")
            post_data.comment_string = [ new_comment ]
            post_data.put()
            html_string += "<p style=color:black>" + new_comment + "</p>"
    else:
        if new_comment != None:
            logging.info("thinks there are multiple comments in list")
            post_data.comment_string.append(new_comment)
            post_data.put()
        comment_string = ""
        for comment in post_data.comment_string:
            logging.info("actually printing all comments in list")
            comment_string += "<p style=color:black>" + comment + "</p>"
        html_string += comment_string
    return html_string

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/admin.html')
        self.response.out.write(template.render())

    def post(self):
        blog_title = self.request.get("blog_title")
        blog_date = self.request.get("blog_date")
        blog_content = self.request.get("blog_content")
        blog_preview = self.request.get("blog_preview")
        blog_link = self.request.get("blog_link")

        new_blog_entry = BlogpostData(#page_id = page_id,
                                      blog_title = blog_title,
                                      blog_date = blog_date,
                                      blog_content = blog_content,
                                      blog_preview = blog_preview,
                                      blog_link = blog_link,
                                      comment_string = comment_string)
        new_blog_entry.put()

        template = jinja_environment.get_template('templates/admin.html')
        self.response.out.write(template.render())
        self.response.out.write("You have submitted a new news article.")


# creates a WSGIApplication and assigns it to the variable app.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostHandler),
    ('/admin', AdminHandler)
], debug=True)
