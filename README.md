# EvS MicroServices and Security

Main topic: MicroService architecture concepts and the urge for proper security. Provides a presentation, term paper and demonstration code.


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
