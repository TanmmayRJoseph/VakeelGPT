import { useState } from "react";

export default function FileUploader({ onUpload }: { onUpload: (file: File) => void }) {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  };

  const handleUpload = () => {
    if (file) onUpload(file);
  };

  return (
    <div className="space-y-4">
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload} className="px-4 py-2 bg-blue-600 text-white rounded">
        Upload PDF
      </button>
    </div>
  );
}