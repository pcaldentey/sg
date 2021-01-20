from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = 'sqlite:////app/bin/database/chinook.db'
Base = automap_base()

# engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Album = Base.classes.albums
Track = Base.classes.tracks
Artist = Base.classes.artists

session = Session(engine)
