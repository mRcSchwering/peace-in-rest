# this python file uses the following encoding: utf-8


class ValidationError(Exception):
    """Use this for further validation errors. E.g. request validation, str should be in a specific format."""
    pass


class NoResultFound(Exception):
    """This is for when a database result is needed but there was none found"""
    pass
