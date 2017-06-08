import subprocess

def mail_to_user(threshold,moisture):
    message = "echo '現在水分が不足しています\nWEBページからお水をお願いします\n'"
    url     = "'⇒[http://210.152.14.37/AIoT/datalist/]'"
    th      = "'\n閾値　　　　：'" + str(threshold)
    mo      = "'\n現在の水分量：'" + str(moisture)
    subject = "[至急]水分が不足しています"
    to_add2  = " shimamura@mobcom.ait.kyushu-u.ac.jp"
    to_add  = " konoacc@gmail.com"
    print("mail")
    subprocess.getoutput(message+" "+url+th+mo+"  | mail -s "+ subject + " " +to_add2)