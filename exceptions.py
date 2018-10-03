

class SapAwsCoreError(Exception):
    """
    The base exception type for the SAP AWS CLI  exceptions.

    :ivar msg: the message associated to the error.
    """

    fmt = 'An unspecified error has occurred'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


class AwsPermissionsError():

    msg = "AWS Permissions Error"
