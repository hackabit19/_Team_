const router = require('express').Router();
const passport = require('passport');
const User = require('../models/userModel');

//auth login
router.get('/login',(req,res)=>{
    res.render('home',{user: req.user});
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

module.exports = router;