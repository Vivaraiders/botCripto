from services.cotarMoedas import cotarMoedas

def get_data(moeda):
    try:
        dados = cotarMoedas(moeda)
        if 'code' in dados:
            return None
    
        return{
        'open': float(dados['openPrice']),
        'last': float(dados['lastPrice']),
        'high': float(dados['highPrice']),
        'low': float(dados['lowPrice']),
        'change': float(dados['priceChangePercent'])
        }
    
    except Exception as err:
        print(f'Erro ao buscar {moeda}: {err}')
        return None
