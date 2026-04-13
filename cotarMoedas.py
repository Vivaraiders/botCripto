import requests

def cotarMoedas(simbolo: str):
    try:
        re = requests.get(url=f'https://api.binance.com/api/v3/ticker/price?symbol={simbolo}')
        data = re.json()
        return data

    except Exception as e:
        return {'erro': str(e)}
    