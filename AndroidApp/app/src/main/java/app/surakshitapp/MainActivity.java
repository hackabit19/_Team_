package app.surakshitapp;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.PendingIntent;
import android.app.job.JobInfo;
import android.app.job.JobScheduler;
import android.content.ComponentName;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.provider.Settings;
import android.view.View;
import android.widget.EditText;
import android.widget.ShareActionProvider;
import android.widget.TextView;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.ActivityRecognition;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import io.ably.lib.realtime.AblyRealtime;
import io.ably.lib.realtime.Channel;
import io.ably.lib.realtime.CompletionListener;
import io.ably.lib.realtime.ConnectionStateListener;
import io.ably.lib.types.AblyException;
import io.ably.lib.types.ClientOptions;
import io.ably.lib.types.ErrorInfo;
import io.ably.lib.types.Param;


public class MainActivity extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener {

    private GoogleApiClient googleApiClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        requestPermission();
        AblyRealtime ably = null;
        try {
            ably = new AblyRealtime("FzGgmg.Z07Qbw:uMa6eafC95XUl-ZJ");
        } catch (AblyException e) {
            e.printStackTrace();
        }
        /* 1. Plug in Ably to the underlying OS */
        try {
            ably.setAndroidContext(this);
        } catch (AblyException e) {
            e.printStackTrace();
        }
        /* 2. Activate (register) your device with FCM */
        try {
            ably.push.activate();
        } catch (AblyException e) {
            e.printStackTrace();
        }

