const WebSocket = require('ws');
const ffmpeg = require('fluent-ffmpeg');
const fs = require('fs');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    console.log('Client connected');

    let frameBuffer = [];  // Array to store buffered frames

    // Start the interval to send frames every 5 seconds
    const sendInterval = setInterval(() => {
        console.log('Checking buffer...');
        if (frameBuffer.length > 0) {
            console.log('Sending frame...');
            ws.send(frameBuffer.shift()); // Send first frame and remove it from the buffer
            console.log('Frame sent');
        }
    }, 5000); // Send every 5 seconds

    ws.on('message', (message) => {
        // Convert the message (Buffer) to a string
        const rtspUrl = message.toString().replace('localhost', 'host.docker.internal');
        console.log('Received RTSP URL:', rtspUrl);

        // Start FFmpeg stream
        const ffmpegProcess = ffmpeg(rtspUrl)
            .inputOptions('-rtsp_transport', 'tcp') // Try using TCP transport
            .inputOptions('-re') // Real-time streaming
            .outputOptions('-f mjpeg') // Output format: MJPEG
            .outputOptions('-c:v mjpeg')  // Force MJPEG codec
            .outputOptions('-map 0:v:0') // Map the first video stream (adjust if needed)
            .outputOptions('-loglevel trace') // Detailed logging for debugging
            .on('start', (commandLine) => {
                console.log('FFmpeg command line: ', commandLine);
            })
            /*
            .on('stderr', (stderr) => {
                console.error('FFmpeg stderr: ', stderr); // Log stderr output
            })
            .on('stdout', (stdout) => {
                // Capture stdout to ensure there's no additional stream data you missed
                // For MJPEG, stdout might not be needed for frame data directly
                console.log('FFmpeg stdout: ', stdout);
            })
            */
            .on('stderr', (stderr) => {
                if (stderr.includes('Input')) {
                    console.log('FFmpeg started receiving data');
                    console.log('FFmpeg input:', stderr);
                }
                console.log('Error:', stderr);
            })
            .on('stdout', (stdout) => {
                // We can log stdout if needed, but we should focus on 'data' for frames
                console.log('FFmpeg stdout output (not frames):', stdout);
            })
            .on('data', (data) => {
                // Buffer video frames (use 'data' from FFmpeg's output)
                console.log('Received frame:', data.length);
                frameBuffer.push(data);
            })
            .on('error', (err) => {
                console.error('FFmpeg error:', err);  // Handle FFmpeg errors
            })
            .on('end', () => {
                console.log('Stream ended');
            })
            .pipe(); // Pipe output to stdout for further handling
    });

    ws.on('close', () => {
        console.log('Client disconnected');
        // Clear interval when client disconnects
        clearInterval(sendInterval);
    });

    ws.on('error', (err) => {
        console.error('WebSocket error:', err);
    });
});

console.log('WebSocket server started on ws://localhost:8080');
