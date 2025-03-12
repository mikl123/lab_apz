Lab Mykhailo Buleshyi

Виконав два додаткових завдання.
1) Зробити retry
2) Зробити комунікацію між facade-service і logging-service та message-service використовуючи gRPC.

Для тестування retry в кореневій папці logging-service є `add_delay = True # needed for retry system check.` який штучно додає delay, щоб тільки третя спроба зареєструвати повідомлення була успішна.

Для gRPC створив окрему папку, з тими самими файлами.

Для тестування всіх підходів створив скрипт `user.py` який робить POST та GET запити до facade-service.

Як запустити?
1) python -m venv venv
2) ./venv/Script/activate
3) pip install -r requirements.txt
4) python facade-service.py
5) python logging-service.py
6) python message-service.py
7) python user.py

   
