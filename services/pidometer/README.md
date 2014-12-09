# Pidometer #

  
## Требования ##

+   Настроенная среда

    ```bash
    pkgadd -d http://get.opencsw.org/now
    /opt/csw/bin/pkgutil -U
    /opt/csw/bin/pkgutil -i libmcrypt4 mcrypt_dev redis
    pkg install SUNWhea SUNWarc SUNWlibm SUNWlibms SUNWdfbh  SUNWlibC SUNWzlib gcc-43 wget gnu-make
    export CPPFLAGS="-I/opt/csw/include"
    export LDFLAGS="-L/opt/csw/lib -R/opt/csw/lib"
    export PKG_CONFIG_PATH="/opt/csw/lib/pkgconfig"
    
    easy_install redis hiredis python-mcrypt
    ```
    
+   Redis как служба (redis.conf, redis.smf)
+   PYTHONPATH=. ./Server


## Идеи ##

+   Вставить переполнение где-то в Си (C/Api для вычислений)
+   Скопилировать все в Cython (.so), избавиться от .pyx, усложнив анализ библиотеки.
+   Оставить весь сервис дырявым и добавить одну совсем не очевидную уязвимость,
    чтобы команды закрыв много всего расслабились.


## Методы ##

1.  Записать данные за какой-то период.
    1.  Дневной график (дискретизация)
    2.  Количество шагов в день/интенсивность/трек
2.  Считать данные за каждый из промежутков времени
    1.  Количество шагов - public
    2.  Интенсивность шагов или трек - private
3.  Зарегистрироваться
    +   выдать токен
    +   завести пользователя в БД
    +   принимать авторизацию


Тестовый флаг:

    7al10jy3oyn5w5rn4z74nqyb7yfpy4b=


Сейчас сервис очень дырявый, буду постепенно закрываться:

[x] Редис по всем адресам (думаю оставить)
[x]  Редис без авторизации (хз, стоит ли)
[x] Register возвращает токен (оставить закоментированным)
[x]  В принципе, можно понять как делаются токены, и вычислить их (сложно)
[x]  Си почти не используется (надо переписать что-то)

