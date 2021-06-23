def create_status(code=200, description=None, **kwargs):
    """
    Creates a status message with code and a description, meant to be returned in a function, and checked in a view to
    determine if the used function was successful or not.
    :param code: HTTP response status code, defaults to 200
    :param description: optional description
    :param kwargs: optional extra information to send back (E.G. ID values after a get request)
    :return: status message as dictionary
    """
    status = {"code": code, 'body': {}}
    if description:
        status['description'] = description
    else:
        if code == 200:
            status['description'] = "Request was successful"
        else:
            status['description'] = "Request threw an error, but the error was not specified"
    if kwargs:
        for k, v in kwargs.items():
            status['body'][k] = v
    return status

