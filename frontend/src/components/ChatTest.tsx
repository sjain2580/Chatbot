import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatTest.css';

const API_BASE_URL = 'https://ai-chatbot-backend-60yq.onrender.com';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  responseTime?: number;
  tokenCount?: number;
}

interface Conversation {
  id: string;
  name: string;
  messages: Message[];
  category: string;
}

interface ChatResponse {
  content: string;
  response_time: number;
  token_count: number;
}

const ChatTest: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([
    { id: '1', name: 'General Chat', messages: [], category: 'general' }
  ]);
  const [activeConvId, setActiveConvId] = useState('1');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeConv = conversations.find(c => c.id === activeConvId) || conversations[0];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeConv.messages, loading]);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/health`);
    setIsHealthy(res.data.status === 'healthy');
    console.log('Health check response:', res.data);
  } catch (error) {
    console.error('Health check failed:', error);
    setIsHealthy(false);
  }
  };

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      content: message.trim(),
      role: 'user',
      timestamp: new Date()
    };

    // Add message to active conversation
    setConversations(prev => prev.map(c => 
      c.id === activeConvId 
        ? { ...c, messages: [...c.messages, userMsg] }
        : c
    ));

    setMessage('');
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, {
        content: userMsg.content
      });

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        content: res.data.content,
        role: 'assistant',
        timestamp: new Date(),
        responseTime: res.data.response_time,
        tokenCount: res.data.token_count
      };

      setConversations(prev => prev.map(c => 
        c.id === activeConvId 
          ? { ...c, messages: [...c.messages, aiMsg] }
          : c
      ));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const createNewConversation = (category: string, name: string) => {
    const newId = Date.now().toString();
    const newConv: Conversation = {
      id: newId,
      name: name,
      messages: [],
      category: category
    };
    
    setConversations(prev => [...prev, newConv]);
    setActiveConvId(newId);
    
    // Focus on input after creating conversation
    setTimeout(() => textareaRef.current?.focus(), 100);
  };

  const deleteConversation = (id: string) => {
    if (conversations.length === 1) return; // Keep at least one
    
    setConversations(prev => prev.filter(c => c.id !== id));
    if (activeConvId === id) {
      setActiveConvId(conversations[0].id);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const categoryIcons: { [key: string]: string } = {
    code: '💻',
    explanation: '📚',
    creative: '🎨',
    analysis: '🔍',
    general: '💬'
  };

  return (
    <div className="chatbot-app">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo">🤖</div>
          <h1 className="app-title">AI Assistant Pro</h1>
        </div>
        <div className="header-right">
          <button 
            className="status-btn"
            onClick={checkHealth}
            aria-label="Check connection status"
          >
            {isHealthy === null ? '⚪ Checking...' : isHealthy ? '🟢 Online' : '🔴 Offline'}
          </button>
        </div>
      </header>

      <div className="app-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2 className="sidebar-title">Conversations</h2>
            <span className="conv-count">{conversations.length}</span>
          </div>

          <div className="conversations-list">
            {conversations.map(conv => (
              <div key={conv.id} className="conv-item-wrapper">
                <button
                  className={`conv-item ${activeConvId === conv.id ? 'active' : ''}`}
                  onClick={() => setActiveConvId(conv.id)}
                  aria-label={`Switch to ${conv.name}`}
                >
                  <span className="conv-icon">{categoryIcons[conv.category]}</span>
                  <div className="conv-details">
                    <div className="conv-name">{conv.name}</div>
                    <div className="conv-msg-count">{conv.messages.length} msgs</div>
                  </div>
                </button>
                {conversations.length > 1 && (
                  <button
                    className="delete-btn"
                    onClick={() => deleteConversation(conv.id)}
                    aria-label={`Delete ${conv.name}`}
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="new-conversation-section">
            <p className="section-label">Start New Conversation:</p>
            <div className="category-buttons">
              <button
                className="category-btn"
                onClick={() => createNewConversation('code', 'Code Generation')}
                title="Start coding conversation"
              >
                💻 Code
              </button>
              <button
                className="category-btn"
                onClick={() => createNewConversation('explanation', 'Explanations')}
                title="Start explanation conversation"
              >
                📚 Explain
              </button>
              <button
                className="category-btn"
                onClick={() => createNewConversation('creative', 'Creative Writing')}
                title="Start creative writing conversation"
              >
                🎨 Creative
              </button>
              <button
                className="category-btn"
                onClick={() => createNewConversation('analysis', 'Analysis')}
                title="Start analysis conversation"
              >
                🔍 Analysis
              </button>
            </div>
          </div>
        </aside>

        {/* Main Chat Area */}
        <main className="chat-main">
          {error && (
            <div className="error-alert" role="alert">
              <span>⚠️ {error}</span>
              <button onClick={() => setError(null)} aria-label="Dismiss error">✕</button>
            </div>
          )}

          <div className="messages-area">
            {activeConv.messages.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">💬</div>
                <h2 className="empty-title">
                  {activeConv.category === 'general' 
                    ? 'Start chatting!' 
                    : `${activeConv.name} Conversation`}
                </h2>
                <p className="empty-text">
                  {activeConv.category === 'general'
                    ? 'Type a message below or create a new conversation from the sidebar.'
                    : 'Type your question or request below to get started.'}
                </p>
              </div>
            ) : (
              <>
                {activeConv.messages.map(msg => (
                  <div key={msg.id} className={`message ${msg.role}`}>
                    <div className="msg-avatar">
                      {msg.role === 'user' ? '👤' : '🤖'}
                    </div>
                    <div className="msg-content">
                      <div className="msg-text">{msg.content}</div>
                      <div className="msg-footer">
                        <span className="msg-time">
                          {msg.timestamp.toLocaleTimeString()}
                        </span>
                        {msg.responseTime && (
                          <span className="msg-badge">{msg.responseTime}ms</span>
                        )}
                        {msg.tokenCount && (
                          <span className="msg-badge">{msg.tokenCount} tokens</span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message assistant">
                    <div className="msg-avatar">🤖</div>
                    <div className="typing-indicator">
                      <span>Thinking</span>
                      <div className="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          <div className="input-area">
            <div className="input-wrapper">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder={`Type your message for ${activeConv.name}...`}
                className="message-input"
                disabled={loading}
                rows={1}
                aria-label="Message input"
              />
              <button
                onClick={sendMessage}
                disabled={loading || !message.trim()}
                className="send-btn"
                aria-label="Send message"
              >
                {loading ? '⏳' : '📤'}
              </button>
            </div>
            <div className="input-hint">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ChatTest;
