@echo off
echo まずは動画のもととなる画像を書き出すよ！
python3 MakeVideo.py
echo 次は動画を書き出すよ！
ffmpeg -r 30 -i output/%04d.png output.mp4
echo 動画の書き出しが終わったよ！
pause