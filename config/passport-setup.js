const passport = require('passport');
const googleStrategy = require('passport-google-oauth').OAuth2Strategy;
const keys = require('./keys');
const User = require('../models/userModel');

passport.serializeUser((user,done)=>{
     done(null, user.id);
});

passport.deserializeUser((id,done)=>{
    User.findById(id).then((user)=>{
        done(null, user);
    });
});

passport.use(
    new googleStrategy({
        //options for google strategy
        callbackURL: '/auth/google/redirect',
        clientID: keys.google.clientID,
        clientSecret: keys.google.clientSecret
    },(accessToken, refreshToken, profile, done)=>{
        //callback
        User.findOne({googleId: profile.id}).then((currentUser)=>{
            if(currentUser){
                 console.log('Already created, Welcome back');
                return done(null,currentUser);
            }else{
                //creating new User
                new User({
                    name: profile.displayName,
                    googleId: profile.id,
                    gender: profile.gender,
                    thumbnail: profile._json.image.url
                }).save().then((newUser)=>{
                    console.log('New User Created : '+ newUser);
                    return done(null , newUser);
                });
            }
        });
    })
);
