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
import os
import webapp2
import jinja2
import string

template_dir = os.path.join(os.path.dirname(__file__),"templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

toggle = False

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        global toggle
        text = self.request.get("text")
        if not toggle:
            self.render("index.html",text = self.get_rot_13(text))
            toggle = True
        else:
            self.render("index.html",text = self.get_original_text(text))
            toggle = False

    def get_rot_13(self, text):
        alphabets = string.ascii_lowercase
        increment = 13
        new_text = ''
        for char in text:
            diff = 0
            try:
                char_index = alphabets.index(char.lower())
                diff = char_index + 13
                if diff > 25:
                    diff = diff - 26
                new_char = alphabets[abs(diff)]
                if char.isupper():
                    new_char = new_char.upper()
            except ValueError:
                new_char = char
            new_text += new_char
        return new_text

    def get_original_text(self, text):
        alphabets = string.ascii_lowercase
        increment = 13
        new_text = ''
        for char in text:
            diff = 0
            try:
                char_index = alphabets.index(char.lower())
                diff = char_index - 13
                if diff < 0:
                    diff = diff + 26
                new_char = alphabets[abs(diff)]
                if char.isupper():
                    new_char = new_char.upper()
            except ValueError:
                new_char = char
            new_text += new_char
        return new_text

app = webapp2.WSGIApplication([
    ('/test', MainPage)
], debug=True)
