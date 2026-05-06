/**
 * Interview Ace — WebSocket Hook
 *
 * Manages WebSocket connection to the backend.
 * Handles reconnection, message parsing, and state management.
 */

import { useState, useEffect, useRef, useCallback } from "react";

interface TranscriptSegment {
  speaker: "interviewer" | "candidate" | "unknown";
  text: string;
  confidence: number;
}

interface AnswerResponse {
  question: string;
  answer: string;
  confidence: number;
  sources: string[];
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [transcripts, setTranscripts] = useState<TranscriptSegment[]>([]);
  const [latestAnswer, setLatestAnswer] = useState<AnswerResponse | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onerror = () => setIsConnected(false);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case "transcript":
          setTranscripts((prev) => [...prev, data.payload]);
          break;
        case "answer":
          setLatestAnswer(data.payload);
          break;
        case "status":
          console.log("Status:", data.payload);
          break;
      }
    };

    return () => ws.close();
  }, [url]);

  const sendMessage = useCallback((message: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  return { isConnected, transcripts, latestAnswer, sendMessage };
}
