import argparse
import time
import random
from kafka import KafkaProducer, KafkaConsumer

def main():
    parser = argparse.ArgumentParser(
        description="Segment Prozess mit Kafka-Kommunikation und erweiterten Schikanen"
    )
    parser.add_argument("--id", required=True, help="Segment ID (Kafka-Topic)")
    parser.add_argument("--type", required=True, choices=["start-goal", "normal", "bottleneck", "caesar"],
                        help="Segment Typ")
    parser.add_argument("--next", nargs="+", required=True, help="Nächste Segment-IDs (Kafka-Topics)")
    args = parser.parse_args()

    bootstrap_servers = ['localhost:9093', 'localhost:9095', 'localhost:9097']
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    # Erzeuge eine zufällige Consumer-Gruppe, damit alte Offsets nicht verwendet werden:
    group_id = args.id + "-" + str(random.randint(1000, 9999))
    consumer = KafkaConsumer(
        args.id,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='latest',  # nur neue Nachrichten lesen
        group_id=group_id,
        enable_auto_commit=True,
        value_deserializer=lambda m: m.decode('utf-8')
    )

    if args.type == "start-goal":
        user_input = input(f"Segment {args.id}: Drücke Enter, um das Rennen zu starten...")
        # Kurze Verzögerung, damit alle Consumer sich vollständig anmelden können
        print("Der Streitwagen macht sich bereit..")
        time.sleep(3)
        print(f"Und LOS: Segment {args.id} sendet initial Token an {args.next}")
        for next_seg in args.next:
            producer.send(next_seg, b"TOKEN")
        producer.flush()
    else:
        print(f"Segment {args.id} vom Typ '{args.type}' wartet auf Token...")

    for message in consumer:
        token = message.value
        if args.type == "normal":
            time.sleep(0.5)
            print(f"Segment {args.id} (normal) leitet Token an {args.next} weiter")
        elif args.type == "bottleneck":
            delay = random.uniform(2, 5)
            print(f"Segment {args.id} (bottleneck) blockiert den Weg für {delay:.1f} Sekunden")
            time.sleep(delay)
            print(f"Segment {args.id} (bottleneck) leitet Token an {args.next} weiter")
        elif args.type == "caesar":
            delay = random.uniform(3, 7)
            print(f"Segment {args.id} (caesar) ruft: 'Ave Caesar!' und blockiert den Weg für {delay:.1f} Sekunden")
            time.sleep(delay)
            print(f"Segment {args.id} (caesar) leitet Token an {args.next} weiter")

        for next_seg in args.next:
            producer.send(next_seg, token.encode('utf-8') if isinstance(token, str) else token)
        producer.flush()

if __name__ == "__main__":
    main()
