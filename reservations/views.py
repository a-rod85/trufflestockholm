from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from .models import Table, Customer, Reservation
from .forms import CustomerForm, Reservations


def get_customer_instance(request, User):
    customer_email = request.user.emailcustomer = Customer.objects.filter(email=customer_email).first()
    return customer_email


def retrieve_reservations(self, request, User):
    if len(Customer.objects.filter(email=customer_email)) !=0:
        current_customer = Customer.objects.get(email=customer_email)
        current_customer_id = current_customer.pk
# If customer exists in model
        current_customer = Customer.objects.get(email=customer_email)
        current_customer_id = current_customer.pk

        # Get any reservations for the customer
        get_reservations = (
            Reservation.objects.filter(customer=current_customer_id)
            .values()
            .order_by("requested_date")
        )

        if len(get_reservations) == 0:
            return None
        else:
            return get_reservations
    else:
        # If user is not present in customer model """
        return None


def validate_date(self, request, reservations):
    today = datetime.datetime.now().date()
    for reservation in reservations:
        if reservation["requested_date"] < today:
            reservation["status"] = "expired"

        return reservations


# Create your views here.
class ReservationsEnquiry(View):
    """Reservations Enquiry view allows customers to make reservation enquiries"""

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            if customer is None:
                email = request.user.email
                customer_form = CustomerForm(initial={"email": email})
            else:
                customer_form = CustomerForm(instance=customer)
            reservation_form = ReservationForm()

        else:
            customer_form = CustomerForm()
            reservation_form = ReservationForm()

        return render(
            request,
            "reservations.html",
            {"customer_form": customer_form, "reservation_form": reservation_form},
        )

    def post(self, request, User=User, *args, **kwargs):
        # Get post data from forms
        customer_form = CustomerForm(data=request.POST)
        reservation_form = ReservationForm(data=request.POST)

        if customer_form.is_valid() and reservation_form.is_valid():
            # Retrieve information from forms
            customer_requested_date = request.POST.get("requested_date")
            customer_requested_time = request.POST.get("requested_time")
            customer_requested_guests = request.POST.get("no_of_guests")
            customer_name = request.POST.get("full_name")

            # Convert date into format required by django
            date_formatted = datetime.datetime.strptime(
                customer_requested_date, "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

            customer_email = request.POST.get("email")
            # See if customer already exists in model """
            customer_query = len(Customer.objects.filter(email=customer_email))

            # Prevent duplicate 'customers' being added to database """
            if customer_query > 0:
                pass
            else:
                customer_form.save()

            # Retrieve customer information to pass to reservation model """
            current_customer = Customer.objects.get(email=customer_email)
            current_customer_id = current_customer.pk
            customer = Customer.objects.get(customer_id=current_customer_id)

            reservation = reservation_form.save(commit=False)
            # Pass formatted date & customer in to model """
            reservation.requested_date = date_formatted
            reservation.customer = customer
            # Save reservation """
            reservation_form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Thank you {customer_name}, your enquiry for "
                f"{customer_requested_guests} people at "
                f"{customer_requested_time} on "
                f"{customer_requested_date} has been sent.",
            )

            # Return blank forms so the same enquiry isn't sent twice """
            url = reverse("reservations")
            return HttpResponseRedirect(url)

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Something is not right with your form "
                "- please make sure your email address & phone number in the"
                " correct format.",
            )

        return render(
            request,
            "reservations.html",
            {"customer_form": customer_form, "reservation_form": reservation_form},
        )


class ManageReservations(View):
    """Manage Reservations view allows customer to maanage
    any existing enquiries"""

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            customer = get_customer_instance(request, User)
            current_reservations = retrieve_reservations(self, request, User)

            if current_reservations is None:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "You've not got any existing "
                    "reservations. You can make reservations here.",
                )
                url = reverse("reservations")
                return HttpResponseRedirect(url)

            else:
                validate_date(self, request, current_reservations)
                return render(
                    request,
                    "manage_reservations.html",
                    {"reservations": current_reservations, "customer": customer},
                )

        else:
            # Prevent customer not logged in from accessing this page
            messages.add_message(
                request,
                messages.ERROR,
                "You must be logged in to " "manage your reservations.",
            )

            url = reverse("reservations")
            return HttpResponseRedirect(url)


