from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from base.models import (

    Leave,
    Employee,

) 


def send_mail_new_employee(email, password):
    try:
        get_user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User with the given email does not exist.")

    context = {
        'first_name': get_user.first_name,
        'last_name': get_user.last_name,
        'password': password,
        'email': email,
        'year': datetime.now().year, 
    }

    receiver_email = email
    template_name = "notification/receiver_info.html"
    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=context,
    )

    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject="Welcome to izyane",
        message=plain_message,
        from_email="your_email@example.com",
        recipient_list=[receiver_email],
        html_message=convert_to_html_content,
        fail_silently=True,  
    )
    return HttpResponse("Email sent successfully.")


class VetLeaveNotification:
    def __init__(self, leave_id, action):
        self.leave_id = leave_id
        self.action = action
        if self.action == "Approved":
            self.message_body = "Your leave application has been granted. Enjoy your holiday!"
        else:
            self.message_body = "We regret to inform you that your leave application has been denied."

        self.applicant_email = None
        self.applicant_first_name = None
        self.applicant_last_name = None
        self.hr_email = None

        try:
            # Get leave object
            leave_obj = Leave.objects.get(id=self.leave_id)
            self.applicant_email = leave_obj.user.email
            self.applicant_first_name = leave_obj.user.first_name
            self.applicant_last_name = leave_obj.user.last_name
        except ObjectDoesNotExist:
            raise ValueError("Invalid leave ID. Leave application not found.")

        try:
            employee_obj = Employee.objects.get(position="HR")
            self.hr_email = employee_obj.user.email
        except ObjectDoesNotExist:
            self.hr_email = "hr@example.com" 
        self.validate_email(self.applicant_email)

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(f"Invalid email address: {email}")

    def send_mail_application(self):
        context = {
            "message": self.message_body,
            "first_name": self.applicant_first_name,
            "last_name": self.applicant_last_name,
        }

        receiver_email = self.applicant_email
        template_name = "notification/leave_application_info.html"

        
        convert_to_html_content = render_to_string(template_name=template_name, context=context)
        plain_message = strip_tags(convert_to_html_content)

        # Send email
        send_mail(
            subject="Your leave application",
            message=plain_message,
            from_email="your_email@example.com",
            recipient_list=[receiver_email],
            html_message=convert_to_html_content,
            fail_silently=False,  
        )
        return HttpResponse("Email sent successfully.")




        


    

