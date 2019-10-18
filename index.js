const express = require('express');
const authRoutes = require('./routes/auth-routes');
const profileRoutes = require('./routes/profile');
const dataRoutes = require('./routes/data-form');
const helpRoutes = require('./routes/helpers');
const safetyRoutes = require('./routes/safety');
const passpostSetup = require('./config/passport-setup');
const mongoose = require('mongoose');
const keys = require('./config/keys');
const cookieSession = require('cookie-session');
const passport = require('passport');

const app= express();

//connected to database
mongoose.connect(keys.mongodb.dbURI,()=>{
    console.log('Database connected');
});

//create cookie
app.use(cookieSession({
    maxAge: 24*60*60*1000,
    keys: [keys.cookieSession.cookieKey]
}));

//initialize passport
app.use(passport.initialize());
app.use(passport.session());

app.set('view engine','ejs');

//setting up routes
app.use('/auth', authRoutes);
app.use('/profile', profileRoutes);
app.use('/report', dataRoutes);
app.use('/help', helpRoutes);
app.use('/safety', safetyRoutes);

app.get('/',(req,res)=>{
    //renders homepage, object tells if user is logged in or not, show buttons accordingly
    console.log('Waah');
    res.render('home', {user: req.user});
});

app.listen(3000,()=>{
   console.log('Listening to 3000');
});