package com.galeradev.galeradevblog.utils

import android.content.Context
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request.Method.GET
import com.android.volley.VolleyError
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.galeradev.galeradevblog.App
import com.android.volley.VolleyLog
import com.android.volley.AuthFailureError




object NetworkUtil {

    fun makeRequest(
        context: Context,
        method: Int,
        path: String,
        onResponse: (String) -> Unit,
        onError: (VolleyError) -> Unit = {},
        params: HashMap<String, String>? = null
    ) {
        val queue = Volley.newRequestQueue(context)

        val request = object : StringRequest(
            method, "${App.API_URL}/$path/", {
                onResponse(it)
            }, {
                onError(it)
            }
        ) {
            override fun getParams(): Map<String, String>? {
                params?.let {
                    for (param in params) {
                        params[param.key] = param.value
                    }
                    return params
                } ?: run {
                    return null
                }
            }

            override fun getHeaders(): Map<String, String> {
                val headers = HashMap<String, String>()
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                return headers
            }

            override fun getBody(): ByteArray? {
                var body = ""
                params?.let {
                    for (param in params) {
                        body += param.key + "=" + param.value + "&"
                    }
                    return body.toByteArray(Charsets.UTF_8)
                } ?: run {
                    return null
                }
            }
        }

        request.retryPolicy = DefaultRetryPolicy(
            10000,
            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        )
        queue.add(request)
    }

    private fun getUrl(url: String, params: HashMap<String, String>?): String {
        var out = url
        if (params != null) {
            out += "?"
            for (param in params)
                out += "${param.key}=${param.value}&"
        }
        return out
    }
}