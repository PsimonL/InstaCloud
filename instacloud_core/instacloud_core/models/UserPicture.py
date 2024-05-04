from instacloud_core.extensions import db

class UserPicture(db.Model):
    __tablename__ = 'user_picture'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    picture_identifier = db.Column(db.String(255), nullable=False)
    picture_tag = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<UserPicture %r>' % self.id