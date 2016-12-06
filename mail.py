import subprocess

def mail_to_user():
    message = "echo お水をください・・・、ページへ飛んでね・・・"
    url     = "ウェブページだよ"
    subject = "[至急]助けて・・・"
    to_add  = " shimamura@mobcom.ait.kyushu-u.ac.jp"
    subprocess.getoutput(message+" "+url+" | mail -s "+ subject + " " +to_add)