"""account service"""

from tinkoff.invest import Client

from env.config import TOKEN


def get_account_data():
    """get brokerage accounts info"""

    with Client(TOKEN) as client:
        data = client.users.get_accounts()
    return data
