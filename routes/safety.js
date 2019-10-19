const router = require('express').Router();
const Safety = require('../models/safetyModel');

router.post('/',(req,res)=>{
    Safety.findOne({longitude : req.body.longitude, latitude : req.body.latitude}).then((location)=>{
        if(location){
            var newLocation = {
                longitude: req.body.longitude,
                latitude: req.body.latitude,
                murder: req.body.murder,
                theft: req.body.theft,
                rape: req.body.rape,
                harassment: req.body.harassment,
                overall: req.body.overall
            };
            Safety.updateOne(location,newLocation,(err,res)=>{
                if(err) throw err;
                else{
                    console.log('Safety parameters updated');
                }
            });
        }
        else{
           new Safety({
            longitude: req.body.longitude,
            latitude: req.body.latitude,
            murder: req.body.murder,
            theft: req.body.theft,
            rape: req.body.rape,
            harassment: req.body.harassment,
            overall: req.body.overall 
           }).save().then(()=>{
               console.log('Safety parameter of new location added');
           });
        }
    });
});

router.get('/phone',(req,res)=>{
    /**Safety.findOne({longitude : req.body.longitude, latitude : req.body.latitude},(err,result)=>{
        if(err) console.log('Invalid or Unavailable details');
        else{
            res.json(result).status(200);
        }
    });*/
    res.json({text:'Hello'}).status(200);
});


module.exports = router;