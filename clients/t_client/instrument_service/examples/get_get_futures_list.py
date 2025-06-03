"""Show futures list with filter by base instrument name"""

from pprint import pprint

from clients.t_client.instrument_service.instruments_servise import (
    InstrumentsService,
)

futures_list = InstrumentsService().get_futures_list()

filtered_list = [item for item in futures_list if "транснеф" in item.name.lower()]

pprint(filtered_list)
