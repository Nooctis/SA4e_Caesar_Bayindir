import argparse
import time
import redis


def main():
    parser = argparse.ArgumentParser(description="Segment Prozess mit Redis-Kommunikation")
    parser.add_argument("--id", required=True, help="Segment ID")
    parser.add_argument("--type", required=True, choices=["start-goal", "normal"], help="Segment Typ")
    parser.add_argument("--next", nargs="+", required=True, help="Nächste Segment IDs")
    args = parser.parse_args()

    # Verbindung zum Redis-Server (Standard: localhost:6379)
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    # Abonniere den eigenen Kanal
    pubsub.subscribe(args.id)

    if args.type == "start-goal":
        # Startbefehl per CLI: Warten auf Enter
        input(f"Segment {args.id}: Drücke Enter, um das Rennen zu starten...")
        print(f"Segment {args.id} sendet initial Token an {args.next}")
        for next_seg in args.next:
            r.publish(next_seg, "TOKEN")

    # Endlosschleife: Warte auf eingehende Token
    for message in pubsub.listen():
        # Überspringe andere Nachrichten (z.B. Subscribe-Bestätigungen)
        if message['type'] != 'message':
            continue
        token = message['data']
        print(f"Segment {args.id} empfängt Token: {token}")
        # Simuliere eine kleine Verarbeitungszeit
        time.sleep(0.5)
        for next_seg in args.next:
            print(f"Segment {args.id} leitet Token an {next_seg} weiter")
            r.publish(next_seg, token)


if __name__ == "__main__":
    main()
