# �˷���� ��ǻ�͸� �������� Window Service Code �Դϴ�. 
https://lifeonroom.com/diy/remote-computer-off-2/ �� �����ϼ��� ^^

- Python 36
- makeVenv.bat - ����ȯ�� ���� (Python ��ġ ��ΰ� c:\Python36 �̾����)
- activeVenv.bat - ����ȯ�� ���� 


* �������� ����� 
pyinstaller --onefile --hidden-import win32timezone controlDeskTopService.py

* �������� ���� ��� 
dist\controlDeskTopService.exe install

* ���� booting �� �ڵ� ���� 
crlt + alt + del -> ���� -> DeskTopControl ��Ŭ�� -> ���� ���� -> Remote Control Desktop Service -> �������� �ڵ�

* �������� ���� ���� �� ���� 
dist\controlDeskTopService.exe stop
dist\controlDeskTopService.exe remove