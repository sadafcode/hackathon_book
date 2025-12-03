
import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import { useSelectedText } from '@site/src/contexts/SelectedTextContext';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext'; // Add this import

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { selectedText, clearSelectedText } = useSelectedText();
        const messagesEndRef = useRef(null);
  
        const { siteConfig } = useDocusaurusContext(); // Get siteConfig
  
        // Extract chatbotApiUrl from customFields
        const chatbotApiUrl = siteConfig.customFields.chatbotApiUrl as string;
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
    setError(null); // Clear errors when toggling
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSendMessage = async (e) => {
    if (e.key === 'Enter' && (input.trim() || selectedText.trim())) {
      const userQuery = input.trim();
      const messageToSend = selectedText.trim()
        ? `Question (on selected text): "${userQuery}"\nSelected Text: "${selectedText}"`
        : userQuery;

      const userMessage = { sender: 'user', text: messageToSend };
      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      clearSelectedText(); // Clear selected text after sending
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(`${chatbotApiUrl}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: userQuery, selected_text: selectedText || null }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        // Assuming non-streaming response for simplicity from FastAPI, or handle stream as before
        // The backend response model is { response: string; source_urls: string[]; }
        const data = await response.json();
        let botResponseText = data.response;
        if (data.source_urls && data.source_urls.length > 0) {
          botResponseText += '\n\n**Sources:**\n' + data.source_urls.map(url => `- ${url}`).join('\n');
        }

        const botMessage = { sender: 'bot', text: botResponseText };
        setMessages((prev) => [...prev, botMessage]);

      } catch (e) {
        console.error("Error sending message:", e);
        setError(`Failed to get response: ${e.message}`);
        setMessages((prev) => [...prev, { sender: 'bot', text: `Error: ${e.message}` }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  if (!isOpen) {
    return (
      <button className={styles.chatButton} onClick={toggleChatbot}>
        Chat
      </button>
    );
  }

  return (
    <div className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h2>RAG Chatbot</h2>
        <button onClick={toggleChatbot} className={styles.closeButton}>X</button>
      </div>
      <div className={styles.chatMessages}>
        {messages.map((msg, index) => (
          <div key={index} className={clsx(styles.message, styles[msg.sender])}>
            {msg.text.split('\n').map((line, i) => <p key={i}>{line}</p>)}
          </div>
        ))}
        {isLoading && <div className={clsx(styles.message, styles.bot)}>Thinking...</div>}
        {error && <div className={clsx(styles.message, styles.bot, styles.error)}>Error: {error}</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.chatInput}>
        {selectedText && (
          <div className={styles.selectedTextIndicator}>
            Using selected text:
            "<span className={styles.selectedTextPreview}>{selectedText.substring(0, 50)}...</span>"
            <button onClick={clearSelectedText} className={styles.clearSelectedTextButton}>Clear</button>
          </div>
        )}
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleSendMessage}
          placeholder={selectedText ? "Ask a question about the selection..." : "Ask a question..."}
          disabled={isLoading}
        />
        <button onClick={() => handleSendMessage({ key: 'Enter', input: input })} disabled={isLoading || (!input.trim() && !selectedText.trim())}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
