import ChatFrame from '@/components/ChatFrame';
import ChatApp from '@/pages/ChatApp';
import DocumentManagementApp from "@/pages/DocumentManagementApp";
import { Routes, Route } from 'react-router-dom';
import { MainLayout } from '@/MainLayout';

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<ChatApp />} />
        <Route path="/documents" element={<DocumentManagementApp />} />
        <Route path="*" element={<div className="p-8 text-center">Page Not Found</div>} />
      </Route>

      

    </Routes>
  );
}

export default App;
