import requests
url='https://vdept.bdstatic.com/694b46596a625469463965534a635a54/394553786e586636/b933a9ea84147c047367dad96805eed7cb75707a968c7003fad72f1b8ed190241ad925fd31ca99775e140661439a85e2.mp4?auth_key=1593330583-0-0-b2ccdfed8d2965f982edcce5152faef7'

response=requests.get(url).content

print('开始保存')
with open(r'F:\vidio\我不是药神老奶奶.mp4','wb')as f:
    f.write(response)
print('保存完毕')
