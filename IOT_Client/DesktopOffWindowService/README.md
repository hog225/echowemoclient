# 알렉사로 컴퓨터를 끄기위한 Window Service Code 입니다. 
https://lifeonroom.com/diy/remote-computer-off-2/ 를 참조하세요 ^^

- Python 36
- makeVenv.bat - 가상환경 생성 (Python 설치 경로가 c:\Python36 이어야함)
- activeVenv.bat - 가상환경 실행 


* 실행파일 만들기 
pyinstaller --onefile --hidden-import win32timezone controlDeskTopService.py

* 실행파일 서비스 등록 
dist\controlDeskTopService.exe install

* 서비스 booting 시 자동 실행 
crlt + alt + del -> 서비스 -> DeskTopControl 우클릭 -> 서비스 열기 -> Remote Control Desktop Service -> 시작유형 자동

* 실행파일 서비스 종료 및 제거 
dist\controlDeskTopService.exe stop
dist\controlDeskTopService.exe remove