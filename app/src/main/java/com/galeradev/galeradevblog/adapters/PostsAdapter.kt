package com.galeradev.galeradevblog.adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.TextView
import com.galeradev.galeradevblog.R
import com.galeradev.galeradevblog.storage.Post

class PostsAdapter(private val aContext: Context, private val aResource: Int, objects: ArrayList<Post>) :
    ArrayAdapter<Post>(aContext, aResource, objects) {

    private data class ViewHolder(
        val title: TextView,
        val tagline: TextView,
        val splashBitmap: ImageView
    )

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val title = getItem(position)?.title
        val tagline = getItem(position)?.tagline
        val splashBitmap = getItem(position)?.splashBitmap
        val holder: ViewHolder
        val view: View

        if (convertView == null) {
            view = LayoutInflater.from(aContext).inflate(aResource, parent, false)
            holder = ViewHolder(
                view.findViewById(R.id.postTitle),
                view.findViewById(R.id.postTagline),
                view.findViewById(R.id.postSplash)
            )
            view.tag = holder

        } else {
            view = convertView
            holder = convertView.tag as ViewHolder
        }


        holder.title.text = title
        holder.tagline.text = tagline
        holder.splashBitmap.setImageBitmap(splashBitmap)

        return view
    }
}
