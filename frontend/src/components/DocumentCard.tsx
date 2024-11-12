import React from 'react';
import { FileText, Image, File, MoreVertical, Download, Trash2, Eye } from 'lucide-react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

interface Document {
  id: number;
  name: string;
  type: string;
  size: string;
  updatedAt: string;
}

const DocumentCard: React.FC<{ document: Document }> = ({ document }) => {
  const getIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="w-8 h-8 text-red-500" />;
      case 'image': return <Image className="w-8 h-8 text-green-500" />;
      default: return <File className="w-8 h-8 text-gray-500" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {getIcon(document.type)}
          <div>
            <h4 className="font-medium text-gray-900">{document.name}</h4>
            <p className="text-sm text-gray-500">
              {document.size} • {document.updatedAt}
            </p>
          </div>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger className="p-2 hover:bg-gray-100 rounded-full">
            <MoreVertical className="w-4 h-4 text-gray-500" />
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem className="flex items-center space-x-2">
              <Eye className="w-4 h-4" />
              <span>Preview</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Download</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="flex items-center space-x-2 text-red-600">
              <Trash2 className="w-4 h-4" />
              <span>Delete</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};

export default DocumentCard;
