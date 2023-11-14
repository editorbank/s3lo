# -*- coding: utf-8 -*-
# Copyright (c) 2012 Thomas Parslow http://almostobsolete.net/
#
#
from boto.exception import BotoServerError


class LimitExceededException(BotoServerError):
    pass


class DataAlreadyAcceptedException(BotoServerError):
    pass


class ResourceInUseException(BotoServerError):
    pass


class ServiceUnavailableException(BotoServerError):
    pass


class InvalidParameterException(BotoServerError):
    pass


class ResourceNotFoundException(BotoServerError):
    pass


class ResourceAlreadyExistsException(BotoServerError):
    pass


class OperationAbortedException(BotoServerError):
    pass


class InvalidSequenceTokenException(BotoServerError):
    pass
