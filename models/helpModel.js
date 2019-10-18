const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const helpSchema = new Schema({
     user :{
         type: String,
         required : true
     },
     numberOne:{type : Number, required : true},
     numberTwo:{type : Number},
     numberThree:{type : Number}
});

module.exports = mongoose.model('help', helpSchema);