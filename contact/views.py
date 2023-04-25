from django.shortcuts import render
from contact import views

# Create your views here.


def homepage(request):
    return render(request, "index.html")


def send_message(request, Contact_form):
    customer_fname = contact_form.cleaned_data["first_name"]
    customer_lname = contact_form.cleaned_data["last_name"]
    email_from = contact_form_data["email_address"]
    subject = "Message from {customer_fname}, {customer_lname}, {email_from}"
    message = contact_form.cleaned_data["message"]
    recipient_list = []
    send_mail(subject, message, email_form, recipient_list)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_message(request, form)

        messages.add_message(
            request, messages.SUCCESS, "GREAT, your message is sent!"
        )

    form = ContactForm()
    return render(request, "", {"form": form})