        /* Subscribe device for native push notifications published on the alerts channel */
        Channel channel = ably.channels.get("test_channel");
        try {
            channel.push.subscribeDevice();
        } catch (AblyException e) {
            e.printStackTrace();
        }
        googleApiClient = new GoogleApiClient.Builder(this)
                .addApi(LocationServices.API)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .build();
        updateEmergencyNumberView();
    }
    private void updateEmergencyNumberView(){
        EditText emergencyNumber1 = (EditText) findViewById(R.id.editText1);
        EditText emergencyNumber2 = (EditText) findViewById(R.id.editText2);
        EditText emergencyNumber3 = (EditText) findViewById(R.id.editText3);
        SharedPreferences myPreferences = getSharedPreferences("myPreferences",MODE_PRIVATE);
        String name = myPreferences.getString("number1", "No name defined");
        if(!name.equals("No name defined")){
            //mergencyNumber1.setText("Enter Emergency Number 1", TextView.BufferType.EDITABLE);
            emergencyNumber1.setText(name,TextView.BufferType.EDITABLE);
        }
        String name2 = myPreferences.getString("number2", "No name defined");
        if(!name2.equals("No name defined")){
            //emergencyNumber2.setText("Enter Emergency Number 2", TextView.BufferType.EDITABLE);
            emergencyNumber2.setText(name2,TextView.BufferType.EDITABLE);
        }

        String name3 = myPreferences.getString("number3", "No name defined");
        if(!name3.equals("No name defined")){
            //emergencyNumber3.setText("Enter Emergency Number 3", TextView.BufferType.EDITABLE);
            emergencyNumber3.setText(name3,TextView.BufferType.EDITABLE);
        }

    }
    public void getEmergencyNumberOnSubmit(View view){

        EditText emergencyNumber1 = (EditText) findViewById(R.id.editText1);
        EditText emergencyNumber2 = (EditText) findViewById(R.id.editText2);
        EditText emergencyNumber3 = (EditText) findViewById(R.id.editText3);
        SharedPreferences myPreferences = getSharedPreferences("myPreferences",MODE_PRIVATE);
        SharedPreferences.Editor editor;
        editor = myPreferences.edit();
        editor.putString("number1",emergencyNumber1.getText().toString());
        editor.putString("number2",emergencyNumber2.getText().toString());
        editor.putString("number3",emergencyNumber3.getText().toString());
        editor.commit();
    }
    public void reportPageInBrowser(View view){
        //Intent Getintent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://nish7898.herokuapp.com"));
        Intent intent = new Intent(MainActivity.this, SecondActivity.class);
        startActivity(intent);
    }
    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case 0: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // permission was granted
                    System.out.println("Permission Granted!");
                    requestLocationUpdates();

                } else {
                    // permission was denied
                    System.out.println("Permission Not Granted!");
                }
                return;
            }
            case 70:{
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // permission was granted
                    System.out.println("Permission Granted!");
                    callFirstNumberAfterGettingPermission(1);

                } else {
                    // permission was denied
                    System.out.println("Permission Not Granted!");
                }
            }
        }
    }
    private void requestPermission() {
        boolean permissionAccessCoarseLocationApproved =
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)
                        == PackageManager.PERMISSION_GRANTED;

        if (permissionAccessCoarseLocationApproved) {
            boolean backgroundLocationPermissionApproved =
                    ActivityCompat.checkSelfPermission(this,
                            Manifest.permission.ACCESS_BACKGROUND_LOCATION)
                            == PackageManager.PERMISSION_GRANTED;

            if (backgroundLocationPermissionApproved) {
                // App can access location both in the foreground and in the background.
                // Start your service that doesn't have a foreground service type
                // defined.
                /*googleApiClient = new GoogleApiClient.Builder(this)
                        .addApi(LocationServices.API)
                        .addConnectionCallbacks(this)
                        .addOnConnectionFailedListener(this)
                        .build();*/
                //requestLocationUpdates();

            } else {
                // App can only access location in the foreground. Display a dialog
                // warning the user that your app must have all-the-time access to
                // location in order to function properly. Then, request background
                // location.
                ActivityCompat.requestPermissions(this, new String[]{
                                Manifest.permission.ACCESS_BACKGROUND_LOCATION},
                        10);
            }
        } else {
            // App doesn't have access to the device's location at all. Make full request
            // for permission.
            ActivityCompat.requestPermissions(this, new String[]{
                            Manifest.permission.ACCESS_COARSE_LOCATION,
                            Manifest.permission.ACCESS_BACKGROUND_LOCATION
                    },
                    0);
        }
    }
    @Override
    public void onStart() {
        super.onStart();
        googleApiClient.connect();
        //requestPermission();
    }

    @Override
    public void onStop() {
        //requestPermission();
        super.onStop();
        if (googleApiClient.isConnected()) {
            googleApiClient.disconnect();
        }
    }

    @Override
    public void onBackPressed() {
        // Check whether you receive location updates after the app has been killed by the system
        System.exit(0);
    }

    @Override
    public void onConnected(Bundle bundle) {
        //requestPermission();
        int permissionCheck1 = ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_COARSE_LOCATION);
        if(permissionCheck1==PackageManager.PERMISSION_GRANTED)
        requestLocationUpdates();
    }

    @Override
    public void onConnectionSuspended(int cause) {
        //requestPermission();
        googleApiClient.connect();
    }

    @Override
    public void onConnectionFailed(ConnectionResult result) {

    }



    public void requestLocationUpdates() {
        //requestPermission();
        LocationRequest locationRequest = new LocationRequest()
                .setInterval(20 * 1000)
                .setPriority(LocationRequest.PRIORITY_BALANCED_POWER_ACCURACY);

        Intent intent = new Intent(this, LocationService.class);
        PendingIntent pendingIntent = PendingIntent.getService(this, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
        LocationServices.FusedLocationApi.requestLocationUpdates(googleApiClient, locationRequest, pendingIntent);
        //ActivityRecognition.ActivityRecognitionApi.requestActivityUpdates(googleApiClient,0,pendingIntent);
    }

    public void callFirstNumber(View view){
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CALL_PHONE},70);
        }
        else
        {
            callFirstNumberAfterGettingPermission(1);
        }
    }
    public void callFirstNumberAfterGettingPermission(int emergency){
        //String emergencyNumberOne=(EditText) findViewById(R.id.editText1).getTex;
        EditText emergencyNumber1 = (EditText) findViewById(R.id.editText1);
        String numberToCall = emergencyNumber1.getText().toString();
        Intent intent = new Intent(Intent.ACTION_DIAL);
        intent.setData(Uri.parse("tel:"+numberToCall));
        startActivity(intent);
    }



}
