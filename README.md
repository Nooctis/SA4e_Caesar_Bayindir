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
git clone https://github.com/Nooctis/SA4e_Caesar_Bayindir.git
cd <repo-verzeichnis>
```

### 2. Python-Requirements installieren

```bash
pip install -r requirements.txt
```

### 3. Kafka-Cluster starten

Die Anwendung verwendet Kafka als Messaging-Backend. Der Kafka-Cluster wird über die Datei `docker-compose.yml` bereitgestellt.

# 3.1 Cluster starten:

```bash
docker-compose up -d
```

# 3.2 Cluster-Status überprüfen:

```bash
docker-compose ps
```

Es sollten Container für `zookeeper`, `kafka1`, `kafka2` und `kafka3` als "Running" angezeigt werden.

Hinweis:
In der Konfiguration werden zwei Listener pro Broker verwendet:

- INTERNAL: Für die Kommunikation innerhalb des Clusters (über die Containernamen).

- EXTERNAL: Für Verbindungen von außen (auf Ports 9093, 9095, 9097).

### 4. Rennstrecken-Konfiguration generieren

Erzeuge mit dem Streckengenerator eine JSON-Konfigurationsdatei. Beispiel: Erstelle 3 Tracks mit jeweils 6 Segmenten:

```bash
python circular-course.py 3 6 tracks.json
```

### 5. Rennen starten

Starte den zentralen Konfigurationsprozess, der für jedes Segment einen eigenen Prozess startet:

```bash
python config.py tracks.json
```

# Start-goal Segmente:

Jedes start-goal Segment wartet auf den manuellen Input (Enter). Wichtig:
Es ist zu beachten, dass alle Segmentprozesse parallel laufen. Wenn du zu schnell Enter drückst, kann es passieren, dass nicht alle Kafka-Consumer vollständig angemeldet sind. Es wurde jedoch ein Delay von 3 Sekunden nach dem Enter hinzugefügt, um dem Vorzubeugen.

# Weitere Segmente:

Je nach Segmenttyp wird der Token weitergegeben:

normal: Leitet den Token nach einer kurzen Verzögerung weiter.

bottleneck: Verzögert den Tokenfluss zufällig (2–5 Sekunden).

caesar: Verzögert den Tokenfluss zufällig (3–7 Sekunden) und gibt zusätzlich "Ave Caesar!" aus.

