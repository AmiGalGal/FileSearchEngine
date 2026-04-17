# SeekAll
SeekAll is a unified local semantic search engine that lets you search through your entire file library — images, videos, and documents — using natural language queries instead of filenames or tags.
It runs completely offline on your machine — no APIs, no cloud services, and no internet required.

---

## 🔍 How it works

**Images**
- Images are encoded into 512-dimensional vectors using CLIP's image encoder
- When you search, your query is encoded using CLIP's text encoder into the same space
- Results are ranked by cosine similarity

**Videos**
- Videos are sampled at 1 frame per second using OpenCV
- Each frame is encoded into a 512-dimensional vector using CLIP's image encoder
- Per-frame vectors are averaged into a single representative vector per video

**Documents**
- Documents are split into chunks of 300 words with 50-word overlap
- Each chunk is encoded into a 384-dimensional vector using `all-MiniLM-L6-v2`
- The most relevant chunk per document is used for ranking

**At query time**
- Your natural language query is encoded separately for each modality
- Each modality is searched independently and scores are normalized
- Results from all three are merged and returned to the user ranked by relevance

---

## 📁 Supported file types

**Images**
- `.jpg` / `.jpeg` / `.jfif`
- `.png`
- `.webp`
- `.bmp`

**Videos**
- `.mp4`
- `.avi`
- `.mov`
- `.mkv`
- `.webm`

**Documents**
- `.pdf`
- `.docx`
- `.pptx`
- `.txt`
- `.md`

---

## ⚙️ Features
- Fully local search engine — no internet required
- Semantic search using natural language (not filename or tag based)
- Images and videos powered by OpenAI CLIP
- Documents powered by `sentence-transformers` (`all-MiniLM-L6-v2`)
- Unified results across all three modalities in a single query
- Returns top-K most relevant results
- Simple GUI built with Tkinter
- No external APIs required

---

## 🖥️ Interface
A simple Tkinter GUI allows you to:
- Search your entire file library using plain English queries
- Filter results by file type (images, videos, documents)
- View matching file paths
- Preview top results directly in the interface

---

## 🗂️ How indexing works
```
your-folder/
    ├── photos/         → CLIP image encoder      → image_index.json
    ├── videos/         → CLIP image encoder      → video_index.json
    └── documents/      → all-MiniLM-L6-v2        → doc_index.json
```
Each modality is indexed and stored separately. You can re-index any modality independently without affecting the others.

---

## 📌 Notes
SeekAll runs three independent search engines under the hood — one per modality — and merges their results at query time. Because CLIP and `all-MiniLM-L6-v2` operate in different vector spaces, scores are normalized within each modality before being combined.

> **Note:** JSON storage works well for small to medium collections. For large libraries, serializing high-dimensional float vectors as plain text is not storage-efficient — migration to a binary format or a dedicated vector store such as ChromaDB is recommended at scale.
