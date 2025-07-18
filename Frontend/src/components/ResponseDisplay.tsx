export default function ResponseDisplay({ answer }: { answer: string }) {
  if (!answer) return null;
  return (
    <div className="w-full bg-gray-100 p-4 rounded shadow">
      <h2 className="text-lg font-semibold mb-2">Explanation</h2>
      <p>{answer}</p>
    </div>
  );
}