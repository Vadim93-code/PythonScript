import csv
import glob
from PIL import ImageDraw, ImageFont, Image

import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# функция опредиления месяца
def DateDef(month):
    if month == "1":
        return "January"
    elif month == "2":
        return "February"
    elif month == "3":
        return "March"
    elif month == "4":
        return "April"
    elif month == "5":
        return "May"
    elif month == "6":
        return "June"
    elif month == "7":
        return "July"
    elif month == "8":
        return "August"
    elif month == "9":
        return "September"
    elif month == "10":
        return "October"
    elif month == "11":
        return "November"
    elif month == "12":
        return "December"

sender = "coffemobile1@gmail.com" # емейл отправителя
password = "(Vadim11453365)"      # пароль отправителя

# функция отправки сертификатов
def SendMessage(namber, email):
    def send_email():

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender, password)

            msg = MIMEMultipart()
            msg["Subject"] = "Document"
            msg["From"] = sender
            msg["To"] = sender

            msg.attach(MIMEText("Ваш сертификат")) #текст сообщения

            with open(f"Imags/{namber}.jpeg", "rb") as f:
                file = MIMEImage(f.read())

            file.add_header('content-disposition', 'attachment', filename=f'{namber}.jpeg')
            msg.attach(file)

            server.sendmail(sender, f"{email}", msg.as_string())

            return "Ok"
        except Exception as _ex:
            return f"{_ex}\n Check your login or password please"

    def main():
        print(send_email())

    if __name__ == "__main__":
        main()

# функия добавления текста на изображения
def addTexInImage(Competition, FirstName, LastName, Distans, Date, Time, Namber, Email):
    im = Image.open('./Doc/Image.jpg')
    draw_text = ImageDraw.Draw(im)
    # fonts
    font = './Font/Roboto-Regular.ttf'
    CompetitionFont = ImageFont.truetype(font, 30)
    FirstNameFont = ImageFont.truetype(font, 60)
    DateFont = ImageFont.truetype(font, 25)
    TimeFont = ImageFont.truetype(font, 110)
    TimeTextFont = ImageFont.truetype(font, 35)

    # Вывод цыетной полоски
    widthImg = len(Competition) * 20
    imgBlue = Image.new('RGB', (widthImg, 50), color=('#8C50DA'))
    NewDrawText = ImageDraw.Draw(imgBlue)
    NewDrawText.text((5,7), Competition, font=CompetitionFont)
    im.paste(imgBlue, (70, 300))

    # Вывод даты
    date = Date.split("/")
    month = DateDef(date[1])
    NewDate = f"{month} {date[0]}, 20{date[2]}"

    # Вывод елементов
    FulName = FirstName + " " + LastName
    DateAndDistans = NewDate + "    |    " + Distans
    TimeText = "---------   FINISH TIME   ---------"

    draw_text.text(
        (70, 350),
        FulName,
        font=FirstNameFont
    )
    draw_text.text(
        (70, 420),
        DateAndDistans,
        font=DateFont
    )
    draw_text.text(
        (90, 450),
        Time,
        font=TimeFont
    )
    draw_text.text(
        (70, 570),
        TimeText,
        font=TimeTextFont
    )

    im.save(f"./Imags/{Namber}.jpeg")
    # im.show()
    SendMessage(Namber, Email)

# Выбираем файл с папки
CvsFiles = []
for file in glob.glob("./Cvs/*.cvs"):
    CvsFiles.append(file)

NameFileCvs = CvsFiles[0].split("\\")

with open(f"Cvs/{NameFileCvs[1]}", encoding='UTF-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter = ",")
    # Счетчик для подсчета количества строк
    count = 0
    # Считывание данных из CSV файла
    for row in file_reader:
        if count != 0:
            addTexInImage(f"{row[1]}", f"{row[3]}", f"{row[2]}", f"{row[6]}", f"{row[7]}", f"{row[8]}", f"{row[0]}", f"{row[5]}")
        count += 1
