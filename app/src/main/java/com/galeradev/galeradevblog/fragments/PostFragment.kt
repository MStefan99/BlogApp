package com.galeradev.galeradevblog.fragments

import android.app.Activity
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.android.volley.Request.Method.*
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.storage.Post
import com.galeradev.galeradevblog.utils.CookieUtil.isLoggedIn
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import kotlinx.android.synthetic.main.fragment_post.*

class PostFragment : Fragment() {
    lateinit var post: Post

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        super.onCreateView(inflater, container, savedInstanceState)
        return inflater.inflate(R.layout.fragment_post, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        post_title.text = post.title
        post_tagline.text = post.tagline
        post_date.text = post.date
        post_author.text = post.author
        post_content.text = post.content
        post_tags.text = post.tags

        if (isLoggedIn()) {
            val params = HashMap<String, String>()
            params["post"] = post.id.toString()

            makeRequest(
                activity as Activity,
                GET,
                "favourite",
                {
                    if (it == "IS FAVOURITE") {
                        favorite_button.text = "Remove"
                        favorite_button.setOnClickListener {
                            makeRequest(
                                activity as Activity,
                                DELETE,
                                "favourite",
                                { }
                            )
                        }
                    } else {
                        favorite_button.text = "Save"
                        favorite_button.setOnClickListener {
                            makeRequest(
                                activity as Activity,
                                PUT,
                                "favourite",
                                { }
                            )
                        }
                    }
                },
                {
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
                },
                params
            )

        } else {
            favorite_button.text = "Log in to save posts"
            favorite_button.isClickable = false
        }
    }
}