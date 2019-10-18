const router = require('express').Router();
const Event = require('../models/eventModel');

router.post('/',(req,res)=>{
     new Event({
         hour: req.body.hour,
         date: req.body.date,
         month: req.body.month,
         year: req.body.year,
         longitude: req.body.longitude,
         latitude: req.body.latitude,
         eventType: req.body.eventType
     }).save().then(()=>{
         console.log('Data entered : '+ Event);
         res.send('Thanks for your response');
     });     
});

module.exports = router;