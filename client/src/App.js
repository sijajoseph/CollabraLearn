import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [message, setMessage] = useState('');
  const [groupId, setGroupId] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket.on('receiveMessage', (data) => {
      setMessages((prev) => [...prev, data]);
    });
  }, []);

  const sendMessage = () => {
    socket.emit('sendMessage', { groupId, text: message });
    setMessage('');
  };

  return (
    <div>
      <input value={groupId} onChange={e => setGroupId(e.target.value)} placeholder="Group ID" />
      <input value={message} onChange={e => setMessage(e.target.value)} placeholder="Message"/>
      <button onClick={sendMessage}>Send</button>
      <ul>
        {messages.map((msg, idx) => <li key={idx}>{msg.text}</li>)}
      </ul>
    </div>
  );
}

export default App;
