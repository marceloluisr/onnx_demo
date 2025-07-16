// Copyright (c)
// Licensed under the MIT License.

package ai.onnxruntime.example.imageclassifier

import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import ai.onnxruntime.*
import java.nio.FloatBuffer
import kotlin.random.Random
import java.io.File


class MainActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "SODBenchmark"
        private const val N_STEPS = 10
        private const val WIDTH = 224
        private const val HEIGHT = 224
        private const val CHANNELS = 3
        private const val BATCH_SIZE = 1
    }

    private lateinit var avgTimeText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        avgTimeText = findViewById(R.id.avgTimeText)

        try {
            runBenchmark()
        } catch (e: Exception) {
            Log.e(TAG, "Benchmark failed: ${e.message}", e)
            avgTimeText.text = "Benchmark error: ${e.message}"
        }
    }

    private fun runBenchmark() {
        Log.d(TAG, "Start")
        val ortEnv = OrtEnvironment.getEnvironment()
        Log.d(TAG, "Loading model")
        
        //val modelBytes = resources.openRawResource(R.raw.mobilenetv2_fp32).readBytes()
        //val inputStream = assets.open("u2net.onnx")
        //val modelBytes = inputStream.readBytes()
        
	val file = File("/data/local/tmp/flim_small.onnx")
	val modelBytes = file.readBytes()



        Log.d(TAG, "Model loaded")
        val session = ortEnv.createSession(modelBytes)

        val tensorSize = BATCH_SIZE * CHANNELS * HEIGHT * WIDTH
        var totalTime: Long = 0

        repeat(N_STEPS) { step ->
            val dummyData = FloatArray(tensorSize) { Random.nextFloat() }
            val floatBuffer = FloatBuffer.wrap(dummyData)
            val shape = longArrayOf(BATCH_SIZE.toLong(), CHANNELS.toLong(), HEIGHT.toLong(), WIDTH.toLong())
            val inputTensor = OnnxTensor.createTensor(ortEnv, floatBuffer, shape)
	   // val inputName = session.inputNames.iterator().next()
            //Log.d(TAG, "Model input name: $inputName")

            val start = SystemClock.elapsedRealtime()
            val outputs = session.run(mapOf("input" to inputTensor))
            val duration = SystemClock.elapsedRealtime() - start

            Log.d(TAG, "Run ${step + 1}: Inference time = $duration ms")
            totalTime += duration

            inputTensor.close()

            // Correct way to close outputs
            for ((_, value) in outputs) {
                value.close()
            }
        }

        val avgTime = totalTime / N_STEPS
        Log.d(TAG, "Average inference time over $N_STEPS runs: $avgTime ms")
        avgTimeText.text = "Average inference time: $avgTime ms"

        session.close()
        ortEnv.close()
    }
}

