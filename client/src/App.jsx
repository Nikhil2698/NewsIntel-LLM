import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [urls, setUrls] = useState([]);
  const [urlInput, setUrlInput] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]); // State to store sources

  const handleAddUrl = () => {
    if (urlInput) {
      setUrls([...urls, urlInput]);
      setUrlInput('');
    }
  };

  const processUrls = async () => {
    const response = await axios.post('/api/process_urls', { urls });
    console.log(response.data); // Handle the response accordingly
  };

  const handleAskQuestion = async () => {
    try {
      const response = await axios.post('/api/answer_question', { question });
      setAnswer(response.data.answer);
      setSources(response.data.sources || []); // Update sources state
    } catch (error) {
      console.error('Error fetching the answer:', error);
      setAnswer('Failed to fetch the answer');
      setSources([]);
    }
  };

  return (
    <div className="App">
      <div>
        <input value={urlInput} onChange={e => setUrlInput(e.target.value)} placeholder="Enter URL" />
        <button onClick={handleAddUrl}>Add URL</button>
        <button onClick={processUrls}>Process URLs</button>
        {urls.map(url => (<div key={url}>{url}</div>))}
      </div>
      <div>
        <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask a question" />
        <button onClick={handleAskQuestion}>Submit Question</button>
        <div>Answer: {answer}</div>
        {sources.length > 0 && (
          <div>
            <h3>Sources:</h3>
            <ul>
              {sources.map((source, index) => (
                <li key={index}>{source}</li>  // Assuming sources are strings (URLs)
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
