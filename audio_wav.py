# -- utf-8 --#
import wave
import pyaudio
import numpy
import pylab

#打开wav格式音频文件
wf = wave.open("C:\\test.wav", "rb")
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
nframes = wf.getnframes()
framerate = wf.getframerate()
str_data = wf.readframes(nframes)
wf.close()
wave_data = numpy.fromstring(str_data, dtype=numpy.short)
wave_data.shape = -1,2
wave_data = wave_data.T

#采样，pylab绘制频谱图
N = 48000
start = 3000
df = framerate/(N-1)
freq = [df*n for n in range(0,N)]
wave_data2=wave_data[0][start:start+N]
c=numpy.fft.fft(wave_data2)*2/N
d=int(len(c)/2)
while freq[d] > 1500:
    d -= 10
pylab.plot(freq[:d-1],abs(c[:d-1]),'r')
pylab.show()

#一个简单的判断
testdate = abs(c[800])
print(testdate)
if testdate > 900:
    print("PASS")
else:
    print("NG")

