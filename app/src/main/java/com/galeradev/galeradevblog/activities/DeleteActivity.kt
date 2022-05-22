package com.galeradev.galeradevblog.activities

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request.Method.PUT
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import kotlinx.android.synthetic.main.activity_delete.*

class DeleteActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_delete)

        reject_button.setOnClickListener {
            onBackPressed()
        }

        confirm_button.setOnClickListener {
            makeRequest(
                this,
                PUT,
                "delete",
                {
                    Toast.makeText(
                        this,
                        it,
                        Toast.LENGTH_LONG
                    ).show()
                    onBackPressed()
                },
                {
                    it.networkResponse.data?.let {data ->
                        Toast.makeText(
                            this,
                            "Network error ${it.networkResponse.statusCode} ${String(data)}",
                            Toast.LENGTH_LONG
                        ).show()
                    } ?: run {
                        Toast.makeText(
                            this,
                            "Network error ${it.networkResponse.statusCode}",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }
            )
            onBackPressed()
        }
    }
}