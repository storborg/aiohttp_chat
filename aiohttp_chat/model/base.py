from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


__all__ = ['Base', 'Session']


Session = scoped_session(sessionmaker())


class _Base(object):
    __table_args__ = {'mysql_engine': 'InnoDB'}

    @classmethod
    def get(cls, id):
        """
        Get an instance of this class by primary key.

        :param id:
            Primary key value.
        :return:
            Instance of the class.
        """
        return Session.query(cls).get(id)


Base = declarative_base(cls=_Base)

Base.metadata.naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s"
}
