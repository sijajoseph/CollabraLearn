// 
const GroupSchema = new mongoose.Schema({
  name: String,
  subject: String,
  members: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
  schedule: [Date]
});
module.exports = mongoose.model('Group', GroupSchema);

