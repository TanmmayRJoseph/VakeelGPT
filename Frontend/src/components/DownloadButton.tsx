import { useState } from "react";

const DownloadButton = ({ sessionId }: { sessionId: string }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `http://localhost:8000/download-summary/?session_id=${sessionId}`
      );

      if (!res.ok) {
        throw new Error("Failed to fetch download link.");
      }

      const data = await res.json();

      if (!data.download_link) {
        throw new Error("No download link found in response.");
      }

      const downloadUrl = `http://localhost:8000${data.download_link}`;
      window.open(downloadUrl, "_blank");
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        onClick={handleDownload}
        disabled={isLoading}
      >
        {isLoading ? "Preparing..." : "📥 Download Summary PDF"}
      </button>
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  );
};

export default DownloadButton;
