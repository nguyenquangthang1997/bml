from sawtooth_sdk.processor.exceptions import InvalidTransaction

from protobuf import payload_pb2


class SupplyPayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.SimpleSupplyPayload()
        self._transaction.ParseFromString(payload)

    @property
    def action(self):
        return self._transaction.action

    @property
    def data(self):
        if self._transaction.HasField('synchronize_data') and \
                self._transaction.action == \
                payload_pb2.SimpleSupplyPayload.SYNCHRONIZE_DATA:
            return self._transaction.synchronize_data
        raise InvalidTransaction('Action does not match payload data')

    @property
    def timestamp(self):
        return self._transaction.timestamp
