import { useState } from "react";
import FileUploader from "../components/FileUploader";
import QuestionInput from "../components/QuestionInput";
import ResponseDisplay from "../components/ResponseDisplay";
import DownloadButton from "../components/DownloadButton";


export default function Home() {
  const [answer, setAnswer] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);

  const uploadPDF = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file); // ✅ Ensure key is "file"

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setSessionId(data.session_id);
    } catch (err) {
      console.error("Upload error:", err);
    }
  };

  const askQuestion = async (question: string) => {
    if (!sessionId) {
      alert("Please upload a PDF first to start a session.");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          question,
          mode: "clause", // or "qa" or "summary"
        }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server Error: ${res.status} - ${errorText}`);
      }

      const data = await res.json();
      console.log("AI Response:", data);
      setAnswer(data.answer);
    } catch (err) {
      console.error("Error asking question:", err);
      setAnswer("❌ Failed to get a response. Please check the console.");
    }
  };

  return (
    <main className="w-[1200px] mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">📚 Legal Clause Assistant</h1>
      <FileUploader onUpload={uploadPDF} />
      <QuestionInput onAsk={askQuestion} />
      <ResponseDisplay answer={answer} />
      {sessionId && <DownloadButton sessionId={sessionId} />}
    </main>
  );
}
