# Turn off Window Service Code with alexa. 

+ check below post
    
    https://lifeonroom.com/diy/remote-computer-off-2/ 


- Use Python36

- Operation
    * launch makeVenv.bat
    * launch activeVenv.bat
    * pip install -r requirements.txt
  
## makeVenv.bat
- make Virtualenv
    - Python path should be "c:\Python36" 
 
## activeVenv.bat
- activate virtualenv 


## make EXE file
 
pyinstaller --onefile --hidden-import win32timezone controlDeskTopService.py

## register Service 
dist\controlDeskTopService.exe install

## auto launch when booting 
crlt + alt + del -> Service -> DeskTopControl right click -> Open Service -> Remote Control Desktop Service -> Start type Auto
    

## Service end or delete
dist\controlDeskTopService.exe stop
dist\controlDeskTopService.exe remove