@echo off
echo �܂��͓���̂��ƂƂȂ�摜�������o����I
python3 MakeVideo.py
echo ���͓���������o����I
ffmpeg -r 30 -i output/%04d.png output.mp4
echo ����̏����o�����I�������I
pause