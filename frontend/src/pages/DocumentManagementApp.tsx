import React, { useState } from 'react';
import { Card } from "@/components/ui/card";
import DocumentManagementHeader from '@/components/DocumentManagement/DocumentManagementHeader';
import DocumentList from '@/components/DocumentManagement/DocumentList';
import { DocumentType, DocumentStatsType } from '@/types/document';

const DocumentManagementApp: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentType[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const stats: DocumentStatsType = {
    lastQueried: "2 hours ago",
    totalQueries: 145,
    itemsIndexed: documents.length,
    createdAt: "Apr 12, 2024"
  };

  const handleUpload = (files: FileList) => {
    const newDocs: DocumentType[] = Array.from(files).map(file => ({
      id: crypto.randomUUID(),
      name: file.name,
      type: file.type.split('/')[1] || file.type,
      size: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
      uploadedAt: new Date().toLocaleDateString()
    }));

    setDocuments(prev => [...prev, ...newDocs]);
  };

  const handleDelete = (id: string) => {
    setDocuments(docs => docs.filter(doc => doc.id !== id));
  };

  const handleSearch = (query: string) => {
    // Implement search logic
    console.log('Searching:', query);
  };

  return (
    <div className="p-6 h-full">
      <Card className="bg-white shadow-xl flex flex-col h-full rounded-xl">
        <DocumentManagementHeader 
            stats={stats}
        />
        <DocumentList
          documents={documents}
          isLoading={isLoading}
          onDelete={handleDelete}
          onSearch={handleSearch}
          onUpload={handleUpload}
        />
      </Card>
    </div>
  );
};

export default DocumentManagementApp; 