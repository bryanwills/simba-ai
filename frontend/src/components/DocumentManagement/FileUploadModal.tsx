import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { Upload } from "lucide-react"

interface FileUploadModalProps {
  isOpen: boolean
  onClose: () => void
  onUpload: (files: FileList) => void
}

export function FileUploadModal({ isOpen, onClose, onUpload }: FileUploadModalProps) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files)
      onClose()
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files)
      onClose()
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add items</DialogTitle>
          <DialogDescription>
            Add files to this capsule. Allowed file types are text files like PDF, DOCX, TXT, etc. Maximum file size is 200MB.
          </DialogDescription>
        </DialogHeader>
        <div
          className={`mt-4 grid place-items-center border-2 border-dashed rounded-lg h-52 ${
            dragActive ? "border-primary" : "border-gray-300"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <Upload className="w-10 h-10 mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-600">
              Drag and drop files here, or click to browse
            </p>
          </div>
        </div>
        <DialogFooter className="flex justify-between">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <div>
            <Input
              id="file-upload"
              type="file"
              multiple
              className="hidden"
              onChange={handleChange}
              accept=".pdf,.doc,.docx,.txt,.md"
            />
            <Button onClick={() => document.getElementById('file-upload')?.click()}>
              Browse files
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 