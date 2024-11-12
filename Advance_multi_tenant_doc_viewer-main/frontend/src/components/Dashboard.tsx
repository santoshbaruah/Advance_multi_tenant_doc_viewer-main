import React, { useState } from 'react';
import Navigation from './Navigation';
import FileUpload from './FileUpload';
import SearchBar from './SearchBar';
import DocumentCard from './DocumentCard';
import { Alert, AlertDescription } from '@/components/ui/alert';

const Dashboard: React.FC = () => {
  const [documents] = useState([
    {
      id: 1,
      name: 'Business Proposal.pdf',
      type: 'pdf',
      size: '2.4 MB',
      updatedAt: '2 hours ago'
    },
    {
      id: 2,
      name: 'Project Screenshot.png',
      type: 'image',
      size: '1.1 MB',
      updatedAt: 'Yesterday'
    }
  ]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
          <p className="text-gray-600">Manage and organize your files</p>
        </div>

        <Alert className="mb-8">
          <AlertDescription>
            Your storage is 80% full. Consider upgrading your plan or deleting unused files.
          </AlertDescription>
        </Alert>

        <FileUpload />
        <SearchBar />

        <div className="grid grid-cols-1 gap-4">
          {documents.map(doc => (
            <DocumentCard key={doc.id} document={doc} />
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
