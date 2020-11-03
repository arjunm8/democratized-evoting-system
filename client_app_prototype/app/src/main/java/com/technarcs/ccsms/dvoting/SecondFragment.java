package com.technarcs.ccsms.dvoting;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.error.VolleyError;
import com.android.volley.request.JsonArrayRequest;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import static com.technarcs.ccsms.dvoting.MainActivity.BALLOT_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.MEDIA_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.USER_ID;
import static com.technarcs.ccsms.dvoting.MainActivity.queue;

public class SecondFragment extends Fragment {

    private RecyclerView recyclerView;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_second, container, false);
    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        loadCandidates(view);
    }

    public void loadCandidates(final View root){
        String base_url = BALLOT_SERVICE_URL+"/candidates";

        Log.d("baseUrl",base_url);


        JsonArrayRequest getRequest = new JsonArrayRequest(Request.Method.GET, base_url, null,
                new Response.Listener<JSONArray>()
                {
                    @Override
                    public void onResponse(JSONArray response) {
                        // display response
                        Log.d("Response", response.toString());

                        candidate_array_init(response,root);
                    }
                },
                new Response.ErrorListener()
                {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("Error.Response", error.toString());

                    }
                }
        );
        getRequest.setShouldCache(false);
        queue.add(getRequest);
    }

    private void candidate_array_init(JSONArray response, final View root) {

        //@TODO group these as objects
        ArrayList<String> candidate_names = new ArrayList<>();
        ArrayList<String> candidate_ids = new ArrayList<>();
        ArrayList<String> images = new ArrayList<>();


        for(int i=0;i<response.length();i++){
            try {
                JSONObject contract = response.getJSONObject(i);

                candidate_names.add(contract.getString("name"));
                candidate_ids.add(contract.getString("id"));
                images.add(MEDIA_SERVICE_URL+"/media/"+contract.getString("image_url"));

            }catch (Exception e){
                Log.e("error parsing json object",e.toString());
            }
        }


        recyclerView = root.findViewById(R.id.recycler_view);

        if (candidate_names.size()>0) {
            RecyclerViewAdapter adapter = new RecyclerViewAdapter(
                    candidate_names,
                    candidate_ids,
                    images,
                    getContext()
            );
            recyclerView.setAdapter(adapter);
            recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        }else{
            root.findViewById(R.id.no_apps_text).setVisibility(View.VISIBLE);
        }

    }

}