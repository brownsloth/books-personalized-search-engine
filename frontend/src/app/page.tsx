"use client";

import { useState } from "react";
import { searchBooks } from "@/lib/api";
import BookResult from "@/components/BookResult";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const books = await searchBooks(query);
    setResults(books);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-12">
      <h1 className="text-3xl font-bold mb-6 text-center">📚 Book Recommender</h1>

      <div className="max-w-xl mx-auto">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="e.g. Looking for a space opera with emotional depth"
          className="w-full p-3 rounded bg-gray-800 text-white border border-gray-600"
        />
        <button
          onClick={handleSearch}
          className="mt-4 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded text-white"
          disabled={loading}
        >
          {loading ? "Searching..." : "Find Books"}
        </button>

        <div className="mt-8 space-y-4">
          {results.map((book, idx) => (
            <BookResult key={idx} book={book} />
          ))}
        </div>
      </div>
    </main>
  );
}
