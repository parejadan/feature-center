from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(25), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("ProductTypes.id"), nullable=True, primary_key=True)
    # delete all feature requests if we drop client
    feature_requests = db.relationship('ClientFeatureRequest', cascade='all, delete-orphan',
                                       backref='Client', lazy='dynamic')

    def to_dict(self):
        serialized = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'product_id': self.product_id,
        }
        return serialized


class FeatureInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_target = db.Column(db.DateTime, nullable=True)  # target date might not be finalized

    def to_dict(self):
        serialized = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_target': self.date_target
        }
        return serialized


class ProductTypes(db.Model):  # existing product types
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(50), nullable=False)
    client_products = db.relationship('Client', cascade='all, delete-orphan', backref='ProductTypes', lazy='dynamic')

    def to_dict(self):
        serialized = {
            'id': self.id,
            'product_code': self.product_code,
        }
        return serialized


class PriorityTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority_name = db.Column(db.String(15), nullable=False)
    request_priority = db.relationship('ClientFeatureRequest', cascade='all, delete-orphan', backref='PriorityTypes',
                                       lazy='dynamic')

    def to_dict(self):
        serialized = {
            'id': self.id,
            'priority_name': self.priority_name,
        }
        return serialized


class ClientFeatureRequest(db.Model):
    # Composite key of client, feature, priority assures a client only has one per feature and request
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False, primary_key=True)
    # make unique to prevent a feature having double priority
    feature_id = db.Column(db.Integer, db.ForeignKey('FeatureInfo.id'), nullable=False, primary_key=True, unique=True)
    priority_id = db.Column(db.Integer, db.ForeignKey('PriorityTypes.id'), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('ProductTypes.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    # delete feature info if client or request ever get removed
    features = db.relationship('FeatureInfo', cascade='all, delete-orphan',
                               backref='ClientFeatureRequest', lazy='dynamic')

    def to_dict(self):
        serialized = {
            'client_id': self.client_id,
            'feature_id': self.feature_id,
            'priority_id': self.priority_id,
            'product_id': self.product_id,
            'date_created': self.date_created,
        }
        return serialized

