# this python file uses the following encoding: utf-8


class ValidationError(Exception):
    """For custom validation errors"""
    pass


class AlreadyExists(Exception):
    """For when something should be created but it already exists"""
    pass


class NoResultFound(Exception):
    """For when a database result is needed but there was none found"""
    pass
