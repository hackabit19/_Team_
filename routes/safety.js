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
var spawn = require('child_process').spawn;
/*router.get('/',(req,res)=>{
    console.log("start");
    /*Safety.findOne({longitude : req.body.longitude, latitude : req.body.latitude},(err,result)=>{
        if(err) console.log('Invalid or Unavailable details');
        else{
            console.log("check");
            res.json(result).status(200);
        }
    });
    //var latitude = req.body.latitude,longitude = req.body.longitude;
    var latitude = 23.34,longitude=87.65;
    var date = new Date().getDate(),month = new Date().getMonth(),year = new Date().getFullYear(),time = new Date().getHours();
    var process = spawn('python',["../finallcode.py",time,date,month,year,longitude,latitude]);
    process.stdout.on('data',(data)=>{
        var arrayAnswer = data.toString();
        console.log("Hello!");
        console.log(arrayAnswer);
    });
    //res.json({text:'Hello'}).status(200);
});*/


module.exports = router;