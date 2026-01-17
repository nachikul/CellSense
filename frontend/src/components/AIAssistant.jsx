import React, { useState } from 'react';
import axios from 'axios';
import './AIAssistant.css';

function AIAssistant({ dataId }) {
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userQuestion = question;
    setQuestion('');
    setLoading(true);

    // Add user question to conversation
    setConversation(prev => [...prev, { type: 'question', text: userQuestion }]);

    try {
      const response = await axios.post('/api/ask-ai', {
        data_id: dataId,
        question: userQuestion
      });

      // Add AI response to conversation
      setConversation(prev => [...prev, { 
        type: 'answer', 
        text: response.data.answer,
        source: response.data.source
      }]);
    } catch (error) {
      setConversation(prev => [...prev, { 
        type: 'error', 
        text: 'Sorry, I couldn\'t process your question. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What's my total income?",
    "How much did I spend?",
    "What are my top spending categories?",
    "What's my savings balance?",
    "Show me a summary of my finances"
  ];

  return (
    <div className="ai-assistant">
      <div className="ai-header">
        <h3>🤖 AI Financial Assistant</h3>
        <p>Ask questions about your finances in plain English</p>
      </div>

      <div className="conversation">
        {conversation.length === 0 ? (
          <div className="welcome-message">
            <p>👋 Hello! I can help you understand your financial data.</p>
            <p className="suggested-label">Try asking:</p>
            <div className="suggested-questions">
              {suggestedQuestions.map((q, idx) => (
                <button
                  key={idx}
                  className="suggested-btn"
                  onClick={() => setQuestion(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          conversation.map((item, idx) => (
            <div key={idx} className={`message ${item.type}`}>
              {item.type === 'question' && <span className="label">You:</span>}
              {item.type === 'answer' && <span className="label">AI:</span>}
              <p>{item.text}</p>
              {item.source && <span className="source">{item.source}</span>}
            </div>
          ))
        )}
        {loading && (
          <div className="message answer loading-msg">
            <span className="label">AI:</span>
            <p>Thinking...</p>
          </div>
        )}
      </div>

      <form onSubmit={handleAskQuestion} className="question-form">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your finances..."
          className="question-input"
          disabled={loading}
        />
        <button 
          type="submit" 
          className="ask-btn"
          disabled={loading || !question.trim()}
        >
          {loading ? '⏳' : '📤'} Ask
        </button>
      </form>
    </div>
  );
}

export default AIAssistant;
