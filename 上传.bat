@echo off
git add .
set /p a= ������commit��
git commit -m %a%
git push