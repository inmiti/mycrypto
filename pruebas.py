import requests

r = requests.get('https://rest.coinapi.io/v1/exchangerate/BTC/EUR?apikey=7872A0C1-144C-47DF-96DD-2970F897CF64')
    
print(r.status_code)
print(r.text)

