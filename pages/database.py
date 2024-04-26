import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine('mysql://avnadmin:AVNS_Rmh1oMSv9pkjyCW9OmD@mysql-39776083-lifeonland.a.aivencloud.com:16152/lifeonland')
Base = declarative_base()

connection = engine.connect()
Session = sessionmaker(bind=engine)
# session = Session()

def get_session():
    # Session = sessionmaker(bind=engine)
    return Session, connection

class Trails(Base):
    __tablename__ = 'trails'
    trail_name = db.Column(db.String(100), primary_key=True)
    trail_desc = db.Column(db.String(5000))
    trail_duration = db.Column(db.Float)
    trail_distance = db.Column(db.Float)
    trail_ele_gain = db.Column(db.Float)
    trail_loop = db.Column(db.String(20))
    trail_dist_mel = db.Column(db.Float)
    trail_time_mel = db.Column(db.Float)
    trail_species = db.Column(db.String(1000))
    
class Uploads(Base):
    __tablename__ = 'uploads'
    upload_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    upload_lat = db.Column(db.Float)
    upload_long = db.Column(db.Float)
    upload_time = db.Column(db.String(50))
    upload_img = db.Column(db.BLOB)
    upload_species = db.Column(db.String(100))
    
    
    



# connection = engine.connect()
# trails = pd.read_sql('SELECT * FROM trails', con=connection)
# uploads = pd.read_sql('SELECT * FROM uploads', con=connection)