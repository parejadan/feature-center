from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ProductTypes(db.Model):  # existing product types
    __tablename__ = 'product_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(50), nullable=False)
    client_relation = db.relationship('Client', 
                                      backref=db.backref('product_type', lazy=True))

    def to_dict(self):
        serialized = {
            'id': self.id,
            'product_code': self.product_code,
        }
        return serialized


class PriorityTypes(db.Model):
    __tablename__ = 'priority_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority_name = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        serialized = {
            'id': self.id,
            'priority_name': self.priority_name,
        }
        return serialized


clientFeatureRequest = db.Table('client_feature_request',
                                db.Column('feature_id', db.Integer, db.ForeignKey('feature_info.id'), primary_key=True),
                                db.Column('priority_id', db.Integer, db.ForeignKey('priority_types.id'), primary_key=True),
                                db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
                                db.Column('date_created', db.DateTime, default=db.func.current_timestamp())
                                )


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(25), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=True),
    # reference to the ORM not the table name
    request_relation = db.relationship('FeatureInfo', secondary=clientFeatureRequest,
                                       backref=db.backref('client', lazy=True))

    def to_dict(self):
        serialized = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'product_id': self.product_id,
            'request_relation': self.request_relation
        }
        return serialized


class FeatureInfo(db.Model):
    __tablename__ = 'feature_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_target = db.Column(db.DateTime, nullable=True)  # target date might not be finalized
    priority_relation = db.relationship('PriorityTypes', secondary=clientFeatureRequest,
                                        backref=db.backref('feature_info', lazy=True))
    client_relation = db.relationship('Client', secondary=clientFeatureRequest,
                                      backref=db.backref('feature_info', lazy=True))

    def to_dict(self):
        serialized = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_target': self.date_target,
            'priority_relation': self.priority_relation,
            'client_relation': self.client_relation
        }
        return serialized
