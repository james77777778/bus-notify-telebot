# Bus Notify by Telebot
## Environment
- python3.6
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## Steps
1. Create a bot by @botfather
    should get a `token` from @botfather
2. Check `chat_id`
    start conversation with @RawDataBot to find
    ```json
    "message": {
        "chat": {
            "id": 12345678
        }
    }
    ```
3. Write a `secret.json` needed by `main.py`
    ```json
    {
        "token": "token_from_botfather",
        "chat_id": 12345678
    }
    ```
4. Test `main.py`
    ```bash
    python3 main.py [city] [route_name] [stop_name] [direction]
    # ex
    python3 main.py NewTaipei 藍23 樟樹一路口 0
    ```
5. Setup crontab
    ```bash
    crontab -e
    ```
    ex: do the query at 17:30 to 17:59 every 3 mins at workday (Mon-Fri)
    ```bash
    30-59/3 17 * * 1-5 cd path/to/your_repo && venv/bin/python main.py NewTaipei 藍23 樟樹一路口 0 > /tmp/cronlog.txt 2>&1
    # exit by :wq
    ```

## Demo
<img src="docs/demo.png" alt="demo" width="300"/>
