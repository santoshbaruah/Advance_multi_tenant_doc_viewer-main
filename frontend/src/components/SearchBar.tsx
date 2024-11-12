import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';

const SearchBar: React.FC = () => {
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  return (
    <div className="mb-8">
      <div className="flex items-center space-x-4">
        <div className="flex-1 relative">
          <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search documents..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          onClick={() => setIsFilterOpen(!isFilterOpen)}
          className="px-4 py-2 border border-gray-300 rounded-lg flex items-center space-x-2 hover:bg-gray-50"
        >
          <Filter className="w-4 h-4" />
          <span>Filters</span>
        </button>
      </div>

      {isFilterOpen && (
        <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <select className="block w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="">All Types</option>
              <option value="pdf">PDF</option>
              <option value="docx">Word</option>
              <option value="image">Images</option>
            </select>
            <input
              type="date"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Start Date"
            />
            <input
              type="date"
              className="block w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="End Date"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
