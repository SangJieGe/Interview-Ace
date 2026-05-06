/**
 * Interview Ace — Toolbar
 *
 * Bottom toolbar with control buttons.
 */

interface ToolbarProps {
  onToggleListening: () => void;
  isConnected: boolean;
}

export function Toolbar({ onToggleListening, isConnected }: ToolbarProps) {
  return (
    <div className="flex items-center justify-around px-4 py-2 bg-gray-800/80">
      <button
        onClick={onToggleListening}
        disabled={!isConnected}
        className="px-4 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium transition-colors"
      >
        🎙️ Toggle Listening
      </button>
      <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors" title="Upload Document">
        📄
      </button>
      <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors" title="Settings">
        ⚙️
      </button>
      <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors" title="Statistics">
        📊
      </button>
    </div>
  );
}
