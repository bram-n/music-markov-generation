const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs').promises;

// Create temp directories for file uploads and results
const UPLOAD_DIR = path.join('/tmp', 'uploads');
const RESULT_DIR = path.join('/tmp', 'result_output');

async function ensureDirectories() {
  await fs.mkdir(UPLOAD_DIR, { recursive: true });
  await fs.mkdir(RESULT_DIR, { recursive: true });
}

exports.handler = async (event, context) => {
  // Ensure CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers
    };
  }

  await ensureDirectories();

  if (event.path === '/api/upload' && event.httpMethod === 'POST') {
    try {
      const body = JSON.parse(event.body);
      const fileData = Buffer.from(body.file.split(',')[1], 'base64');
      const measures = body.measures || 8;
      
      // Save uploaded file
      const uploadPath = path.join(UPLOAD_DIR, 'input.mid');
      await fs.writeFile(uploadPath, fileData);

      // Run Python script
      const pythonProcess = spawn('python', [
        'markov_generator.py',
        uploadPath,
        measures.toString(),
        RESULT_DIR
      ]);

      const result = await new Promise((resolve, reject) => {
        let output = '';
        let error = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          error += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            resolve(output);
          } else {
            reject(new Error(`Python process exited with code ${code}: ${error}`));
          }
        });
      });

      // Read generated files
      const midiFile = await fs.readFile(path.join(RESULT_DIR, 'generated_melody.mid'));
      const xmlFile = await fs.readFile(path.join(RESULT_DIR, 'generated_melody.xml'));

      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          midiFile: midiFile.toString('base64'),
          xmlFile: xmlFile.toString('base64'),
          message: 'File processed successfully'
        })
      };
    } catch (error) {
      console.error('Error:', error);
      return {
        statusCode: 500,
        headers: {
          ...headers,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          error: 'Error processing file: ' + error.message
        })
      };
    }
  }

  return {
    statusCode: 404,
    headers,
    body: JSON.stringify({ error: 'Not Found' })
  };
}; 