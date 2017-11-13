from feature.model import db
from feature.model.logic import to_json_dump


class Transaction:
    def __init__(self):
        self.INSERT = 'insert'
        self.UPDATE = 'update'
        self.DELETE = 'delete'

        # map transaction types to actual transaction to commit
        # only accessible via commit
        self._actions = {
            self.INSERT: self._insert,
            self.UPDATE: self._update,
            self.DELETE: self._delete
        }

    def commit(self, query, t_type):
        try:
            self._actions[t_type](query)
            db.session.commit()
            return True
        except Exception as ex:
            print('exception encountered processing {} transaction: '.format(t_type), ex)
            return False

    @staticmethod
    def basic_select(table, order_key=None, _id=None, _cast=True):
        try:
            if _id is None:
                query = table.query

                if not (order_key is None):
                    query = query.order_by(order_key)

                query = query.all()
            else:
                query = table.query.get(_id)

            if _cast:
                return to_json_dump(query)
            else:
                return query
        except Exception as ex:
            print('exception encountered pulling records from {}: '.format(table), ex)

    @staticmethod
    def _insert(query):
        db.session.add(query)

    @staticmethod
    def _update(query):
        pass

    @staticmethod
    def _delete(query):
        db.session.delete(query)
