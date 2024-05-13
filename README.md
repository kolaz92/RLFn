# RLFn
Return latin fullname bot

# Инструкция по запуску

1. Установить docker (https://docs.docker.com/engine/install/)
2. Скачать папку с кодом. В файл dockerfile вставить свой токен телеграмм бота
3. Открыть папку с кодом в терминале, создать docker образ командой (могут потребоваться права суперпользователя)

```
$ docker bulid .
$ docker images
```

4. Скопируйте IMAGE IG последнего образа и запустите контейнер командой 

```
$ docker bulid .
$ docker run -d -p 80:80 <IMAGE_ID>
```

5. Откройте телеграмм и протестируйте работу бота 
