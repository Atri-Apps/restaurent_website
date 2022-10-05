from .atri import Atri
from fastapi import Request, Response
from atri_utils import *
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def set_data(at: Atri, data):
    for i in range(1, 6):
        instance: at.Flex13.__class__ = getattr(at, f'Flex13{i}')
        instance.styles.display = 'none'
    for i in range(1, int(data['rating']) + 1):
        instance: at.Flex13.__class__ = getattr(at, f'Flex13{i}')
        instance.styles.display = 'flex'
    # Comment
    instance: at.TextBox1.__class__ = getattr(at, 'TextBox78')
    instance.custom.text = instance.custom.text[0] + data['review'] + instance.custom.text[-1]

    # Review
    instance: at.TextBox1.__class__ = getattr(at, 'TextBox79')
    instance.custom.text = data['comment']

    # Place
    instance: at.TextBox1.__class__ = getattr(at, 'TextBox80')
    instance.custom.text = data['place']

    # Name
    instance: at.TextBox1.__class__ = getattr(at, 'TextBox81')
    instance.custom.text = data['name']

    # Image
    instance: at.Image74.__class__ = getattr(at, 'Image40')
    instance.custom.src = "/app-assets/" + data['image']


def init_state(at: Atri):
    """
    This function is called everytime "Publish" button is hit in the editor.
    The argument "at" is a dictionary that has initial values set from visual editor.
    Changing values in this dictionary will modify the intial state of the app.
    """
    pass


def handle_page_request(at: Atri, req: Request, res: Response, query: str):
    """
    This function is called whenever a user loads this route in the browser.
    """
    at.TextBox142.custom.text = '1'
    fd = open('reviews.json')
    data = json.load(fd)
    at.Flex130.styles.display = 'none'
    at.Flex137.styles.display = 'none'
    set_data(at, data[0])
    pass


def handle_event(at: Atri, req: Request, res: Response):
    """
    This function is called whenever an event is received. An event occurs when user
    performs some action such as click button.
    """
    if at.Image74.onClick:
        fd = open('reviews.json')
        data = json.load(fd)
        idx = int(at.TextBox142.custom.text)
        if idx == 1:
            pass
        else:
            at.TextBox142.custom.text = str(idx - 1)
            set_data(at, data[idx-2])

    if at.Image75.onClick:
        fd = open('reviews.json')
        data = json.load(fd)
        idx = int(at.TextBox142.custom.text)
        if idx == len(data):
            pass
        else:
            at.TextBox142.custom.text = str(idx + 1)
            set_data(at, data[idx])

    if at.Button21.onClick:
        name = at.Input1.custom.value.strip()
        email = at.Input2.custom.value.strip()
        user_msg = at.Input9.custom.value.strip()
        phone = at.Input4.custom.value.strip()
        location = at.Input3.custom.value.strip()
        date = at.Input6.custom.value.strip()
        schedule = at.Input5.custom.value.strip()

        message = Mail(
            from_email='sanskarg348@gmail.com',
            to_emails='19803023@mail.jiit.ac.in',
            subject='Sending with Twilio SendGrid is Fun',
            html_content=f'Hey Restaurant-x this is {name} my email is {email} and my query for you is {user_msg} the '
                         f'contact number is {phone} and my location {location} the date would be {date} and timing '
                         f'would be {schedule}')
        try:

            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            print(message)
            response = sg.send(message)
            at.Flex137.styles.display = 'flex'
        except Exception as e:
            print(e)
