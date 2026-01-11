import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!inputText) return;
    setIsLoading(true);
    setError('');

    try {
      // Call our Python Backend
      const response = await axios.post('https://fermentatively-semivitreous-johanna.ngrok-free.dev/generate', 
        { text: inputText },
        { responseType: 'blob' } // Important: We expect a file, not JSON
      );

      // Create a URL for the PDF blob and open it
      const file = new Blob([response.data], { type: 'application/pdf' });
      const fileURL = URL.createObjectURL(file);
      window.open(fileURL, '_blank');
      
    } catch (err) {
      setError('Failed to generate report. Is the backend running?');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>ProDoc<span>Engine</span></h1>
        <p>Automated Corporate Documentation Platform</p>
      </header>

      <main className="main-content">
        <div className="card">
          <label>Document Input</label>
          <textarea 
            placeholder="Enter a topic (e.g., 'Launch Strategy for Coffee Shop') OR paste your rough notes..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isLoading}
          />
          
          <div className="actions">
            <button 
              className={`generate-btn ${isLoading ? 'loading' : ''}`} 
              onClick={handleGenerate}
              disabled={isLoading}
            >
              {isLoading ? 'Processing Engine...' : 'Generate Professional PDF'}
            </button>
          </div>
          
          {error && <div className="error-msg">{error}</div>}
        </div>
      </main>
    </div>
  );
}

export default App;