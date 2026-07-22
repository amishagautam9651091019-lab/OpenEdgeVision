#houduantuiliu
ffmpeg -re -stream_loop -1 -i "/home/fjut/video/uav-traffic.mp4" -an -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -r 25 -g 50 -f rtsp -rtsp_transport tcp rtsp://127.0.0.1:8554/drone01

#di zhenglv tui liu
ffmpeg -re -stream_loop -1 -i "/home/fjut/video/uav-traffic.mp4" -an -vf "scale=1280:-2,fps=20" -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -bf 0 -g 20 -keyint_min 20 -sc_threshold 0 -b:v 1200k -maxrate 1200k -bufsize 2400k -f rtsp -rtsp_transport tcp rtsp://127.0.0.1:8554/drone01

