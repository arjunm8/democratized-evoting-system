package com.technarcs.ccsms.dvoting;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Matrix;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.error.VolleyError;
import com.android.volley.request.SimpleMultiPartRequest;
import com.android.volley.request.StringRequest;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;

import androidx.appcompat.app.AppCompatActivity;


import static com.technarcs.ccsms.dvoting.MainActivity.MEDIA_SERVICE_URL;
import static com.technarcs.ccsms.dvoting.MainActivity.queue;

public class image_uploader extends AppCompatActivity {

    private static final int REQUEST_CAPTURE_IMAGE = 100;

    ImageView imageView;
    EditText titleInput;
    EditText descriptionInput;
    String imageUrl;
    String title;
    String description;
    Button upload;
    Button submit;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_uploader);

        upload = findViewById(R.id.camera_button);

        imageView = findViewById(R.id.camera_imageview);
        titleInput = findViewById(R.id.title_input);

        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCameraIntent();
            }
        });

        submit = findViewById(R.id.submit_contract);

        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

    }



    private void openCameraIntent() {
        Intent pictureIntent = new Intent(
                MediaStore.ACTION_IMAGE_CAPTURE
        );
        if(pictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(pictureIntent,
                    REQUEST_CAPTURE_IMAGE);
        }
    }

    private void uploadImage(Bitmap imageB) throws IOException {

        String url = MEDIA_SERVICE_URL+"/media";

        SimpleMultiPartRequest smr = new SimpleMultiPartRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response", response);

                        imageUrl = response.substring(9,response.length()-2);
                        Log.d("imageUrl", imageUrl);

                        Picasso.get().load(imageUrl).into(imageView);

                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_LONG).show();
            }
        });

        String path = getFilesDir()+"potato.png";
        File file = new File(path);
        OutputStream os = new BufferedOutputStream(new FileOutputStream(file));
        imageB.compress(Bitmap.CompressFormat.PNG, 100, os);
        os.close();

        smr.addFile("file", path);

        smr.setShouldCache(false);
        queue.add(smr);
    }


    public static Bitmap rotateImage(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(),
                matrix, true);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode,
                                    Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_CAPTURE_IMAGE &&
                resultCode == RESULT_OK) {
            if (data != null && data.getExtras() != null) {
                Bitmap imageBitmap = (Bitmap) data.getExtras().get("data");
                //maybe something's wrong with my gyro.
                imageBitmap = rotateImage(imageBitmap,90);
                try {
                    uploadImage(imageBitmap);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

    }
}