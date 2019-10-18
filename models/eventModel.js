const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const eventSchema = new Schema({
    hour:{type:Number},
    date:{type:Number},
    month:{type:Number},
    year:{type:Number},
    longitude:{type:Number,required:true},
    latitude:{type:Number,required:true},
    crimeType:{type:String,required:true}
});

module.exports = mongoose.model('event', eventSchema);