# **Book Suggestion Search Engine (Reddit-powered)**

## **Overview**

This project is an experimental search engine that helps users discover books based on natural language queries. It pulls data from real user posts and comments on the [r/suggestmeabook](https://www.reddit.com/r/suggestmeabook/) subreddit, where users request book suggestions and the community responds with recommendations.

At present, the system indexes Reddit posts using semantic search via [FAISS](https://github.com/facebookresearch/faiss) and [Sentence Transformers](https://www.sbert.net/), then surfaces book recommendations based on related posts and extracted book titles.

## **✅ Features Implemented**

### **🔍 Semantic Search Engine**

- We use the all-MiniLM-L6-v2 SentenceTransformer model to encode user queries and subreddit posts.  

- FAISS is used to perform approximate nearest neighbor search over vectorized Reddit posts.  

- Top-matching posts are used to extract book titles mentioned in comments or post body.  

### **📚 Book Extraction**

- Extracted book titles are matched using string heuristics from post comments or bodies.  

- Associated reasons are extracted from the original comment mentioning the book (if available).  

### **🌐 Frontend**

- Simple frontend UI (Next.js + Tailwind) allows:  
  - Freeform natural language search (e.g., "recommend a dark psychological thriller").  

  - Displays top 5 book suggestions with title, reasoning (if found), and source link.  

  - Styled result components for better readability.  

## **🚧 Current Limitations**

### **1\. Book Title Extraction is Heuristic**

- We do not yet use a robust NLP pipeline or external validation to confirm if a phrase is an actual book.  

- Results may include false positives (non-book phrases) or miss valid titles.  

### **2\. Ranking is Static**

- FAISS ranks related Reddit posts, but the actual book ranking within a result is based purely on frequency — not learned from user behavior.  

- No personalization or active learning is currently implemented.  

### **3\. No Feedback Loop**

- There's no way for the user to mark whether a recommendation was relevant or not.  

- We're not learning over time which suggestions work better.  

## **🧪 Planned Improvements**

### **✍️ Better Book Extraction**

- Use known book title databases (Google Books API, Open Library, etc.) to validate and match titles using fuzzy matching or BERT-based span extraction.  

- Discard invalid matches and ambiguous titles early.  

### **💡 Feedback Collection**

- Add a feedback logging endpoint (/feedback) to capture whether users found a suggestion helpful.  

- Track which queries lead to which books and how users rated them.  

### **🤖 Learning to Rank**

- Train a lightweight ML model (e.g. logistic regression, LambdaMART, or a neural ranker) on feedback data.  

- Features could include:  
  - Query → Post similarity  

  - Post → Book comment relevance  

  - Prior frequency/popularity  

  - Community upvotes  

### **📈 Dashboard**

- Add a dashboard to monitor:  
  - Most common search terms  

  - Most liked/disliked books  

  - System performance over time  

## **🧰 Setup Instructions**

### **Backend**

bash

CopyEdit

\# From the project root

cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

\# Run the API

uvicorn search_api:app --reload

### **Frontend**

bash

CopyEdit

cd frontend

npm install

npm run dev

## **🧠 Summary**

This project is a strong **foundation** for a smarter recommendation tool based on community knowledge. While current retrieval and ranking are static and heuristic, the framework allows for rapid extension into a learning-based and feedback-driven engine.

We’ve built:

- A working FAISS + SentenceTransformer search engine  

- A book extraction mechanism from real Reddit discussions  

- A basic frontend interface for end-to-end interaction  

Next, we aim to:

- Improve extraction quality  

- Log user feedback  

- Learn from interaction to continuously improve