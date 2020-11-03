package com.technarcs.ccsms.dvoting;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.error.VolleyError;
import com.android.volley.request.StringRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

import androidx.annotation.NonNull;
import androidx.biometric.BiometricPrompt;
import androidx.cardview.widget.CardView;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import static com.technarcs.ccsms.dvoting.MainActivity.USER_ID;
import static com.technarcs.ccsms.dvoting.MainActivity.USER_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.queue;
import static com.technarcs.ccsms.dvoting.login.USER_PHONE;

public class FirstFragment extends Fragment {

    public static Boolean docv=false;
    public static Boolean facev=false;
    Executor newExecutor = Executors.newSingleThreadExecutor();

    CardView face;
    CardView auth;
    Button proceed;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_first, container, false);
    }

    @Override
    public void onResume() {
        super.onResume();
        if(docv) {
            face.setCardBackgroundColor(Color.WHITE);
        }
        if(facev) {
            auth.setCardBackgroundColor(Color.WHITE);
        }
    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        face = view.findViewById(R.id.faceverifycard);
        auth = view.findViewById(R.id.authverifycard);
        proceed = view.findViewById(R.id.button_first);

        view.findViewById(R.id.docverifycard).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(getContext(), ImageUploader.class);
                startActivity(i);
                docv = true;
            }
        });


        face.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(getContext(), ImageUploader.class);
                startActivity(i);
                facev = true;
            }
        });


        auth.setOnClickListener(new View.OnClickListener() {
            final BiometricPrompt myBiometricPrompt = new BiometricPrompt(
                    getActivity(),
                    newExecutor,
                    new BiometricPrompt.AuthenticationCallback() {
                        @Override
                        public void onAuthenticationSucceeded(@NonNull BiometricPrompt.AuthenticationResult result) {
                            super.onAuthenticationSucceeded(result);
                            proceed.setBackgroundColor(getResources().getColor(R.color.colorPrimary));
                        }

            });

                @Override
            public void onClick(View view) {
                Log.e("tag","asking for auth");
                final BiometricPrompt.PromptInfo promptInfo = new BiometricPrompt.PromptInfo.Builder()
                        .setTitle("Owner Authentication Required")
                        .setDescription("Ask the device owner for authentication")
                        .setNegativeButtonText("Cancel")
                        .build();
                myBiometricPrompt.authenticate(promptInfo);
            }
        });

        proceed.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                postUser();
            }
        });
    }



    private void postUser(){
        String url = USER_SERVICE_URL+"/user";
        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        Log.d("Response", response);
                        try {
                            JSONObject obj = new JSONObject(response);
                            USER_ID = obj.getString("id");
                            Toast.makeText(getActivity(), "User Created: "+obj.getString("id"), Toast.LENGTH_SHORT).show();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }finally {
                            NavHostFragment.findNavController(FirstFragment.this)
                                    .navigate(R.id.action_FirstFragment_to_TutFragment);
                        }

                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Log.d("Error.Response", error.toString());
                        Toast.makeText(getActivity(), "User Creation failed: "+error.toString(), Toast.LENGTH_LONG).show();
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("phone", USER_PHONE);
                params.put("name", "placeholder_till_form_ready");
                return params;
            }
        };
        postRequest.setShouldCache(false);

        queue.add(postRequest);
    }


}