/**
 * Interview Ace — Answer Panel
 *
 * Displays the Knowledge Agent's suggested answer.
 * Shows confidence score and source references.
 */

interface AnswerResponse {
  question: string;
  answer: string;
  confidence: number;
  sources: string[];
}

export function AnswerPanel({ answer }: { answer: AnswerResponse | null }) {
  if (!answer) {
    return (
      <div className="text-center text-gray-400 py-4">
        💡 Answers will appear here when questions are detected
      </div>
    );
  }

  const confidenceColor =
    answer.confidence > 0.8
      ? "text-green-400"
      : answer.confidence > 0.5
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div className="bg-purple-900/30 rounded-lg p-3 border border-purple-500/30">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-purple-300">💡 Suggested Answer</h2>
        <span className={`text-xs font-mono ${confidenceColor}`}>
          ★ {(answer.confidence * 100).toFixed(0)}% confidence
        </span>
      </div>

      <p className="text-xs text-gray-400 mb-2 italic">Q: {answer.question}</p>
      <p className="text-sm leading-relaxed">{answer.answer}</p>

      {answer.sources.length > 0 && (
        <div className="mt-2 pt-2 border-t border-purple-500/20">
          <p className="text-xs text-gray-500">Sources: {answer.sources.join(", ")}</p>
        </div>
      )}
    </div>
  );
}
