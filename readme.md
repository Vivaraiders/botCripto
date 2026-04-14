# Bot Cripto

Bot de Telegram para monitoramento de criptomoedas com alertas em tempo real.

---

## Funcionalidades

* Monitoramento de preços (BTC, ETH, etc)
* Alertas automáticos
* Suporte a múltiplos usuários
* Integração com banco de dados

---

## Tecnologias

* Python
* Telegram Bot API
* MySQL
* Asyncio

---

## Estrutura do Projeto

```
BOTCRIPTO/
│
├── bot/
│   └── telegram_bot.py
│
├── services/
│   ├── cotarMoedas.py
│   ├── merket_data.py
│
├── database/
│   ├── database.py
│   ├── users.py
│   ├── coins.py
│
├── alerts/
│   └── checker.py
│
├── main.py
├── .env
└── README.md
```

---

## Como rodar

```bash
pip install python-telegram-bot python-dotenv
python main.py
```

---

## Como funciona

* Usuário envia uma moeda (ex: BTCBRL)
* Bot salva no banco de dados
* Sistema monitora preços
* Envia alerta quando a condição é atendida

---

## Autor

Samuel Augusto
