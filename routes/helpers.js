const router = require('express').Router();
const Help = require('../models/helpModel')

router.post('/',(req,res)=>{
    new Help({
        user: req.body.Id,
        numberOne: req.body.numberOne,
        numberTwo: req.body.numberTwo,
        numberThree: req.body.numberThree
    }).save().then(()=>{
        console.log('Help numbers added');
        res.render('/profile/');
    })
});

router.get('/',(req,res)=>{
    Help.findOne({googleId : req.body.Id},(err,result)=>{
        if(err) throw err;
        else{
        res.json(result).status(200);
        }
    });
});

module.exports = router;