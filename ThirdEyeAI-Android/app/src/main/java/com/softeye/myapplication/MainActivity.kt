package com.softeye.myapplication

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {

    private val client by lazy {
        OkHttpClient
            .Builder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .build()
    }
    private var tts: TextToSpeech? = null

    private lateinit var nsdManager: NsdManager
    private var discoveryListener: NsdManager.DiscoveryListener? = null
    private var serverHost: String? = null
    private var serverPort: Int = 6000

    private lateinit var imageCapture: ImageCapture

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) startCamera()
        else Toast.makeText(this, "카메라 권한이 필요합니다.", Toast.LENGTH_SHORT).show()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED
        ) {
            startCamera()
        } else {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }

        initServiceDiscovery()

        tts = TextToSpeech(this) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale.KOREAN
            }
        }

        findViewById<Button>(R.id.captureButton).setOnClickListener {
            if (serverHost == null) {
                Toast.makeText(this, "서버를 아직 찾지 못했습니다.", Toast.LENGTH_SHORT).show()
<<<<<<< HEAD
                Log.d("테스트", "버튼 클릭됨")
=======
>>>>>>> main
            } else {
                takePictureAndSend()
            }
        }
    }

    private fun initServiceDiscovery() {
        nsdManager = getSystemService(Context.NSD_SERVICE) as NsdManager

        discoveryListener = object : NsdManager.DiscoveryListener {
            override fun onDiscoveryStarted(regType: String) {
                Log.d("NSD", "Discovery started: $regType")
            }

            override fun onServiceFound(service: NsdServiceInfo) {
                if (service.serviceType == "_http._tcp." &&
                    service.serviceName == "ThirdEyeKiosk"
                ) {
                    nsdManager.resolveService(service, object : NsdManager.ResolveListener {
                        override fun onServiceResolved(resolved: NsdServiceInfo) {
                            serverHost = resolved.host.hostAddress
                            serverPort = resolved.port
                            Log.d("NSD", "Resolved: $serverHost:$serverPort")
                        }

                        override fun onResolveFailed(srv: NsdServiceInfo, error: Int) {
                            Log.e("NSD", "Resolve failed: $error")
                        }
                    })
                }
            }

            override fun onServiceLost(service: NsdServiceInfo) {}

            override fun onStartDiscoveryFailed(type: String, code: Int) {
                Log.e("NSD", "Start discovery failed: $code")
                nsdManager.stopServiceDiscovery(this)
            }

            override fun onStopDiscoveryFailed(type: String, code: Int) {
                Log.e("NSD", "Stop discovery failed: $code")
                nsdManager.stopServiceDiscovery(this)
            }

            override fun onDiscoveryStopped(serviceType: String) {
                Log.d("NSD", "Discovery stopped")
            }
        }

        nsdManager.discoverServices(
            "_http._tcp.",
            NsdManager.PROTOCOL_DNS_SD,
            discoveryListener
        )
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA
            val preview = Preview.Builder().build().also { p ->
                val previewView = findViewById<androidx.camera.view.PreviewView>(R.id.previewView)
                p.setSurfaceProvider(previewView.surfaceProvider)
            }

            cameraProvider.unbindAll()
            cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture)
        }, ContextCompat.getMainExecutor(this))
    }

    private fun takePictureAndSend() {
        val fileName = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US)
            .format(System.currentTimeMillis()) + ".jpg"
        val file = File(cacheDir, fileName)

        val outputOptions = ImageCapture.OutputFileOptions.Builder(file).build()

        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageSavedCallback {
                override fun onError(exc: ImageCaptureException) {
                    Log.e("CameraX", "사진 저장 실패", exc)
                    speakText("사진 저장에 실패했습니다.")
                }

                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    uploadImageToServer(file)
                }
            }
        )
    }

    private fun uploadImageToServer(file: File) {
        val host = serverHost ?: return
        val url = "http://$host:$serverPort/analyze-image"

        lifecycleScope.launch {
            try {
                val requestBody = MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart(
                        "image", file.name,
                        file.asRequestBody("image/jpeg".toMediaTypeOrNull())
                    )
                    .build()

                val request = Request.Builder()
                    .url(url)
                    .post(requestBody)
                    .build()

<<<<<<< HEAD
                val result = withContext(Dispatchers.IO) {
                    client.newCall(request).execute().body?.string() ?: "{}"
                }


=======
                val response = withContext(Dispatchers.IO) { client.newCall(request).execute() }
                val result = response.body?.string() ?: "{}"

>>>>>>> main
                val rawText = JSONObject(result).optString("tts_text", "")
                val cleanText = rawText
                    .replace(Regex("[\\*\\_\\~\\`]+"), "")
                    .replace(Regex("[\\[\\]\\(\\)]"), "")

                speakText(cleanText.ifEmpty { "결과를 가져오지 못했습니다." })
            } catch (e: IOException) {
                Log.e("Server", "전송 실패", e)
<<<<<<< HEAD
                speakText("서버 전송에 실패했습니다.")jiu
=======
                speakText("서버 전송에 실패했습니다.")
>>>>>>> main
            }
        }
    }

    private fun speakText(text: String) {
        Log.d("TTS", "Speak: $text")
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "utteranceId")
    }

    override fun onDestroy() {
        discoveryListener?.let { nsdManager.stopServiceDiscovery(it) }
        tts?.shutdown()
        super.onDestroy()
    }
}
