import { Link } from "react-router-dom";

export default function About() {
  return (
    <div className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">About Legal Assistant</h1>
      <p>This tool allows you to upload legal PDFs and ask clause-based questions.</p>
      <Link to="/" className="text-blue-600 underline">← Back to Home</Link>
    </div>
  );
}