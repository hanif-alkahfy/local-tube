import { Download } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-red-500 p-4 flex items-center justify-between">
      <div className="w-full max-w-xl mx-auto flex items-center gap-2 bg-white rounded-full px-4 py-2">
        <input
          type="text"
          placeholder="Search videos..."
          className="flex-grow outline-none text-sm"
        />
        <button className="text-gray-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-5 h-5"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z"
            />
          </svg>
        </button>
      </div>

      <button className="text-white mr-5">
        <Download className="w-5 h-5" />
      </button>
    </header>
  );
}
