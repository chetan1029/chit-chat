class MessageError(Exception):
    pass


class DataStoreError(MessageError):
    pass


class MessageNotFoundError(MessageError):
    pass
