from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from guest_user.decorators import allow_guest_user
from django.contrib import messages
from  .forms import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.http import *

from django.core.paginator import Paginator


@login_required(login_url='job_list')
def logout_view(request):
    logout(request)
    return redirect('job_list')


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags




@allow_guest_user
def job_list(request):
    user = request.user
    q = request.GET.get('q', '')
    skills = request.GET.getlist('skills')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Build the filter conditions
    filter_conditions = Q(title__icontains=q)
    if skills:
        filter_conditions &= Q(skills__id__in=skills)
    if price_min and price_max:
        filter_conditions &= Q(Price__range=(price_min, price_max))

    # Perform the search query
    jobs = Job.objects.filter(filter_conditions)


   
    all_skills = Skill.objects.all()

    items_per_page = 10
    
    paginator = Paginator(jobs, items_per_page)
    
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    

    return render(request, 'job_list.html', {'jobs': jobs,"all_skills":all_skills , "page":page})


@allow_guest_user
def job_detail(request, job_id):
    user = request.user
    job = get_object_or_404(Job, id=job_id)
    proposals = Proposal.objects.filter(project=job)
    if request.user.is_authenticated:
        is_applied = proposals.filter(freelancer=user).exists()
    else:
        messages.info(request, "Please login to apply for this job.")
        return redirect('job_list')
    
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)

        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.freelancer = request.user
            proposal.project = job
            proposal.status = 'pending'
            proposal.save()
            messages.success(request, f"Your proposal has been sent successfully. ,, You will get update soon to Email {proposal.email}")
            subject = f"{proposal.name} sent a  Proposal  for {job.title} Techkaj-job"
            date_time_x = timezone.now()
            message = f"{proposal.name} sent a  Proposal  for {job.title} Techkaj-job"
            email_list = email_for_send_message.objects.all()
            recipient_list = []
            for ix in email_list:
                recipient_list.append(ix.email)
               

            send_mail(
            subject,
            message,
            settings.FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            )
            return redirect('dashboard')  # Replace 'success_url' with your desired success page URL

    else:
        form = ProposalForm()

    return render(request, 'job_detail.html', {'job': job, 'proposals': proposals, 'is_applied': is_applied,"form":form})



@login_required(login_url='job_list')
def Update_proposal(request, id):
    proposal = get_object_or_404(Proposal, id=id)

    if request.method == 'POST':
        form = UpdateProposalForm(request.POST, request.FILES, instance=proposal)

        if form.is_valid():
            proposal = form.save()
          
            messages.success(request, f"Your proposal has been Update successfully. ")
          
            return redirect('dashboard')  # Replace 'success_url' with your desired success page URL

    else:
        form = UpdateProposalForm(instance=proposal)


    return render(request, 'update_propsoal.html',{"form":form})




@login_required(login_url='job_list')
def delete_proposal(request, id):
    proposal = get_object_or_404(Proposal, id=id)
    proposal.delete()
    messages.success(request, f"Your proposal has been Deleted  successfully. ")


    return redirect('dashboard')







