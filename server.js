const express = require('express');
const http = require('http');
const mongoose = require('mongoose');
const socketio = require('socket.io');
const cors = require('cors');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketio(server);

app.use(cors());
app.use(express.json());

// Import routes
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/user');
const groupRoutes = require('./routes/group');
const chatRoutes = require('./routes/chat');

// Use routes
app.use('/api/auth', authRoutes);
app.use('/api/user', userRoutes);
app.use('/api/group', groupRoutes);
app.use('/api/chat', chatRoutes);

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, () => {
  console.log('MongoDB connected');
});

// Socket.io setup
io.on('connection', (socket) => {
  socket.on('joinGroup', (groupId) => {
    socket.join(groupId);
  });
  socket.on('sendMessage', (data) => {
    io.to(data.groupId).emit('receiveMessage', data);
  });
  socket.on('notify', (notification) => {
    io.emit('notification', notification);
  });
});

server.listen(process.env.PORT || 5000, () => {
  console.log(`Server running on port ${process.env.PORT || 5000}`);
});
