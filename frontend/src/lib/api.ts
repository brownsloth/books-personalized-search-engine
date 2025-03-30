export type BookResult = {
  title: string;
  reason: string;
  source_url: string;
};

export async function searchBooks(query: string): Promise<BookResult[]> {
  const res = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(query)}`);
  const data = await res.json();
  return data.books;
}
