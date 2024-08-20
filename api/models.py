class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


class Book:
    def __init__(self, id, title, author, year):
        self.id = id
        self.title = title
        self.author = author
        self.year = year