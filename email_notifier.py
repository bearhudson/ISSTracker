import smtplib

from main import EMAIL
from main import FROM
from main import PASS


def send_message(position, miles):
    with smtplib.SMTP_SSL('smtp.gmail.com') as connection:
        connection.login(user=EMAIL, password=PASS)
        connection.sendmail(
            from_addr=FROM,
            to_addrs=EMAIL,
            msg=f"Subject:☝️Look Up!☝\nThe ISS should be above.\n"
                f"Current position: {position}\n"
                f"Distance: {miles}"
        )
