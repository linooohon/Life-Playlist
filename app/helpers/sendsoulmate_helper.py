import logging
from app.model.models import User, Soulmate_Record
from app import db, mail
from flask_mail import Mail, Message
from app.settings import MAIL_USERNAME, MAIL_USERNAME, SENDGRID_API_KEY, MAIL_DEFAULT_SENDER
from flask import render_template
from smtplib import SMTPException


# 檢查送信紀錄是否已有
def check_soulmate_record_in_db(original_email, soulmate_email, db_artistsong_lowerstrip):
    record_samesong_lists = []
    pre_record_soulmate_lists = []
    pre_record_lists = Soulmate_Record.query.filter_by(
        original_email=original_email).all()
    
    for pre_record in pre_record_lists:
        pre_record_soulmate_lists.append(pre_record.soulmate_email)

    if soulmate_email in pre_record_soulmate_lists:
        record_lists = Soulmate_Record.query.filter_by(
            original_email=original_email, soulmate_email=soulmate_email).all()
        
        for record in record_lists:
            record_samesong_lists.append(record.same_song)
        
        if db_artistsong_lowerstrip in record_samesong_lists:
            print(
                f"{original_email} had same song with {soulmate_email} before, so don't send again")
            return False
        else:
            print('Find Soulmate !')
            return True

    else:
        print('Find Soulmate !')
        return True


# 把此次送信紀錄記在 db
def save_soulmate_record_to_db(original_email, soulmate_email, db_artistsong_lowerstrip):
    new_soulmate_record_item = Soulmate_Record(
        original_email=original_email, soulmate_email=soulmate_email, same_song=db_artistsong_lowerstrip)
    db.session.add(new_soulmate_record_item)
    db.session.commit()


# 寄信
# email setting for sending soulemate's email to user
def send_mail(current_user_email, soulmate_email, soulmate_firstname):
    print("start to sent email")
    msg_title = 'Talk to your life playlist soulmate'
    msg_recipients = [current_user_email]
    msg = Message(msg_title, sender=MAIL_DEFAULT_SENDER,
                  recipients=msg_recipients)
    msg.html = render_template(
        'soulmate_mail.html', soulmate_email=soulmate_email, soulmate_firstname=soulmate_firstname)
    try:
        mail.send(msg)
    except SMTPException as e:
        logging.error(e.message)
        
    return 'You Send Mail by Flask-Mail Success!!'



# 找出目前 user 的 artistsong lowerstrip list, 變小寫, 去空格
def current_artistsong_lowerstrip(current_user):
    current_artistsong_lowerstrip_list = []
    for i in current_user.playlists:
        current_artistsong = i.__dict__['artist'] + i.__dict__['song']
        current_artistsong_lowerstrip = ''.join(
            current_artistsong.lower().strip().split())
        current_artistsong_lowerstrip_list.append(
            current_artistsong_lowerstrip)
    return current_artistsong_lowerstrip_list


# 從 db loop 每個 user 的 playlist 看有沒有歌出現在現在這個當前 user 的 playlist
def loop_all_user_playlist(current_user, all_user, current_artistsong_lowerstrip_list):
    samesong_list = []
    for i in all_user:
        for j in i.playlists:
            db_artistsong = j.__dict__['artist'] + j.__dict__['song']
            db_artistsong_lowerstrip = ''.join(
                db_artistsong.lower().strip().split())
            if db_artistsong_lowerstrip in current_artistsong_lowerstrip_list and i.id is not current_user.id \
                    and db_artistsong_lowerstrip not in samesong_list:
                samesong_list.append(db_artistsong_lowerstrip)
                if len(samesong_list) >= 1:
                    # print(i.id)
                    # print(i.email)
                    your_soulmate_email = i.email
                    your_soulmate_firstname = i.first_name
                    need_send_email = check_soulmate_record_in_db(
                        current_user.email, your_soulmate_email, db_artistsong_lowerstrip)
                    if need_send_email:
                        save_soulmate_record_to_db(
                            current_user.email, your_soulmate_email, db_artistsong_lowerstrip)
                        send_mail(current_user.email, your_soulmate_email,
                                  your_soulmate_firstname)


def check_same_song_lover():
    logging.basicConfig(
        filename="send_soulmate_email.log", level=logging.INFO)
    logging.info("========Start to update========")
    all_user = User.query.all()
    for user in all_user:
        current_artistsong_lowerstrip_list = current_artistsong_lowerstrip(
            user)
        # 從 db 找全部 playlist 看有沒有歌出現在現在這個 user 的 playlist
        loop_all_user_playlist(user, all_user,
                               current_artistsong_lowerstrip_list)
    print("Finish updated")
    logging.info("=========Finish updated=========")












# Legacy
# def send_mail(current_user_email, soulmate_email, soulmate_firstname):
#     print("start to sent email")
#     msg_title = 'Talk to your life playlist soulmate'
#     msg_recipients = [current_user_email]
#     # msg_body = f"your life playlist soulmate's email is {soulmate_email}"
#     msg = Message(msg_title, sender=MAIL_DEFAULT_SENDER,
#                   recipients=msg_recipients)
#     # msg.body = msg_body
#     msg.html = render_template(
#         'soulmate_mail.html', soulmate_email=soulmate_email, soulmate_firstname=soulmate_firstname)
#     mail.send(msg)
#     return 'You Send Mail by Flask-Mail Success!!'


# Legacy
# def send_mail(current_user_email, soulmate_email, soulmate_firstname):
#     sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
#     from_email = Email("lifeplaylistsmtp@gmail.com")
#     to_email = To("linooohon@gmail.com")
#     subject = "Sending with SendGrid is Fun"
#     content = Content("text/html", "123")
#     mail = Mail(from_email, to_email, subject, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
#     return 'You Send Mail by Flask-Mail Success!!'
