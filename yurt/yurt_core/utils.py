import os

__author__ = 'deanmercado'

###
# helper functions
###


def find_file_in_ancestor(
        target_file,
        path=None,
        error_message='Could not find file in ancestor',
        stack_limit=None,
        depth=0
):
    if path is None:
        path = os.getcwd()
    if os.path.exists(os.path.join(path, target_file)):
        return path
    if stack_limit is None:
        if os.path.expanduser("~") == path:
            raise IOError(error_message)
    if stack_limit:
        if depth == stack_limit:
            raise IOError("{}: Max stack limit reached".format(error_message))

    return find_file_in_ancestor(
        target_file,
        path=os.path.dirname(path),
        error_message=error_message,
        stack_limit=stack_limit,
        depth=depth + 1
    )


def get_iter(dictionary):
    """
    Just a wrapper method that handles Python2->Python3 dict iterations
    :param dictionary: (Dict)
    :return: (Dict)
    """
    try:
        return dictionary.iteritems()
    except AttributeError:
        return dictionary.items()
