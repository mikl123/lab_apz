Lab Mykhailo Buleshyi

Виконав два додаткових завдання.
1) Зробити retry
2) Зробити комунікацію між facade-service і logging-service та message-service використовуючи gRPC.

Для тестування retry в кореневій папці logging-service є `add_delay = True # needed for retry system check.` який штучно додає delay, щоб тільки третя спроба зареєструвати повідомлення була успішна.

Для gRPC створив окрему папку, з тими самими файлами.

Для тестування всіх підходів створив скрипт `user.py` який робить POST та GET запити до facade-service.
