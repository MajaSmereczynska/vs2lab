# Aufgabe 3.1

## Experiment 2

Race-condition welcher Client zuerst dran kommt.  
Clients kommen aber solange dran bis sie STOP senden (for loop auf 30 gesetzt, immer noch erst ein Client dann der andere)

Dann aber direkt (also Temporal und Referenziell gekoppelt)

# Aufgabe 3.2

## Experiment 1

Da es lang genug gedauert hat den zweiten Aufruf von client.py zu starten hat der die erste TIME Nachricht verpasst.

```
b'TIME 17:56:28.354603'
b'TIME 17:56:33.354857'
b'TIME 17:56:38.355165'
b'TIME 17:56:43.355433'
b'TIME 17:56:48.355694'
```
```
b'TIME 17:56:33.354857'
b'TIME 17:56:38.355165'
b'TIME 17:56:43.355433'
b'TIME 17:56:48.355694'
b'TIME 17:56:53.355973'
```

Also Ereignis-basiert

## Experiment 2

client.py empfängt fünf TIME Nachrichten  
client1.py 3 DATE Nachrichten.

client.py empfängt auch schon wenn client1.py noch nicht gestartet ist (wie oben auch schon)

Zwei total unabhängige Ereignis-basierte Busse.

# Aufgabe 3.3

## Experiment 1

Farmer 1 und 2 beenden sich beide sobald die Workload ausgesendet wurde.
Worker wechelt immer ab zwischen Farmer 1 und 2

## Experiment 2

Wird auf Worker verteilt die zum Zeitpunkt von tasksrc.py X Aufruf aktiv sind verteilt. (Wenn 0 Worker dann wartet Farmer audf ersten Worker und gibt dem die gesamte Workload)
Wenn also beide Worker zuerst gestartet werden und dann erst der Farmer bekommen beide Worker je eine Hälfte der Workload.