@login_required(login_url='job_list')
def Send_projects_file_view(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
   
    form = SendProjectsFileForm(request.POST, request.FILES, instance=proposal)
    if form.is_valid():
            send_file_obj = form.save(commit=False)
            send_file_obj.freelancer = request.user
            send_file_obj.project = proposal.project
            send_file_obj.proposal = proposal
            send_file_obj.save()
            return redirect('dashboard')  # Replace 'success_url' with your desired success page URL
    else:
        form = SendProjectsFileForm(instance=proposal)


    return render(request, 'update_file.html',{"form":form})


"""
   model = Send_Projects_file(project=proposal.project,proposal=proposal, freelancer=proposal.freelancer, file=send_file)
        model.save()
        subject = f"{model.freelancer} sent a File for {model.project.title} Techkaj-job"
        date_time_x = timezone.now()

        message =f"{model.freelancer} sent a a FIle for {model.project.title} Techkaj-job in {date_time_x} time"
        email_list = email_for_send_message.objects.all()
        recipient_list = []
        for ix in email_list:
             recipient_list.append(ix.email)
             print(recipient_list)

        send_mail(
            subject,
            message,
            settings.FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            )

        messages.success(request, f"Your File has been sent successfully. ")


"""






@login_required(login_url='job_list')
def hire_freelancer(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        hire = Hire(project=proposal.project, freelancer=proposal.freelancer)
        hire.save()
        proposal.status = 'accepted'
        proposal.save()
        return redirect('job_detail', job_id=proposal.project.id)
    
    return render(request, 'hire_freelancer.html', {'proposal': proposal, })

@login_required(login_url='job_list')
def proposal_rejecte(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        hire = Hire(project=proposal.project, freelancer=proposal.freelancer)
        hire.save()
        proposal.status = 'rejected'
        proposal.save()
        post_save.send(sender=Hire, text="You have been rejected for ", instance=hire, created=True)

        return redirect('job_detail', job_id=proposal.project.id)
    
from django.db.models import Sum

@login_required(login_url='login')
def Dashboard(request):
    profile = request.user
    id = request.user.id
    jobs = Job.objects.filter(owner=id)
  
    proposals = Proposal.objects.filter(freelancer=id)
 
    send_files = Send_Projects_file.objects.filter(Q(freelancer=id) & Q(proposal__in=proposals))

    if request.user.is_authenticated:
        is_send = Send_Projects_file.objects.filter(freelancer=profile).exists()
    else:
        messages.info(request, "Please login to apply for this job.")
        return redirect('job_list')

    earning_money = Earning_money.objects.filter(Q(freelancer=id) | Q(proposal__in=proposals))

    total_money = Earning_money.get_total_money_for_freelancer(freelancer=id)

    payouts = Pay_out_money.objects.filter(Q(freelancer=id) | Q(earning_money__in=earning_money))
    
    earnings_data = Earning_money.objects.filter(freelancer=request.user).values('project__title').annotate(total_earnings=Sum('money'))
    project_names = [data['project__title'] for data in earnings_data]
    earnings = [data['total_earnings'] for data in earnings_data]
    
    for proposal in proposals:
        pass
   
    form = SendProjectsFileForm(request.POST, request.FILES)
    if form.is_valid():
            send_file_obj = form.save(commit=False)
            send_file_obj.freelancer = request.user
            send_file_obj.project = proposal.project
            send_file_obj.proposal = proposal
            send_file_obj.save()
            subject = f"{send_file_obj.freelancer} sent a File for {send_file_obj.project.title} Techkaj-job"
            date_time_x = timezone.now()

            message =f"{send_file_obj.freelancer} sent a a FIle for {send_file_obj.project.title} Techkaj-job in {date_time_x} time"
            email_list = email_for_send_message.objects.all()
            recipient_list = []
            for ix in email_list:
              recipient_list.append(ix.email)
              

              send_mail(
              subject,
              message,
              settings.FROM_EMAIL,
              recipient_list,
              fail_silently=False,
             )

            # messages.success(request, f"Your File has been sent successfully. ")
            return redirect('dashboard')  # Replace 'success_url' with your desired success page URL
    else:
        form = SendProjectsFileForm()




    context = {
        "jobs": jobs,
        "proposals": proposals,
        "profile": profile,
        "send_files": send_files,
        "is_send": is_send,
        "total_money": total_money,
        "payouts": payouts,
   "earning_money":earning_money,
           'project_names': project_names,
        'earnings': earnings,
"form":form,


    }
    return render(request, 'Dashboard.html', context)




# import stripe
# from django.conf import settings
# from django.http import JsonResponse

# stripe.api_key = "sk_test_51IoolWKZy2WF2k2RTBKaqXWJF07FAeNrwHYI8yL5HCQRUhNJOOE7vgosRvFFgJmHKQfwX8Ljks6DbCjBcC1RcEsf00gnWiVjZr"

# def payout(request):
#     try:
#         payout = stripe.Payout.create(
#             amount=10,  # Amount in cents (change this according to your requirement)
#             currency='usd',
#             method='instant',
#             destination=""
#         )

#         return JsonResponse({'success': True, 'message': 'Payout successful.'})
#     except stripe.error.StripeError as e:
#         return JsonResponse({'success': False, 'message': str(e)})


from decimal import Decimal


@login_required(login_url='job_list')
def payout(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    earning_money = Earning_money.objects.filter(proposal=proposal).first()
  
    if request.method == 'POST':
        destination_type = request.POST.get('destination_type')
        if destination_type == 'bkash':
            destination_name =request.POST.get('destination_name')
            destination_phone =request.POST.get('destination_phone')
            destination_address = request.POST.get('destination_address')
            account_number = ''
            account_holder_name = ''
            bank_name = ''
            routing_number = ''
            paypal_name = ''
            paypal_email = ''
        elif destination_type == 'paypal':
            destination_address = ''
            destination_name = ''
            destination_phone = ''
            account_number = ''
            account_holder_name = ''
            bank_name = ''
            routing_number = ''
            paypal_name = request.POST.get('paypal_name')
            paypal_email = request.POST.get('paypal_email')
        
        elif destination_type == 'bank':
            destination_address = ''
            destination_name = ''
            destination_phone = ''
            paypal_name = ''
            paypal_email = ''
            account_number = request.POST.get('account_number')
            account_holder_name = request.POST.get('account_holder_name')
            bank_name = request.POST.get('bank_name')
            routing_number = request.POST.get('routing_number')
        else:
            return redirect('dashboard')  
        if earning_money:
            model = Pay_out_money.objects.create(
                project=proposal.project,
                proposal=proposal,
                freelancer=proposal.freelancer,
                money=earning_money.money,
                destination_address=destination_address,
                earning_money=earning_money,
            account_number=account_number,
            account_holder_name=account_holder_name,
            bank_name=bank_name,
            routing_number=routing_number,
            destination_phone=destination_phone,
            destination_name=destination_name,
            destination_type=destination_type,
            paypal_name =paypal_name,
            paypal_email = paypal_email,
            )
            model.save()

            subject = f"{model.freelancer} sent a Payout request  for {model.project.title} Techkaj-job"
            date_time_x = timezone.now()

            message =f"{model.freelancer} sent a a Payout request  for {model.project.title} Techkaj-job in {date_time_x} time"
            email_list = email_for_send_message.objects.all()
            recipient_list = []
            for ix in email_list:
             recipient_list.append(ix.email)
             print(recipient_list)

            send_mail(
            subject,
            message,
            settings.FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            )

            earning_money.money = Decimal('0.0')
            earning_money.save()
            messages.success(request, f"Your Payout has been sent successfully. ")

            return redirect('dashboard')
    
    return redirect('dashboard')


@login_required(login_url='job_list')
def e_bkash(request, payout_id):
    status = "bkash"

    payout = get_object_or_404(Pay_out_money, id=payout_id)

    if request.method == 'POST':
        form = EditBkashMoneyForm(request.POST, instance=payout)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Bkash has been Updated successfully. ")
            return redirect('dashboard')
    else:
        form = EditBkashMoneyForm(instance=payout)

    return render(request, 'type/e-bkash.html', {'form': form, 'payout': payout})



@login_required(login_url='job_list')
def e_bank(request, payout_id):
    status = "bank"
    payout = get_object_or_404(Pay_out_money, id=payout_id)

    if request.method == 'POST':
        form = EditBankMoneyForm(request.POST, instance=payout)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Bank has been Updated successfully. ")
            return redirect('dashboard')
    else:
        form = EditBankMoneyForm(instance=payout)

    return render(request, 'type/e-bank.html', {'form': form, 'payout': payout})



@login_required(login_url='job_list')
def e_paypal(request, payout_id):
    status = "paypal"
    payout = get_object_or_404(Pay_out_money, id=payout_id)

    if request.method == 'POST':
        form = EditPaypalMoneyForm(request.POST, instance=payout)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your Paypal has been Updated successfully. ")
            return redirect('dashboard')
    else:
        form = EditPaypalMoneyForm(instance=payout)

    return render(request, 'type/e-paypal.html', {'form': form, 'payout': payout,"status":status})





def base_view(request):
    user = request.user

    return render(request, 'base.html')




def about(request):
    body_html_data = About_us.objects.all()
    return render(request, 'about.html',{"body_html_data":body_html_data})


from django.shortcuts import render, redirect
from .forms import ContactUsForm

def contact(request):
    contact_us_model = contact_us.objects.all()
    for ix in contact_us_model:
        pass
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            subject = f"{ix.subject} New Contact for  Techkaj-job"
            date_time_x = timezone.now()

            message =f"{ix.message}   Techkaj-job in {date_time_x} time"
            email_list = email_for_send_message.objects.all()
            recipient_list = []
            for ix in email_list:
              recipient_list.append(ix.email)
              print(recipient_list)

            send_mail(
            subject,
         message,
            settings.FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            )


            messages.success(request, "Your message has been sent successfully.")

            return redirect('contact')

    else:
        form = ContactUsForm()
    
    return render(request, 'contact.html', {'form': form})



def service_view(request):
    body_html_data = service.objects.all()

    return render(request, 'service.html',{"body_html_data":body_html_data})


def home(request):
   
    jobs = Job.objects.all()


    items_per_page = 3
    
    paginator = Paginator(jobs, items_per_page)
    
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        "jobs":jobs
    }
    return render(request, 'home.html',context)





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Use keyword argument for request
            return redirect('dashboard')  # Replace 'home' with the name of your home page URL pattern
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    return render(request, 'login.html', {'error_message': error_message})






def custom_404_error(request, exception):
    return render(request, '404.html', status=404)



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            subject = f"New User {user.username} Registered to Techkaj-job "
            date_time_x = timezone.now()
            message =f"{user.username} Registered to Techkaj-job in {date_time_x}"
            email_list = email_for_send_message.objects.all()
            recipient_list = []
            for ix in email_list:
             recipient_list.append(ix.email)
             print(recipient_list)

            send_mail(
            subject,
            message,
            settings.FROM_EMAIL,
            recipient_list,
            fail_silently=False,
            )

            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

