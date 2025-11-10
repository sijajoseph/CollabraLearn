// 
const GroupSchema = new mongoose.Schema({
  name: String,
  subject: String,
  members: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
  schedule: [Date]
});
module.exports = mongoose.model('Group', GroupSchema);

// models/Message.js
const MessageSchema = new mongoose.Schema({
  group: { type: mongoose.Schema.Types.ObjectId, ref: 'Group' },
  sender: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  text: String,
  createdAt: { type: Date, default: Date.now }
});
module.exports = mongoose.model('Message', MessageSchema);