class EditReservation(View):
    """View for user to be able to edit their existing reservations"""

    def get(self, request, reservation_id, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            # Get reservation object based on id
            reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
            # Prevent customers editing expired reservations
            today = datetime.datetime.now().date()
            if reservation.requested_date < today:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You are trying to edit a " "reservation that is in the past.",
                )
                url = reverse("manage_reservations")
                return HttpResponseRedirect(url)
            # Prevent customers editing rejected reservations
            elif reservation.status == "rejected":
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You are trying to edit a " "reservation that has been rejected.",
                )
                url = reverse("manage_reservations")
                return HttpResponseRedirect(url)
            else:
                # Convert date to display in dd/mm/YYYY format
                date_to_string = reservation.requested_date.strftime("%d/%m/%Y")
                reservation.requested_date = date_to_string

                # Get customer info
                customer = get_customer_instance(request, User)

                # Compare names of reservation owner and user
                reservation_owner = reservation.customer
                name_of_user = customer

                if reservation_owner != name_of_user:
                    # If the names do not match redirect to manage reservations
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "You are trying to edit a " "reservation that is not yours.",
                    )
                    url = reverse("manage_reservations")
                    return HttpResponseRedirect(url)

                else:
                    # return both forms with the existing information
                    customer_form = CustomerForm(instance=customer)
                    reservation_form = ReservationForm(instance=reservation)

                    return render(
                        request,
                        "edit_reservation.html",
                        {
                            "customer_form": customer_form,
                            "customer": customer,
                            "reservation_form": reservation_form,
                            "reservation": reservation,
                            "reservation_id": reservation_id,
                        },
                    )

        else:
            # Prevent users not logged in from accessing this page
            messages.add_message(
                request,
                messages.ERROR,
                "You must be logged in to " "manage your reservations.",
            )

            url = reverse("reservations")
            return HttpResponseRedirect(url)

    def post(self, request, reservation_id, User=User, *args, **kwargs):
        customer = get_customer_instance(request, User)
        # get reservation from database
        reservation_id = reservation_id
        reservation = get_object_or_404(Reservation, reservation_id=reservation_id)

        reservation_form = ReservationForm(data=request.POST, instance=reservation)
        customer_form = CustomerForm(instance=customer)

        if reservation_form.is_valid():
            # get the post information from the form
            customer_requested_date = request.POST.get("requested_date")
            customer_requested_time = request.POST.get("requested_time")
            # Convert date into format required by django
            date_formatted = datetime.datetime.strptime(
                customer_requested_date, "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

            # Update the existing reservation with the form data.
            reservation.reservation_id = reservation_id
            reservation.requested_time = customer_requested_time
            # Pass formatted date to prevent it from saving incorrectly
            reservation.requested_date = date_formatted
            reservation.requested_guests = request.POST.get("no_of_guests")
            # Change status to pending as the admin needs to approve
            reservation.status = "pending"
            reservation_form.save(commit=False)
            reservation_form.save()
            messages.info(
                request, f"Reservation {reservation_id} has now" " been updated."
            )
            # Retreive new list of reservations to display
            current_reservations = retrieve_reservations(self, request, User)
            validate_date(self, request, current_reservations)
            # Return user to manage reservations page
            return render(
                request,
                "manage_reservations.html",
                {"reservations": current_reservations},
            )

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Something is not right with your form "
                "- please make sure your email address & phone number are "
                "entered in the correct format.",
            )

        return render(
            request,
            "edit_reservation.html",
            {
                "reservation_form": reservation_form,
                "customer_form": customer_form,
                "reservation": reservation,
                "customer": customer,
            },
        )


