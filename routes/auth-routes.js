const router = require('express').Router();
const passport = require('passport');
const User = require('../models/userModel');

//auth login
router.get('/login',(req,res)=>{
    res.render('dashboard');
});

//auth logout
router.get('/logout',(req,res)=>{
    //passport
    req.logOut();
    res.redirect('/');
});

//auth with google
router.get('/google',passport.authenticate('google',{
    scope : ['profile']
}));

router.get('/google/redirect',passport.authenticate('google',{failureRedirect:'/login'}),(req,res)=>{
    console.log((req.user).phone);
    if((req.user).phone == 0000000000){
        res.render('info',{user : req.user});
    }
    else{
        res.redirect('/profile/');
    }
});

router.post('/phone',(req,res)=>{
    User.updateOne({googleId : req.body.Id},{phone : req.body.phone}, (err,res)=>{
        if(err) throw err;
        else 
        console.log('User Phone number added');
    });
});

module.exports = router;