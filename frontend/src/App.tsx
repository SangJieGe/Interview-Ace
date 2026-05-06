/**
 * Interview Ace — Main Application Component
 *
 * Layout:
 * ┌──────────────────────────┐
 * │  🎙️ Interview Ace    [—] │  ← Header (drag area)
 * ├──────────────────────────┤
 * │                          │
 * │  Live Transcript         │  ← Real-time transcript
 * │  ────────────────        │
 * │  Q: "Tell me about..."  │
 * │  A: "Based on my..."    │
 * │                          │
 * ├──────────────────────────┤
 * │  Suggested Answer        │  ← Knowledge Agent output
 * │  ★ Confidence: 92%      │
 * │  "I have 5 years of..." │
 * ├──────────────────────────┤
 * │  ⚙️  📄  🎤  📊        │  ← Bottom toolbar
 * └──────────────────────────┘
 */

import { useWebSocket } from "./hooks/useWebSocket";
import { TranscriptPanel } from "./components/TranscriptPanel";
import { AnswerPanel } from "./components/AnswerPanel";
import { Toolbar } from "./components/Toolbar";

export default function App() {
  const { transcripts, latestAnswer, isConnected, sendMessage } =
    useWebSocket("ws://localhost:8000/ws/interview");

  return (
    <div className="flex flex-col h-screen bg-gray-900/90 text-white rounded-xl overflow-hidden backdrop-blur-sm">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-2 bg-gray-800/80 cursor-move">
        <span className="font-semibold">🎙️ Interview Ace</span>
        <div className="flex gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              isConnected ? "bg-green-400" : "bg-red-400"
            }`}
          />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-3 space-y-3">
        <TranscriptPanel segments={transcripts} />
        <AnswerPanel answer={latestAnswer} />
      </main>

      {/* Toolbar */}
      <Toolbar
        onToggleListening={() => sendMessage({ type: "toggle_listening" })}
        isConnected={isConnected}
      />
    </div>
  );
}
