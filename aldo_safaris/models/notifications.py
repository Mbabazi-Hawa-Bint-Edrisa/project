from flask_sqlalchemy import SQLAlchemy
from aldo_safaris.extensions import db

db = SQLAlchemy()

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String(20))

    recipient = db.relationship('User', backref='notifications')

    def __repr__(self):
        return '<Notification %r>' % self.notification_id
