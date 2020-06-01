import datetime
import time
import logging
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from addressing import addresser

from protobuf import payload_pb2

from tp.payload import SupplyPayload
from tp.state import SupplyState

SYNC_TOLERANCE = 60 * 5
LOGGER = logging.getLogger(__name__)


class SupplyHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def family_versions(self):
        return [addresser.FAMILY_VERSION]

    @property
    def namespaces(self):
        return [addresser.NAMESPACE]

    def apply(self, transaction, context):
        header = transaction.header
        payload = SupplyPayload(transaction.payload)
        state = SupplyState(context)
        if payload.action == payload_pb2.SimpleSupplyPayload.SYNCHRONIZE_DATA:
            _synchronize_data(
                state=state,
                public_key=header.signer_public_key,
                payload=payload)


def _synchronize_data(state, public_key, payload):
    state.set_data(
        public_key=public_key,
        data=payload.data.data,
    )
