import subprocess

def mail_to_user(threshold,moisture):
    message = "echo 'お水をください・・・\nWEBページへお願いします\n'"
    url     = "'⇒[http://210.152.14.37/AIoT/datalist/]'"
    th      = "'\n閾値　　　　：'" + str(threshold)
    mo      = "'\n現在の水分量：'" + str(moisture)
    subject = "[至急]水分が不足しています・・・"
    to_add  = " shimamura@mobcom.ait.kyushu-u.ac.jp"
    print("mail")
    subprocess.getoutput(message+" "+url+th+mo+"  | mail -s "+ subject + " " +to_add)