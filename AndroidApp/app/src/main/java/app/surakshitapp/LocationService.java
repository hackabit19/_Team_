package app.surakshitapp;

import android.app.IntentService;
import android.app.NotificationManager;
import android.content.Intent;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;

import androidx.core.app.NotificationCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


import static android.content.Context.NOTIFICATION_SERVICE;

public class LocationService extends IntentService {

    private static final String INTENT_SERVICE_NAME = LocationService.class.getName();

    public LocationService() {
        super(INTENT_SERVICE_NAME);
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        if (null == intent) {
            return;
        }

        Bundle bundle = intent.getExtras();

        if (null == bundle) {
            return;
        }

        Location location = bundle.getParcelable("com.google.android.location.LOCATION");

        if (null == location) {
            return;
        }

        if (null != location) {
            // TODO: Handle the incoming location

            Log.i(INTENT_SERVICE_NAME, "onHandleIntent " + location.getLatitude() + ", " + location.getLongitude());

            // Just show a notification with the location's coordinates
            /*NotificationManager notificationManager = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
            NotificationCompat.Builder notification = new NotificationCompat.Builder(this);
            notification.setContentTitle("Location");
            notification.setContentText(location.getLatitude() + ", " + location.getLongitude());
            notification.setSmallIcon(R.drawable.common_full_open_on_phone);*/
            //notificationManager.notify(1234, notification.build());
        }
    }

    public void connectToServer(Location location){
        RequestQueue queue = Volley.newRequestQueue(this);
        //RequestQueue queue = Volley.newRequestQueue(this);
        final String url = "http://nish7898.herokuapp.com/";
        StringRequest putRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response", (response));

                        //myTextView.setText(response.toString());
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("Error.Response", error.toString());
                    }
                }

        ){
            @Override
            protected Map<String,String> getParams(){
                Map<String, String> params = new HashMap<String, String>();
                return params;
            }
        };
        queue.add(putRequest);
    }

}
