const express = require('express');
const Ably = require('Ably');
const parser = require('body-parser');
const cors = require('cors');
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
const realtime = new Ably.Realtime({key: keys.ably.ablyKey });
const randomstring = require("randomstring");
const path = require('path');
const app= express();
const ejs = require('ejs');
//connected to database


//create cookie
app.use(cookieSession({
    maxAge: 24*60*60*1000,
    keys: [keys.cookieSession.cookieKey]
}));

//initialize passport
app.use(passport.initialize());
app.use(passport.session());

app.use(express.static('public'));
app.set('view engine','ejs');

mongoose.connect(keys.mongodb.dbURI,()=>{
  console.log('Database connected');
});

app.use(parser.json()); //should be written above below lines...parse json data
app.use(parser.urlencoded({extended:true}));

//app.use(express.static(path.join(__dirname,'public')));
app.use('*', function(req, res, next){ // to alllow cors error //mdn cors
    res.set('Access-Control-Allow-Origin','*') //editing header
    res.set('Access-Control-Allow-Headers','content-type'); //for chrome
    next();
});

//setting up routes
app.use('/auth', authRoutes);
app.use('/profile', profileRoutes);
app.use('/report', dataRoutes);
app.use('/help', helpRoutes);
app.use('/safety', safetyRoutes);

app.get('/',(req,res)=>{
    //renders homepage, object tells if user is logged in or not, show buttons accordingly
    console.log('Waah');
    res.sendFile(path.join(__dirname, '/public', 'home.html'));
});
var spawn = require('child_process').spawn;
app.get('/safety',(req,res)=>{
    console.log("start");
    /*Safety.findOne({longitude : req.body.longitude, latitude : req.body.latitude},(err,result)=>{
        if(err) console.log('Invalid or Unavailable details');
        else{
            console.log("check");
            res.json(result).status(200);
        }
    });*/
    //var latitude = req.body.latitude,longitude = req.body.longitude;
    var latitude = 23.34,longitude=87.65;
    var date = new Date().getDate(),month = new Date().getMonth(),year = new Date().getFullYear(),time = new Date().getHours();
    var process = spawn('python',["./finallcode.py",time,date,month,year,longitude,latitude]);
    process.stdout.on('data',(data)=>{
        var arrayAnswer = data.toString();
        console.log("Hello!");
        console.log(arrayAnswer);
    });
    res.send("Hello");
    //res.json({text:'Hello'}).status(200);
});

app.get('/authFromAndroid', function (req, res) {
    var tokenParams = {
      'clientId': randomstring.generate({
          length: 12,
          
        })
    }; 
    realtime.auth.createTokenRequest(tokenParams, function(err, tokenRequest) {
      if (err) {
        res.status(500).send('Error requesting token: ' + JSON.stringify(err));
      } else {
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(tokenRequest));
      }
    });
  });


var port = process.env.PORT || 3000;
app.listen(port,()=>{
   console.log('Listening to 3000');
});