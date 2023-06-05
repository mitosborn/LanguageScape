from datetime import datetime
from flask_dance.consumer.storage import BaseStorage
from flask_dance.utils import FakeCache, first
from flask_login import AnonymousUserMixin, current_user
from pynamodb.attributes import UnicodeAttribute, MapAttribute, UTCDateTimeAttribute

from model.LangModel import LangModel


class OAuth(LangModel):
    """
    A :ref:`SQLAlchemy declarative mixin <sqlalchemy:declarative_mixins>` with
    some suggested columns for a model to store OAuth tokens:

    ``id``
        an integer primary key
    ``provider``
        a short name to indicate which OAuth provider issued
        this token
    ``created_at``
        an automatically generated datetime that indicates when
        the OAuth provider issued this token
    ``token``
        a :class:`JSON <sqlalchemy.types.JSON>` field to store
        the actual token received from the OAuth provider
    """

    class Meta(LangModel.Meta):
        table_name = 'OAuth'

    user_id = UnicodeAttribute(hash_key=True)  # User.username = OAuth.id
    provider = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()
    token = MapAttribute()

    def __tablename__(cls):
        return f"flask_dance_{cls.__name__.lower()}"

    @property
    def id(self):
        return self.user_id

    def __repr__(self):
        parts = [self.__class__.__name__]
        if self.id:
            parts.append(f"id={self.id}")
        if self.provider:
            parts.append(f'provider="{self.provider}"')
        return "<{}>".format(" ".join(parts))


