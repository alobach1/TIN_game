# Uruchomienie:
```
$ python3 python_client.py < port >
```
## Klient łączy się z serwerem za pomoćą 3 wątków:
``` 
    plik network.py
```

 * **tcp_thread**  -  uruchamia wątek tcp_sending, oczekuję od serwera pakietu start albo  stop poprzez socket TCP
 * **udp_thread**   -  przejmuje pakiety poprzez socket UDP od serwera o stanie gry
 * **tcp_sending**  -  wysyła pakiety do serwera poprzez socket TCP dla utrzymania połączenia

