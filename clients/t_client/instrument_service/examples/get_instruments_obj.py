"""Show instrument object"""

from pprint import pprint

from clients.t_client.instrument_service.instruments_id_types import (
    InstrumentsIdTypes,
)
from clients.t_client.instrument_service.instruments_servise import (
    InstrumentsService,
)

cli = InstrumentsService()

resp = cli.get_instrument_by(
    "TRNFP", InstrumentsIdTypes.INSTRUMENT_ID_TYPE_TICKER, class_code="TQBR"
)
# resp = cli.get_instrument_by('FUTASTR06250', InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI)
# resp = cli.get_futures_by('FUTASTR06250', InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI)
pprint(resp)
