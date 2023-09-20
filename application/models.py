from application import db, app

app.app_context().push()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(50))
    author = db.Column(db.String(100))

    def __init__(self, date, title, content, tag, author):
        self.date = date
        self.title = title
        self.content = content
        self.tag = tag
        self.author = author

    def __repr__(self):
        return f"On {self.date} I {self.content}"
    
    @property
    def json(self):
        return { "id":self.id, "date": self.date, "title":self.title, "content": self.content, "tag": self.tag, "author": self.author }