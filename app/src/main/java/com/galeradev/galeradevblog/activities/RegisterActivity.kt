package com.galeradev.galeradevblog.activities

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request.Method.PUT
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import kotlinx.android.synthetic.main.activity_register.*

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        register_button.setOnClickListener {
            val usernameEmpty = username_input.text.toString().isEmpty()
            val emailEmpty = email_input.text.toString().isEmpty()
            val passwordEmpty = password_input.text.toString().isEmpty()
            val passwordRepeatEmpty = password_repeat_input.text.toString().isEmpty()

            val passwordsMismatch = password_input.text.toString() != password_repeat_input.text.toString()

            if (usernameEmpty || emailEmpty || passwordEmpty || passwordRepeatEmpty) {
                Toast.makeText(this, "Please fill in all the fields", Toast.LENGTH_LONG).show()
            } else if (passwordsMismatch) {
                Toast.makeText(this, "Passwords do not match", Toast.LENGTH_LONG).show()
            } else {
                val params = HashMap<String, String>()
                params["username"] = username_input.text.toString()
                params["email"] = email_input.text.toString()
                params["new-password"] = password_input.text.toString()

                makeRequest(
                    this,
                    PUT,
                    "register",
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
}