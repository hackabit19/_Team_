const router = require('express').Router();
const Event = require('../models/eventModel');

router.post('/',(req,res)=>{
     new Event({
         month: req.body.Month,
         date: req.body.Date,
         year: req.body.Year,
         longitude: req.body.LOCATION_LONGITUDE,
         latitude: req.body.LOCATION_LATITUDE,
         hour: req.body.Hour,
         eventType: req.body.Crime
     }).save().then(()=>{
         console.log('Data entered : '+ Event);
         res.send('Thanks for your response');
     });     
});

router.get('/',(req,res)=>{
    Event.find({}).toArray((err,result)=>{
        if(err) throw err;
        else{
            console.log(result);
            res.send(result).status(200);
        }
    });
});

module.exports = router;