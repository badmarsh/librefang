import { useEffect, useState } from "react";
import { Card } from "./ui/Card";
import { SectionLabel } from "./ui/SectionLabel";
import { Pill } from "./ui/Pill";

interface AgentEvent {
  agent_id: string;
  kind: string; // "THINKING", "TOOL_CALL", "AWAITING_MEMORY", "DONE"
  timestamp: string;
}

export function MediaDesolatorStatusPanel() {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [status, setStatus] = useState<"connecting" | "connected" | "disconnected">("connecting");

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/api/desolator/monitor`;
    
    let ws: WebSocket;
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    const connect = () => {
      setStatus("connecting");
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setStatus("connected");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // In LibreFang, Event might have a structure. Let's extract what we need.
          // Assuming data has agent_id and a kind or similar
          const newEvt: AgentEvent = {
            agent_id: data.agent_id || data.agent || "unknown",
            kind: data.kind || data.type || "EVENT",
            timestamp: new Date().toISOString(),
          };
          
          setEvents((prev) => [newEvt, ...prev].slice(0, 10)); // Keep last 10
        } catch (e) {
          console.error("Failed to parse websocket event", e);
        }
      };

      ws.onclose = () => {
        setStatus("disconnected");
        reconnectTimeout = setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      if (ws) ws.close();
    };
  }, []);

  return (
    <Card padding="md" className="surface-lit mb-3 lg:mb-4">
      <div className="flex items-center justify-between mb-3">
        <SectionLabel className="!mb-0">Media Desolator Swarm Activity</SectionLabel>
        <Pill kind={status === "connected" ? "running" : status === "connecting" ? "pending" : "error"} size="sm" mono>
          {status}
        </Pill>
      </div>
      
      <div className="space-y-2 max-h-[200px] overflow-y-auto pr-2">
        {events.length === 0 ? (
          <div className="text-xs text-text-dim py-4 text-center">No recent activity</div>
        ) : (
          events.map((evt, i) => (
            <div key={i} className="flex items-center justify-between py-1.5 border-b border-border-subtle last:border-0">
              <div className="flex flex-col">
                <span className="text-[13px] font-medium text-text-main">{evt.agent_id}</span>
                <span className="text-[11px] text-text-dim font-mono">{evt.kind}</span>
              </div>
              <span className="text-[11px] text-text-dim">
                {new Date(evt.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
