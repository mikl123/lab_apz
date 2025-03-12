Lab Mykhailo Buleshyi

Виконав додаткове завдання.
1) Зробити окремий сервіс для визначення ip.

Для тестування всіх підходів створив скрипт `user.py` який робить POST та GET запити до facade-service.

Як запустити?
1) python -m venv venv
2) ./venv/Script/activate
3) pip install -r requirements.txt
4) python facade-service.py
5) python logging-service.py -- port 5001
6) python logging-service.py -- port 5002
7) python logging-service.py -- port 5003
8) python message-service.py
9) python config-server.py
10) python user.py

Якщо обрано інші порти для logging-service тоді доведеться змінити ip-config.json
