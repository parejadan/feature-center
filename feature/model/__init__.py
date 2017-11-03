from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ProductTypes(db.Model):  # existing product types
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        serialized = {
            'id': self.id,
            'product_code': self.product_code,
        }
        return serialized


class PriorityTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority_name = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        serialized = {
            'id': self.id,
            'priority_name': self.priority_name,
        }
        return serialized


clientFeatureRequest = db.Table('ClientFeatureRequest',
                                db.Column('client_id', db.Integer, db.ForeignKey('Client.id'), nullable=False,
                                          primary_key=True),
                                db.Column('feature_id', db.Integer, db.ForeignKey('FeatureInfo.id'), nullable=False,
                                          primary_key=True),
                                db.Column('priority_id', db.Integer, db.ForeignKey('PriorityTypes.id'), nullable=False,
                                          primary_key=True),
                                db.Column('date_created', db.DateTime, default=db.func.current_timestamp())
                                )
# def to_dict(self):
#    serialized = {
#        'client_id': self.client_id,
#        'feature_id': self.feature_id,
#        'priority_id': self.priority_id,
#        'product_id': self.product_id,
#        'date_created': self.date_created,
#    }
#    return serialized


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(25), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("ProductTypes.id"), nullable=True, primary_key=True)
    request_relation = db.relationship('FeatureInfo', secondary=clientFeatureRequest, lazy='subquery',
                                       backref=db.backref('client', lazy=True))

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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_target = db.Column(db.DateTime, nullable=True)  # target date might not be finalized
    priority_relation = db.relationship('PriorityTypes', secondary=clientFeatureRequest, lazy='subquery',
                                        backref=db.backref('FeatureInfo', lazy=True))
    client_relation = db.relationship('Client', secondary=clientFeatureRequest, lazy='subquery',
                                      backref=db.backref('FeatureInfo', lazy=True))

    def to_dict(self):
        serialized = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_target': self.date_target
        }
        return serialized
