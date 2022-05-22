package com.galeradev.galeradevblog.fragments

import android.app.Activity
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.android.volley.Request.Method.GET
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.activities.MainActivity
import com.galeradev.galeradevblog.adapters.PostsAdapter
import com.galeradev.galeradevblog.storage.Post
import com.galeradev.galeradevblog.utils.NetworkUtil.makeRequest
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.android.synthetic.main.fragment_posts.*


class PostsFragment : Fragment() {

    private lateinit var posts: ArrayList<Post>

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        super.onCreateView(inflater, container, savedInstanceState)
        getPosts {
            setPosts(it)
            posts = it
        }
        return inflater.inflate(R.layout.fragment_posts, container, false)
    }

    override fun onResume() {
        super.onResume()
        swipe_refresh.setOnRefreshListener {
            getPosts {
                setPosts(it)
                posts = it
            }
        }

        posts_list.setOnItemClickListener { _, _, position, _ ->
            val act = activity as MainActivity
            act.sendData(posts[position])
        }
    }


    private fun getPosts(callback: (ArrayList<Post>) -> Unit) {
        makeRequest(
            activity as Activity,
            GET,
            "posts",
            {
                swipe_refresh.isRefreshing = false

                val listType = object : TypeToken<ArrayList<Post>>() {}.type
                val posts: ArrayList<Post> = Gson().fromJson(it, listType)

                callback(posts)
            },
            {
                swipe_refresh.isRefreshing = false

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

    private fun setPosts(posts: ArrayList<Post>) {
        val postsAdapter = PostsAdapter(
            activity!!.applicationContext,
            R.layout.posts_adapter,
            posts
        )
        posts_list.adapter = postsAdapter
    }
}