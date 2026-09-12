import Link from "next/link";
import type { Event } from "@/lib/types";

export function EventCard({ event }: { event: Event }) {
  const time = new Date(event.latest_confirmation);
  return (
    <Link
      className="event-row"
      href={`/app/events/${event.id}`}
      style={{ gridTemplateColumns: "76px minmax(0,1fr) 96px" }}
    >
      <div className="timestamp">
        {time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        <br />
        <span>{time.toLocaleDateString()}</span>
      </div>
      <div>
        <div className="event-title">{event.title}</div>
        <div className="event-explain">{event.explanation}</div>
        <div className="chips">
          <span className="chip">{event.event_type}</span>
          {event.topics.slice(0, 3).map((topic) => (
            <span className="chip" key={topic}>
              {topic}
            </span>
          ))}
        </div>
      </div>
      <div className="score">
        <strong>{Math.round(event.confidence * 100)}%</strong>
        confidence
        <br />
        {event.source_count} sources
      </div>
    </Link>
  );
}
