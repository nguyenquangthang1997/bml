from addressing import addresser

# from protobuf import user_pb2
from protobuf import data_pb2


class SupplyState(object):
    def __init__(self, context, timeout=2):
        self._context = context
        self._timeout = timeout

    def set_data(self, public_key, data):
        user_address = addresser.get_user_address(public_key)

        data_pb = data_pb2.Data(
            data=data
        )
        container = data_pb2.DataContainer()
        state_entries = self._context.get_state(
            addresses=[user_address], timeout=self._timeout)
        if state_entries:
            container.ParseFromString(state_entries[0].data)

        container.entries.extend([data_pb])
        data = container.SerializeToString()
        updated_state = {}
        updated_state[user_address] = data
        self._context.set_state(updated_state, timeout=self._timeout)
