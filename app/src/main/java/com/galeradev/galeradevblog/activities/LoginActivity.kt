package com.galeradev.galeradevblog.activities

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request.Method.POST
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import kotlinx.android.synthetic.main.activity_login.*

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        login_button.setOnClickListener {
            val params = HashMap<String, String>()
            params["login"] = login_input.text.toString()
            params["current-password"] = password_input.text.toString()

            makeRequest(
                this,
                POST,
                "login",
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
                },
                params
            )
        }

        recover_button.setOnClickListener {
            val intent = Intent(this, RecoverCreateActivity::class.java)
            startActivity(intent)
        }
    }
}
