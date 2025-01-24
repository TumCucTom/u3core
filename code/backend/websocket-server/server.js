const WebSocket = require('ws');
const ffmpeg = require('fluent-ffmpeg');
const fs = require('fs');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Client connected');
  
  // Handle incoming stream request from client
  ws.on('message', (message) => {
    console.log('Received message:', message);
    const rtspUrl = message;

    // Transcode RTSP to MJPEG using FFmpeg and stream it to the WebSocket client
    ffmpeg(rtspUrl)
      .inputOptions('-re') // Real-time streaming
      .outputOptions('-f mjpeg') // Output format: MJPEG
      .outputOptions('-q:v 5') // Quality level
      .on('start', (commandLine) => {
        console.log('FFmpeg command line: ', commandLine);
      })
      .on('data', (data) => {
        // Send video frame as binary data to client
        ws.send(data);
      })
      .on('error', (err) => {
        console.error('FFmpeg error:', err);
      })
      .on('end', () => {
        console.log('Stream ended');
      })
      .pipe(); // Pipe output directly to the WebSocket stream
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });

  ws.on('error', (err) => {
    console.error('WebSocket error:', err);
  });
});

console.log('WebSocket server started on ws://localhost:8080');
