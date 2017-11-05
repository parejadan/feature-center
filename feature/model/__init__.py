from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def safe_serialize(obj):
    try:
        return obj.serialized()
    except Exception as ex:
        print('unable to serialize {}'.format(obj), ex)


class ProductTypes(db.Model):  # existing product types
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(50), nullable=False)
    client_relation = db.relationship('Client', cascade='all, delete-orphan',
                                      backref='ProductTypes', lazy=True)

    def to_dict(self):
        return safe_serialize(self)

    def serialized(self):
        _serialized = {
            'id': self.id,
            'product_code': self.product_code,
        }
        return _serialized


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(25), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    request_relation = db.relationship('ClientFeatureRequest', cascade='all, delete-orphan',
                                       backref='Client', lazy=True)

    def to_dict(self):
        return safe_serialize(self)

    def serialized(self):
        _serialized = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'product_id': self.product_id,
        }
        return _serialized


class ClientFeatureRequest(db.Model):
    __tablename__ = 'client_feature_request'
    # we only care that it's unique
    # db.Sequence("seq_client_feature_request_id"), unique=True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))  # read requirements closer, primary_key=True)
    priority_id = db.Column(db.Integer)
    date_target = db.Column(db.DateTime, nullable=True)  # target date might not be finalized
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())  # keep track client request vs target

    def to_dict(self):
        return safe_serialize(self)

    def serialized(self):
        _serialized = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_id': self.client_id,
            'product_id': self.product_id,
            'priority_id': self.priority_id,
            'date_target': self.date_target.strftime("%m-%d-%Y"),
            'date_created': self.date_created.strftime("%m-%d-%Y")
        }
        return _serialized
