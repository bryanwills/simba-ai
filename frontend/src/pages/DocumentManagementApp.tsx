import React, { useState } from 'react';
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Toaster } from "@/components/ui/toaster";
import DocumentManagementHeader from '@/components/DocumentManagement/DocumentManagementHeader';
import DocumentList from '@/components/DocumentManagement/DocumentList';
import { DocumentType, DocumentStatsType } from '@/types/document';
import { ingestionApi } from '@/lib/ingestion_api';

const DocumentManagementApp: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const stats: DocumentStatsType = {
    lastQueried: "2 hours ago",
    totalQueries: 145,
    itemsIndexed: documents.length,
    createdAt: "Apr 12, 2024"
  };

  const handleUpload = async (files: FileList) => {
    if (files.length === 0) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please select a file to upload",
      });
      return;
    }

    if (files.length > 5) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Maximum 5 files allowed at once",
      });
      return;
    }

    setIsLoading(true);
    try {
      const file = files[0];
      
      // Check for duplicate
      if (documents.some(doc => doc.name === file.name)) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "A file with this name already exists",
        });
        return;
      }

      const result = await ingestionApi.uploadDocument(file);
      
      setDocuments(prev => [...prev, {
        id: crypto.randomUUID(),
        name: file.name,
        type: file.type.split('/')[1] || file.type,
        size: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
        uploadedAt: new Date().toLocaleDateString()
      }]);

      toast({
        title: "Success",
        description: result.message,
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error.message || "Upload failed. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = (id: string) => {
    setDocuments(docs => docs.filter(doc => doc.id !== id));
  };

  const handleSearch = (query: string) => {
    // Implement search logic
    console.log('Searching:', query);
  };

  return (
    <>
      <div className="p-6 h-full">
        <Card className="bg-white shadow-xl flex flex-col h-full rounded-xl">
          <DocumentManagementHeader stats={stats} />
          <DocumentList
            documents={documents}
            isLoading={isLoading}
            onDelete={handleDelete}
            onSearch={handleSearch}
            onUpload={handleUpload}
          />
        </Card>
      </div>
      <Toaster />
    </>
  );
};

export default DocumentManagementApp; 