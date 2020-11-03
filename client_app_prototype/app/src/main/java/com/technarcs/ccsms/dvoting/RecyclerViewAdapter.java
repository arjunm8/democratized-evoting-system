package com.technarcs.ccsms.dvoting;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.error.VolleyError;
import com.android.volley.request.JsonObjectRequest;
import com.android.volley.request.StringRequest;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.navigation.fragment.NavHostFragment;
import androidx.recyclerview.widget.RecyclerView;

import static com.technarcs.ccsms.dvoting.MainActivity.BALLOT_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.TXN_ID;
import static com.technarcs.ccsms.dvoting.MainActivity.USER_ID;
import static com.technarcs.ccsms.dvoting.MainActivity.USER_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.queue;
import static com.technarcs.ccsms.dvoting.login.USER_PHONE;


public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerViewAdapter.ViewHolder> {
    private ArrayList<String> candidate_names;
    private ArrayList<String> candidate_ids;
    private ArrayList<String> images;

    private Context mContext;

    public RecyclerViewAdapter(
            ArrayList<String> candidate_names,
            ArrayList<String> candidate_ids,
            ArrayList<String> images,
            Context mContext) {

        this.candidate_names = candidate_names;
        this.candidate_ids = candidate_ids;
        this.images = images;
        this.mContext = mContext;
    }


    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view  = LayoutInflater.from(parent.getContext()).inflate(R.layout.candidate_list_item, parent, false);

        return new ViewHolder(view);
    }

    //major @TODO: use string resources and constants instead of so much hardcoding
    @Override
    public void onBindViewHolder(@NonNull final ViewHolder holder, final int position) {
        Picasso.get().load(images.get(position)).into(holder.imageView);
        holder.candidate_name.setText(candidate_names.get(position));
         holder.actionButton1.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    AlertDialog.Builder builder = new AlertDialog.Builder(mContext);
                    builder.setMessage("Are you sure you want to Vote this Candidate?")
                            .setCancelable(true)
                            .setPositiveButton("Yes, I am sure!", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int id) {
                                    postVote(candidate_ids.get(position));
                                }
                            });
                    AlertDialog alert = builder.create();
                    alert.show();
                }
            });
    }

    @Override
    public int getItemCount() {
        return candidate_names.size();
    }

    private void postVote(final String candidate_id){
        String url = BALLOT_SERVICE_URL+"/ballot";
        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {
                        // response
                        Log.d("Response", response);
                        try {
                            JSONObject obj = new JSONObject(response);
                            TXN_ID = obj.getString("transaction_id");
                            Toast.makeText(mContext, "Vote Casted to blockchain, txn id: "+TXN_ID, Toast.LENGTH_LONG).show();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }finally {
                            /*
                            NavHostFragment.findNavController(FirstFragment.this)
                                    .navigate(R.id.action_FirstFragment_to_SecondFragment);
                             */
                        }

                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Log.d("Error.Response", error.toString());
                        Toast.makeText(mContext, "Vote Posting failed: "+error.toString(), Toast.LENGTH_LONG).show();
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("candidate_id", candidate_id);
                params.put("user_id", USER_ID);
                return params;
            }
        };
        postRequest.setShouldCache(false);

        queue.add(postRequest);
    }


    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView candidate_name;
        ImageView imageView;
        Button actionButton1;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            candidate_name = itemView.findViewById(R.id.c_candidate_name);
            imageView = itemView.findViewById(R.id.c_image);
            actionButton1 = itemView.findViewById(R.id.action_button1);
        }
    }


    }
