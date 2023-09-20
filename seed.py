from application import db
from application.models import Entry
from datetime import datetime


db.drop_all()
print("Droping database")
db.create_all()
print("Creating database")

print("Seeding database")
entry1 = Entry(
    date="08/09/23",
    title="Twice in London!",
    content="I went to watch the Kpop girl group Twice at the O2 in London. It was AMAZING!",
    tag="Concert",
    author="Ravs"
)

entry2 = Entry(
    date="15/09/23",
    title="Trip to Kosovo",
    content="Today I flew to Kosovo with my friends",
    tag="Travel",
    author="Dina"
)

entry3 = Entry(
    date="20/09/23",
    title="Finished watching One Piece Live Action",
    content="I completed watching the One Piece Live Action on Netflix, it was really good!",
    tag="TV",
    author="Malar"
)

db.session.add(entry1)
db.session.add_all([entry2, entry3])

db.session.commit()

print("Database seeded successfully")
