/**
 * Interview Ace — Transcript Panel
 *
 * Displays real-time transcript with speaker labels.
 * Interviewer messages on the left, candidate's on the right.
 */

interface TranscriptSegment {
  speaker: "interviewer" | "candidate" | "unknown";
  text: string;
  confidence: number;
}

export function TranscriptPanel({ segments }: { segments: TranscriptSegment[] }) {
  if (segments.length === 0) {
    return (
      <div className="text-center text-gray-400 py-8">
        🎤 Waiting for audio...
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
        Live Transcript
      </h2>
      {segments.map((seg, i) => (
        <div
          key={i}
          className={`p-2 rounded-lg text-sm ${
            seg.speaker === "interviewer"
              ? "bg-blue-900/40 mr-8"
              : "bg-green-900/40 ml-8"
          }`}
        >
          <span className="text-xs font-medium text-gray-400">
            {seg.speaker === "interviewer" ? "👤 Interviewer" : "🧑 You"}
          </span>
          <p className="mt-1">{seg.text}</p>
        </div>
      ))}
    </div>
  );
}
