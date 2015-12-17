# EvS MicroServices and Security

Main topic: MicroService architecture concepts and the urge for proper security. Provides a presentation, term paper and demonstration code.


## Architecture

These are the three parts of this microservice and security demonstration.

### frontend

A [React][6] rich internet application to communicate with the microservices.

### microservice1

An image processing service written with [Python][4] and [Flask][3].

### microservice2

A storage service which communicates with [MongoDB][5] via [PHP][2] and [Silex][1].

## Grobe Gliederungsideen:
1. Einführung (Corny) ~4S
  * Was ist ein Microservice?
  * Aufbrechen des Monolithen (Parallelen zu MAS)
  * Motivation Microservices und Sicherheit
  * Ausführungsumgebung (lokal, im Netzwerk verteilt, global verteilt, ?)
2. Microservice-Architekturen und Sicherheit (Felix) ~4S
  * thread-/prozessbasiert
  * VM / Docker
  * Kubernetes, Mesos, EC2, Azure...
3. Kommunikation und Sicherheit (Felix) ~4S
  * Queueing (RabbitMQ, ?)
  * RESTful (HTTP, TCP/UDP, ?)
4. Schutzziele (Corny) ~4S
  * Vertraulichkeit
  * Handshake-basiertes Verfahren (OAuth2, ?)
  * tokenbasiertes Authentifikationsverfahren (JWT, ?)
  * Verfügbarkeit
  * Integrität
  * TLS
5. Demo ~1S
  * Microservice bauen
  * Reden sicher.
6. Zusammenfassung / Literatur (~3S)


[1]: http://silex.sensiolabs.org/
[2]: http://php.net/
[3]: http://flask.pocoo.org/
[4]: https://www.python.org/
[5]: https://www.mongodb.org/
[6]: https://facebook.github.io/react/
