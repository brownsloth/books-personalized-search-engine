type BookResultProps = {
  book: {
    title: string;
    reason?: string;
    source_url?: string;
  };
};

export default function BookResult({ book }: BookResultProps) {
  return (
    <div className="border border-gray-700 p-4 rounded bg-gray-800 text-white shadow space-y-2">
      <h3 className="text-lg font-semibold">{book.title}</h3>
      {book.reason && <p className="text-sm text-gray-300 italic">"{book.reason}"</p>}
      {book.source_url && (
        <a
          href={book.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:underline text-sm"
        >
          View on Reddit
        </a>
      )}
    </div>
  );
}
