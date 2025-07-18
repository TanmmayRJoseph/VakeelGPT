import { useState } from "react";

export default function QuestionInput({ onAsk }: { onAsk: (question: string) => void }) {
  const [question, setQuestion] = useState("");

  return (
    <div className="space-y-2">
      <input
        type="text"
        placeholder="Ask a legal question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full border px-3 py-2 rounded"
      />
      <button
        onClick={() => onAsk(question)}
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Ask
      </button>
    </div>
  );
}