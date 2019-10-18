const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userSchema = new Schema({
    name: {type: String},
    googleId: {type: String,unique: true},
    gender: {type: String},
    thumbnail : {type : String},
    phone: {type: Number, default:0000000000}
});

const User = mongoose.model('user', userSchema);
module.exports = User;