class DynamoDBStorage(BaseStorage):
    """
    Stores and retrieves OAuth tokens using a relational database through
    the `SQLAlchemy`_ ORM.

    .. _SQLAlchemy: http://www.sqlalchemy.org/
    """

    def __init__(
            self,
            model,
            user=None,
            user_id=None,
            user_required=None,
            anon_user=None,
            cache=None,
    ):
        """
        Args:
            model: The SQLAlchemy model class that represents the OAuth token
                table in the database. At a minimum, it must have a
                ``provider`` column and a ``token`` column. If tokens are to be
                associated with individual users in the application, it must
                also have a ``user`` relationship to your User model.
                It is recommended, though not required, that your model class
                inherit from
                :class:`~flask_dance.consumer.storage.sqla.OAuthConsumerMixin`.
            user:
                If you want OAuth tokens to be associated with individual users
                in your application, this is a reference to the user that you
                want to use for the current request. It can be an actual User
                object, a function that returns a User object, or a proxy to the
                User object. If you're using `Flask-Login`_, this is
                :attr:`~flask.ext.login.current_user`.
            user_id:
                If you want to pass an identifier for a user instead of an actual
                User object, use this argument instead. Sometimes it can save
                a database query or two. If both ``user`` and ``user_id`` are
                provided, ``user_id`` will take precendence.
            user_required:
                If set to ``True``, an exception will be raised if you try to
                set or retrieve an OAuth token without an associated user.
                If set to ``False``, OAuth tokens can be set with or without
                an associated user. The default is auto-detection: it will
                be ``True`` if you pass a ``user`` or ``user_id`` parameter,
                ``False`` otherwise.
            anon_user:
                If anonymous users are represented by a class in your application,
                provide that class here. If you are using `Flask-Login`_,
                anonymous users are represented by the
                :class:`flask_login.AnonymousUserMixin` class, but you don't have
                to provide that -- Flask-Dance treats it as the default.
            cache:
                An instance of `Flask-Caching`_. Providing a caching system is
                highly recommended, but not required.

        .. _Flask-SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/
        .. _Flask-Login: https://flask-login.readthedocs.io/
        .. _Flask-Caching: https://flask-caching.readthedocs.io/en/latest/
        """
        self.model = model
        self.user = user
        self.user_id = user_id
        if user_required is None:
            self.user_required = user is not None or user_id is not None
        else:
            self.user_required = user_required
        self.anon_user = anon_user or AnonymousUserMixin
        self.cache = cache or FakeCache()

    # def make_cache_key(self, blueprint, user=None, user_id=None):
    #     uid = first([user_id, self.user_id, blueprint.config.get("user_id")])
    #     if not uid:
    #         u = first(
    #             _get_real_user(ref, self.anon_user)
    #             for ref in (user, self.user, blueprint.config.get("user"))
    #         )
    #         uid = getattr(u, "id", u)
    #     return "flask_dance_token|{name}|{user_id}".format(
    #         name=blueprint.name, user_id=uid
    #     )

    def get(self, blueprint, user=None, user_id=None):
        """When you have a statement in your code that says
        "if <provider>.authorized:" (for example "if google.authorized:"),
        a long string of function calls result in this function being used to
        check the Flask server's cache and database for any records associated
        with the current_user. The `user` and `user_id` parameters are actually
        not set in that case (see base.py:token(), that's what calls this
        function), so the user information is instead loaded from the
        current_user (if that's what you specified when you created the
        blueprint) with blueprint.config.get('user_id').

        :param blueprint:
        :param user:
        :param user_id:
        :return:
        """
        # check cache
        # cache_key = self.make_cache_key(blueprint=blueprint, user=user, user_id=user_id)
        # token = self.cache.get(cache_key)
        # if token:
        #     return token
        # if not cached, make database queries
        print("Called GET OAuth")
        provider = blueprint.name
        uid = first([user_id, self.user_id, blueprint.config.get("user_id")])
        u = first(
            _get_real_user(ref, self.anon_user)
            for ref in (user, self.user, blueprint.config.get("user"))
        )
        print("Printing user objects")
        print(u)
        print(uid)
        print(current_user)
        print(dir(blueprint))
        if self.user_required and not u and not uid:
            raise ValueError("Cannot get OAuth token without an associated user")
        fetched_token = None
        try:
            # check for user ID
            if hasattr(self.model, "user_id") and uid:
                fetched_token = self.model.safe_get(uid, provider).to_dict()['token']
            # check for user (relationship property)
            elif hasattr(self.model, "user_id") and u:
                fetched_token = self.model.safe_get(u.get_id(), provider).to_dict()['token']
        except Exception as e:
            fetched_token = None
            print(e)


        # if we have the property, but not value, filter by None
        # elif hasattr(self.model, "user_id"):
        #     query = query.filter_by(user_id=None, condition=condition)
        # run query

        # # cache the result
        # self.cache.set(cache_key, token)
        print("GET returning oauth: {token}".format(token=fetched_token))
        print("This is confusing")
        return fetched_token

    def set(self, blueprint, token, user=None, user_id=None):
        print("Called SET OAuth")
        uid = first([user_id, self.user_id, blueprint.config.get("user_id")])
        u = first(
            _get_real_user(ref, self.anon_user)
            for ref in (user, self.user, blueprint.config.get("user"))
        )

        if self.user_required and not u and not uid:
            raise ValueError("Cannot set OAuth token without an associated user")

        # check for user ID
        has_user_id = hasattr(self.model, "user_id")
        oauth = None
        if has_user_id and uid:
            oauth = self.model.safe_get(uid, blueprint.name)
        # check for user (relationship property)
        has_user = hasattr(self.model, "user")
        if has_user and u:
            oauth = self.model.safe_get(u.user_id, blueprint.name)
        # queue up delete query -- won't be run until commit()
        if oauth:
            oauth.token = token
        else:
            oauth = self.model(user_id=u.user_id,
                               provider=blueprint.name,
                               created_at=datetime.now(),
                               token=token)
        oauth.save()

    # # invalidate cache
    # self.cache.delete(
    #     self.make_cache_key(blueprint=blueprint, user=user, user_id=user_id)
    # )

    def delete(self, blueprint, user=None, user_id=None):
        print("Called DELETE OAuth")
        print(blueprint)
        print(user)
        print(user_id)
        uid = first([user_id, self.user_id, blueprint.config.get("user_id")])
        u = first(
            _get_real_user(ref, self.anon_user)
            for ref in (user, self.user, blueprint.config.get("user"))
        )
        #
        # if self.user_required and not u and not uid:
        #     raise ValueError("Cannot delete OAuth token without an associated user")

        oauth = None
        # check for user ID
        if hasattr(self.model, "user_id") and uid:
            oauth = self.model.safe_get(uid, blueprint.name)
        # check for user (relationship property)
        elif hasattr(self.model, "user_id") and u:
            oauth = self.model.safe_get(u.user_id, blueprint.name)
        else:
            raise NotImplemented("OAuth Token not found in DELETE")
        # if we have the property, but not value, filter by None
        # elif hasattr(self.model, "user_id"):
        #     query = query.filter_by(user_id=None)
        # run query
        oauth.delete()
        # invalidate cache
        # self.cache.delete(
        #     self.make_cache_key(blueprint=blueprint, user=user, user_id=user_id)
        # )


def _get_real_user(user, anon_user=None):
    """
    Given a "user" that could be:

    * a real user object
    * a function that returns a real user object
    * a LocalProxy to a real user object (like Flask-Login's ``current_user``)

    This function returns the real user object, regardless of which we have.
    """
    if hasattr(user, "_get_current_object"):
        # this is a proxy
        user = user._get_current_object()
    if callable(user):
        # this is a function
        user = user()
    if anon_user and isinstance(user, anon_user):
        return None
    return user
