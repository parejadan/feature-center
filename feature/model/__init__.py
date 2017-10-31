from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    # delete all feature requests if we drop client
    feature_requests = db.relationship('ClientFeatureRequest', cascade='all, delete-orphan',
                                       backref='Client', lazy='dynamic')


class FeatureInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_target = db.Column(db.DateTime, nullable=True)  # target date might not be finalized


class ProductTypes(db.Model):  # existing product types
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_code = db.Column(db.String(50), nullable=False)


class ClientFeatureRequest(db.Model):
    # Composite key of client, feature, priority assures a client only has one per feature and request
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False, primary_key=True)
    # make unique to prevent a feature having double priority
    feature_id = db.Column(db.Integer, db.ForeignKey('FeatureInfo.id'), nullable=False, primary_key=True, unique=True)
    priority = db.Column(db.Integer, nullable=False, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('ProductTypes.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # delete feature info if client or request ever get removed
    features = db.relationship('FeatureInfo', cascade='all, delete-orphan',
                               backref='ClientFeatureRequest', lazy='dynamic')


