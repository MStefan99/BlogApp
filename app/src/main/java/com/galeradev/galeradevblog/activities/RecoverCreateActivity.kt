package com.galeradev.galeradevblog.activities

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request.Method.POST
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import kotlinx.android.synthetic.main.activity_create_recover.*

class RecoverCreateActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_recover)

        reset_button.setOnClickListener {
            val params = HashMap<String, String>()
            params["login"] = login_input.text.toString()

            makeRequest(
                this,
                POST,
                "recover_create",
                {
                    Toast.makeText(
                        this,
                        it,
                        Toast.LENGTH_LONG
                    ).show()
                    onBackPressed()
                }, {
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
                },
                params
            )
        }
    }
}