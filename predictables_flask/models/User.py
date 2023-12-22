from typing import List, Tuple

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from predictables_flask.logger import create_logger
from predictables_flask.models.db import db

print(f"db: {db}")
print(f"db.Model: {db.Model}")
print(f"type(db): {type(db)}")
print(f"type(db.Model): {type(db.Model)}")

logger = create_logger(__file__)


class User(UserMixin, db.Model):
    """
    A class used to represent a user.
    """

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    __repr_attrs__ = ["id", "username", "email"]
    __repr_json__ = ["id", "username", "email"]
    __repr_json_exclude__ = ["password_hash"]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self) -> str:
        return "<User %r>" % self.username

    def _does_user_already_exist(self, username: str) -> bool:
        """
        Check if user already exists. Returns True if user already exists, False otherwise.
        """
        return self.query.filter_by(username=username).first() is not None

    def _is_username_empty(self, username: str) -> bool:
        """
        Check if username is empty. Returns True if username is empty, False otherwise.
        """
        return username == ""

    def _is_email_empty(self, email: str) -> bool:
        """
        Check if email is empty. Returns True if email is empty, False otherwise.
        """
        return email == ""

    def _does_email_already_exist(self, email: str) -> Tuple[bool, "User"]:
        """
        Check if email already exists. Returns True if email already exists, False otherwise.
        """
        qry = self.query.filter_by(email=email).first()
        return qry is not None, qry

    def _does_email_include_at_symbol(self, email: str) -> bool:
        """
        Check if email includes the @ symbol. Returns True if email includes the @ symbol, False otherwise.
        """
        return "@" in email

    def _does_email_follow_text_at_text_dot_text_format(self, email: str) -> bool:
        """
        Check if email follows the text@text.text format. Eg. an_email@gmail.com. Returns True if email follows the text@text.text format, False otherwise.
        """
        return len(email.split("@")) == 2 and len(email.split(".")) == 2

    def validate_username_before_adding_new_user(self, username: str) -> bool:
        """
        Validate username before adding a new user. Username is considered valid if:
        1. It is not empty
        2. It does not already exist in the database

        Returns True if username is valid, False otherwise.

        Parameters
        ----------
        username : str
            The username to validate.

        Returns
        -------
        bool
            True if username is valid, False otherwise.

        Note
        ----
        This method is used in the POST /api/v1/auth/register endpoint.
        """
        if self._is_username_empty(username):
            logger.info(f"Username is empty: `{username}`")
            return False
        elif self._does_user_already_exist(username):
            logger.info(f"User already exists: `{username}`")
            return False
        else:
            logger.info(f"Username is valid: `{username}`")
            return True

    def validate_email_before_adding_new_user(self, email: str) -> bool:
        """
        Validate email before adding a new user. Email is considered valid if:
        1. It is not empty
        2. It does not already exist in the database
        3. It includes the @ symbol
        4. It follows the text@text.text format

        Returns True if email is valid, False otherwise.

        Parameters
        ----------
        email : str
            The email to validate.

        Returns
        -------
        bool
            True if email is valid, False otherwise.

        Note
        ----
        1. This method is used in the POST /api/v1/auth/register endpoint.
        2. This method does not implement logging directly. Instead, it calls other methods that implement logging.
        """
        if self._is_email_empty(email):
            # Check if email is empty
            logger.info(f"Email is empty: `{email}`")
            return False
        elif self._does_email_already_exist(email)[0]:
            # Check if email already exists
            logger.info(
                f"Email already exists for user {self._does_email_already_exist(email)[1]}: `{email}`"
            )
            return False
        elif not self._does_email_include_at_symbol(email):
            # Check if email includes the @ symbol
            logger.info(f"Email does not include @ symbol: `{email}`")
            return False
        elif not self._does_email_follow_text_at_text_dot_text_format(email):
            # Check if email follows the text@text format
            logger.info(f"Email does not follow text@text.text format: `{email}`")
            return False
        else:
            # Email is valid
            logger.info(f"Email is valid: `{email}`")
            return True

    # Password hashing and checking
    def _is_password_empty(self, password: str) -> bool:
        """
        Check if password is empty. Returns True if password is empty, False otherwise.
        """
        return password == ""

    def _is_password_same_as_username(self, password: str, username: str) -> bool:
        """
        Check if password is the same as username. Returns True if password is the same as username, False otherwise.
        """
        return password == username

    def _is_password_same_as_email(self, password: str, email: str) -> bool:
        """
        Check if password is the same as email. Returns True if password is the same as email, False otherwise.
        """
        return password == email

    def _is_password_same_as_first_name(self, password: str, first_name: str) -> bool:
        """
        Check if password is the same as first name. Returns True if password is the same as first name, False otherwise.
        """
        return password == first_name

    def _is_password_same_as_last_name(self, password: str, last_name: str) -> bool:
        """
        Check if password is the same as last name. Returns True if password is the same as last name, False otherwise.
        """
        return password == last_name

    def _is_password_at_least_8_characters_long(self, password: str) -> bool:
        """
        Check if password is at least 8 characters long. Returns True if password is at least 8 characters long, False otherwise.
        """
        return len(password) >= 8

    def validate_password_before_adding_new_user(
        self, password: str, username: str, email: str, first_name: str, last_name: str
    ) -> bool:
        """
        Validate password before adding a new user. Password is considered valid if:
        1. It is not empty
        2. It is not the same as the username
        3. It is not the same as the email
        4. It is not the same as the first name
        5. It is not the same as the last name
        6. It is at least 8 characters long

        Returns True if password is valid, False otherwise.

        Parameters
        ----------
        password : str
            The password to validate.
        username : str
            The username to compare against the password.
        email : str
            The email to compare against the password.
        first_name : str
            The first name to compare against the password.
        last_name : str
            The last name to compare against the password.

        Returns
        -------
        bool
            True if password is valid, False otherwise.

        Note
        ----
        1. This method is used in the POST /api/v1/auth/register endpoint.
        2. This method does not implement logging directly. Instead, it calls other methods that implement logging.
        """
        if self._is_password_empty(password):
            # Check if password is empty
            logger.info(f"Password is empty: `{password}`")
            return False
        elif self._is_password_same_as_username(password, username):
            # Check if password is the same as username
            logger.info(
                f"Password is the same as username (username: `{username}`): `{password}`"
            )
            return False
        elif self._is_password_same_as_email(password, email):
            # Check if password is the same as email
            logger.info(
                f"Password is the same as email (email: `{email}`): `{password}`"
            )
            return False
        elif self._is_password_same_as_first_name(password, first_name):
            # Check if password is the same as first name
            logger.info(
                f"Password is the same as first name (first name: `{first_name}`): `{password}`"
            )
            return False
        elif self._is_password_same_as_last_name(password, last_name):
            # Check if password is the same as last name
            logger.info(
                f"Password is the same as last name (last name: `{last_name}`): `{password}`"
            )
            return False
        elif not self._is_password_at_least_8_characters_long(password):
            # Check if password is at least 8 characters long
            logger.info(f"Password is not at least 8 characters long: `{password}`")
            return False
        else:
            # Password is valid
            logger.info("Password is valid")
            return True

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the password is correct.

        Parameters
        ----------
        password : str
            The password to check.

        Returns
        -------
        bool
            True if the password is correct, False otherwise.
        """
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            logger.error(f"Error checking password: {e}")
            raise e

    def to_dict(self) -> dict:
        return {attr: getattr(self, attr) for attr in self.__repr_json__}

    # CRUD operations
    def create(self) -> None:
        """
        Create a new user.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"User `{self.username}` created successfully")
        except Exception as e:
            logger.error(f"Error creating user `{self.username}`: {e}")
            raise e

    def update(self) -> None:
        """
        Update a user.
        """
        try:
            db.session.commit()
            logger.info(f"User `{self.username}` updated successfully")
        except Exception as e:
            logger.error(f"Error updating user `{self.username}`: {e}")
            raise e

    def save(self) -> None:
        """
        Save a user.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"User `{self.username}` saved successfully")
        except Exception as e:
            logger.error(f"Error saving user `{self.username}`: {e}")
            raise e

    def delete(self) -> None:
        """
        Delete a user.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"User `{self.username}` deleted successfully")
        except Exception as e:
            logger.error(f"Error deleting user `{self.username}`: {e}")
            raise e

    # Class methods
    @classmethod
    def get_by_username(cls, username: str) -> "User":
        """
        Get a user by username.

        Parameters
        ----------
        username : str
            The username of the user to get.

        Returns
        -------
        User
            The user with the given username.
        """
        try:
            user = cls.query.filter_by(username=username).first()
            logger.info(f"User `{username}` retrieved successfully")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user `{username}`: {e}")
            raise

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        """
        Get a user by email.
        """
        try:
            user = cls.query.filter_by(email=email).first()
            logger.info(f"User `{email}` retrieved successfully")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user `{email}`: {e}")
            raise e

    @classmethod
    def get_by_id(cls, id: int) -> "User":
        """
        Get a user by ID.
        """
        try:
            user = cls.query.get(id)
            logger.info(f"User `{id}` retrieved successfully")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user `{id}`: {e}")
            raise e

    @classmethod
    def get_all(cls) -> List["User"]:
        """
        Get all users.
        """
        try:
            users = cls.query.all()
            logger.info(f"Users retrieved successfully")
            return users
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            raise e
