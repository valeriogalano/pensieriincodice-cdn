
curl -o ./models/ggml-large-v3.bin -L 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin'            

ffmpeg -i ../pensieriincodice-cdn/public/episodes/PIC130.mp3 -acodec pcm_s16le -ar 16000 -ac 1 output.wav

 ./bin/whisper --language it -t 7 --print-colors --model ./models/ggml-large-v3.bin --output-srt --file output.wav  --output-file PIC132.srt

cat PIC131.yml | ollama run mistral "Prepare a summary of this podcast episode in italian language and generate tags"

