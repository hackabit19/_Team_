const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const safetySchema = new Schema({
    longitude :{ type: Number,required: true},
    latitude :{ type :Number, required:true},
    murder :{ type :Number, required:true},
    theft :{ type :Number, required:true},
    rape :{ type :Number, required:true},
    harassment :{ type :Number, required:true},
    overall :{type :Number, required:true}
});

const Safety = mongoose.model('safety', safetySchema);
module.exports = Safety;