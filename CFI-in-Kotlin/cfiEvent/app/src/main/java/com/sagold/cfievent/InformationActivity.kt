package com.sagold.cfievent

import android.os.Bundle
import android.support.v7.app.AppCompatActivity

import kotlinx.android.synthetic.main.activity_information.*
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.QueryDocumentSnapshot
import kotlinx.android.synthetic.main.content_information_activity.*


class InformationActivity : AppCompatActivity() {
    private val db = FirebaseFirestore.getInstance()

    companion object {
        const val IS_ADMIN = "IS_ADMIN"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_information)

        if (intent.getBooleanExtra(IS_ADMIN, false)) {
            showLoginFlag()
        }
    }

    private fun showLoginFlag() {
        db.collection("FLAG")
            .get()
            .addOnCompleteListener {
                if (it.isSuccessful) {
                    for (document: QueryDocumentSnapshot in  it.result) {
                        if (document.id == "LOGIN") {
                            showMessage(document.data["KEY"] as String)
                        }
                    }
                } else {
                    showMessage("Error getting documents.")
                }
            }
    }

    private fun showMessage(message: String) {
        messageTextView.text = message
    }
}