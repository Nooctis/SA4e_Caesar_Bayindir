# Ave Caesar Rennsimulation

Dieses Repository enthält eine Simulation des Rennspiels "Ave Caesar". Die Anwendung simuliert mehrere Rennstrecken, die aus einer festgelegten Anzahl von Segmenten bestehen. Die Segmente kommunizieren untereinander über einen Kafka-Cluster. Einige Segmente (z. B. Bottleneck und Caesar) verzögern den Tokenfluss, um typische Rennherausforderungen zu simulieren.

## Features

- **Streckengenerierung:**  
  Das Skript `circular-course.py` generiert eine JSON-Konfiguration der Rennstrecken.  
  - Jeder Track beginnt und endet mit einem "start-goal"-Segment.
  - Neben "normalen" Segmenten können auch "bottleneck" und "caesar" Segmente vorkommen.
  - Die Typen "bottleneck" und "caesar" fügen zufällige Verzögerungen ein, um Engpässe zu simulieren.

- **Rennkoordination und Kommunikation:**  
  - Das Skript `config.py` liest die Konfiguration und startet für jedes Segment einen eigenen Prozess.
  - Das Skript `segment.py` implementiert die Logik der Segmente:
    - **start-goal:** Wartet auf manuellen Input (Enter) und sendet dann seinen Token.
    - **normal:** Leitet den Token mit einer kurzen Verzögerung weiter.
    - **bottleneck:** Verzögert den Tokenfluss zufällig (2–5 Sekunden).
    - **caesar:** Verzögert den Tokenfluss zufällig (3–7 Sekunden) und gibt zusätzlich "Ave Caesar!" aus.

- **Kafka-basiertes Messaging:**  
  Die Kommunikation zwischen den Segmenten erfolgt über Kafka (mithilfe der [kafka-python](https://github.com/dpkp/kafka-python) Bibliothek). Ein Kafka-Cluster (drei Broker und ein Zookeeper) wird über Docker Compose gestartet.

## Voraussetzungen

- **Python 3.9 oder höher**
- **Docker und Docker Compose**
- **pip** (zur Installation der Python-Abhängigkeiten)

## Einrichtung und Ausführung

### 1. Repository klonen

```bash
git clone <deine-repo-url>
cd <dein-repo-verzeichnis>