class DeleteReservation(View):
    """View for user to delete reservations"""

    def get(self, request, reservation_id, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            reservation = get_object_or_404(Reservation, reservation_id=reservation_id)
            customer = get_customer_instance(request, User)
            # Prevent customers editing expired reservations
            today = datetime.datetime.now().date()
            if reservation.requested_date < today:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You are trying to cancel a " "reservation that is in the past.",
                )
                url = reverse("manage_reservations")
                return HttpResponseRedirect(url)
            else:
                # Delete customers reservation
                return render(
                    request,
                    "delete_reservation.html",
                    {
                        "customer": customer,
                        "reservation": reservation,
                        "reservation_id": reservation_id,
                    },
                )
        else:
            # Prevent users not logged in from accessing this page
            messages.add_message(
                request,
                messages.ERROR,
                "You must be logged in to " "manage your reservations.",
            )

            url = reverse("reservations")
            return HttpResponseRedirect(url)

    def post(self, request, reservation_id, User=User, *args, **kwargs):
        # get reservation from database
        reservation_id = reservation_id
        reservation = Reservation.objects.get(pk=reservation_id)
        # Delete the reservation
        reservation.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Reservation {reservation_id} has now " "been cancelled.",
        )
        # Get updated list of reservations
        current_reservations = retrieve_reservations(self, request, User)
        # Return user to manage reservations page
        validate_date(self, request, current_reservations)
        return render(
            request, "manage_reservations.html", {"reservations": current_reservations}
        )


class EditCustomerDetails(View):
    """View for user to be able to edit their information"""

    def get(self, request, User=User, *args, **kwargs):
        if request.user.is_authenticated:
            # Get customer object based on user
            customer = get_customer_instance(request, User)
            if customer is None:
                # If 'customer' does not exist return user email
                email = request.user.email
                customer_form = CustomerForm(initial={"email": email})
            else:
                # return both forms with the existing information
                customer_form = CustomerForm(instance=customer)

            return render(
                request,
                "edit_customer_details.html",
                {
                    "customer_form": customer_form,
                    "customer": customer,
                },
            )

        else:
            # If user not logged in redirect to reservations page
            messages.add_message(
                request,
                messages.ERROR,
                "You must be logged in to update your " "details.",
            )

            url = reverse("reservations")
            return HttpResponseRedirect(url)

    def post(self, request, User=User, *args, **kwargs):
        customer = get_customer_instance(request, User)
        customer_form = CustomerForm(data=request.POST, instance=customer)

        # Prevent duplicate 'customers' being added to database
        if customer_form.is_valid():
            if customer is None:
                customer_form.save()
                messages.add_message(
                    request, messages.SUCCESS, "Your details have now been added."
                )
            else:
                if customer_form.has_changed():
                    # get the information from the form
                    customer_full_name = request.POST.get("full_name")
                    customer_phone_number = request.POST.get("phone_number")

                    customer_form.save(commit=False)
                    # Update customer instance with new information
                    customer.full_name = customer_full_name
                    customer.phone_number = customer_phone_number
                    customer_form.save()
                    messages.add_message(
                        request, messages.SUCCESS, "Your details have now been updated."
                    )

                    return render(
                        request,
                        "edit_customer_details.html",
                        {
                            "customer_form": customer_form,
                            "customer": customer,
                        },
                    )

                else:
                    # If no information has changed
                    messages.add_message(
                        request, messages.WARNING, "No information has changed."
                    )
                    return render(
                        request,
                        "edit_customer_details.html",
                        {
                            "customer_form": customer_form,
                            "customer": customer,
                        },
                    )

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Something is not right with your form "
                "please make sure your email address & phone number "
                "are entered in the correct format.",
            )

        return render(
            request,
            "edit_customer_details.html",
            {
                "customer_form": customer_form,
                "customer": customer,
            },
        )
