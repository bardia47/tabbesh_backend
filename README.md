# tabbesh.ir web app


**if you don't use backup 
add this to your database**

`accounts_role` :  {id=1,code='1',title='دانش آموز'}{id=2,code='2',title='ادمین'}{id=3,code='3',title='دبیر'}

**if using windows:**
 
 ***for install gettext:***
 
 download the precompiled binary installer. Download the "static" flavor of your Operating System (32bit or 64bit) and simple run the installer.
https://mlocati.github.io/articles/gettext-iconv-windows.html

Update the system PATH:

Control Panel > System > Advanced > Environment Variables

In the System variables list, click Path, click Edit and then New. Add C:\Program Files\gettext-iconv\bin value.

***for install reddis:***

 https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504
 
 
#### for backend developers : 
use `pip freeze > requirements.txt` to add your libraries to site

 - `pip install -r requirements.txt`
