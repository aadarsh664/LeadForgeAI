class SearchException(Exception):
    pass

class SearchValidationError(SearchException):
    pass

class ProviderNotFoundError(SearchException):
    pass

class ProviderExecutionError(SearchException):
    pass
