'use client'

import { useEffect, useRef, useState } from 'react';

export default function ChatWidget() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);


  const startStream = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);

    // Show temporary empty AI message
    setMessages(prev => [...prev, { role: 'ai', text: '' }]);


    setInput('');
    setLoading(true);

    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let done = false;
    let currentText = '';

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) {
        const chunkStr = decoder.decode(value);
        try {
          const chunkJson = JSON.parse(chunkStr);
          currentText += chunkJson.response || '';
          setMessages(prev => {
            const last = prev[prev.length - 1];
            if (last?.role === 'ai') {
              return [...prev.slice(0, -1), { role: 'ai', text: currentText }];
            } else {
              return [...prev, { role: 'ai', text: currentText }];
            }
          });
        } catch {}
      }
    }

    setLoading(false);
  };


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="avatar">{msg.role === 'user' ? 'U' : 'AI'}</div>
            <div className="bubble">
              {msg.text || (msg.role === 'ai' && loading ? (
                <span className="dots"><span>.</span><span>.</span><span>.</span></span>
              ) : null)}
            </div>
          </div>
        ))}
         <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <textarea
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              startStream();
            }
          }}
          placeholder="Ask something..."
        />
        <button onClick={startStream} disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
