package com.galeradev.galeradevblog.fragments

import android.app.Activity
import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.android.volley.Request.Method.GET
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.storage.User
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.android.synthetic.main.fragment_account.*

class AccountFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        super.onCreateView(inflater, container, savedInstanceState)
        return inflater.inflate(R.layout.fragment_account, container, false)
    }

    override fun onResume() {
        super.onResume()

        makeRequest(
            activity as Activity,
            GET,
            "account",
            {
                val listType = object : TypeToken<User>() {}.type
                val user: User = Gson().fromJson(it, listType)
                tv_username.text = "Hi, ${user.username}!"
                if (user.verified) {
                    tv_email.setTextColor(Color.parseColor("#2bf27f"))
                    tv_email.text = "Your email (${user.email}) is verified!"
                } else {
                    tv_email.setTextColor(Color.parseColor("#f22746"))
                    tv_email.text = "Your email (${user.email}) is not verified!"
                }

            }, {
                tv_username.text = "Not logged in"
                it.networkResponse.data?.let {data ->
                    Toast.makeText(
                        activity,
                        "Network error ${it.networkResponse.statusCode} ${String(data)}",
                        Toast.LENGTH_LONG
                    ).show()
                } ?: run {
                    Toast.makeText(
                        activity,
                        "Network error ${it.networkResponse.statusCode}",
                        Toast.LENGTH_LONG
                    ).show()
                }

            }
        )
    }
}