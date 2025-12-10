from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import reportlab
from django.db.models import Count, Q
from .models import Profile,Complaint
# from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from .forms import UserRegisterForm,ProfileUpdateForm,UserProfileform,ComplaintForm,UserProfileUpdateform,statusupdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from datetime import datetime
from .ai_service import ComplaintAnalyzer

from django.shortcuts import redirect
from django.contrib import messages

import os
from dotenv import load_dotenv
from django.shortcuts import render
import google.generativeai as genai

# Try to load .env file, but don't fail if it doesn't exist
try:
    load_dotenv()
except:
    pass

# Configure Gemini API - use settings if available, otherwise use environment variable
from django.conf import settings
api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv("GEMINI_API_KEY"))
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def chatbot_view(request):
    response_text = ""
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            response = model.generate_content(prompt)
            response_text = response.text
    return render(request, "chat.html", {"response": response_text})

#page loading.
def index(request):
    return render(request,"ComplaintMS/home.html")

def aboutus(request):
    return render(request,"ComplaintMS/aboutus.html")

def login(request):
    return render(request,"ComplaintMS/login.html")

def logout(request):
    # Log out the user
    auth_logout(request)
    # Add a success message
    messages.success(request, 'You have been successfully logged out.')
    # Redirect to the logout page
    return redirect('logout_page')

def logout_page(request):
    return render(request, "ComplaintMS/logout.html")

def signin(request):
    return render(request,"ComplaintMS/signin.html")

from django.http import JsonResponse
import json

def chat(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if prompt:
            try:
                # Simple contact information response based on issue type
                response = get_contact_information(prompt)
            except Exception as e:
                response = "I understand you have an issue. Here's how you can get help:\n\n📧 Email: higherauthority@gmail.com\n📞 Phone: +1-555-123-4567\n🏢 Office: Administration Building, Room 101\n\nPlease contact them directly for immediate assistance."
            
            return JsonResponse({'response': response, 'status': 'success'})
    
    return render(request, "ComplaintMS/chat.html", {'response': None})

def get_contact_information(prompt):
    """Provide contact information based on the type of issue described"""
    prompt_lower = prompt.lower()
    
    # Define contact information for different issue types
    contacts = {
        'classroom': {
            'email': 'classroom.issues@college.edu',
            'phone': '+1-555-100-1001',
            'office': 'Academic Affairs, Room 201',
            'person': 'Academic Coordinator'
        },
        'teacher': {
            'email': 'faculty.affairs@college.edu',
            'phone': '+1-555-100-1002',
            'office': 'Faculty Affairs, Room 301',
            'person': 'Faculty Affairs Director'
        },
        'management': {
            'email': 'management.office@college.edu',
            'phone': '+1-555-100-1003',
            'office': 'Management Office, Room 401',
            'person': 'Management Coordinator'
        },
        'college': {
            'email': 'college.administration@college.edu',
            'phone': '+1-555-100-1004',
            'office': 'Administration Building, Room 501',
            'person': 'College Administrator'
        },
        'general': {
            'email': 'higherauthority@gmail.com',
            'phone': '+1-555-123-4567',
            'office': 'Administration Building, Room 101',
            'person': 'General Affairs Officer'
        }
    }
    
    # Determine the type of issue
    if any(word in prompt_lower for word in ['classroom', 'room', 'facility', 'equipment']):
        contact_type = 'classroom'
    elif any(word in prompt_lower for word in ['teacher', 'professor', 'instructor', 'faculty']):
        contact_type = 'teacher'
    elif any(word in prompt_lower for word in ['management', 'admin', 'administrative']):
        contact_type = 'management'
    elif any(word in prompt_lower for word in ['college', 'university', 'institution']):
        contact_type = 'college'
    else:
        contact_type = 'general'
    
    contact = contacts[contact_type]
    
    response = f"""I understand your issue. Here's the appropriate contact information for your concern:

📧 Email: {contact['email']}
📞 Phone: {contact['phone']}
🏢 Office: {contact['office']}
👤 Contact Person: {contact['person']}

Please reach out to them directly for immediate assistance. They will be able to help you resolve your issue quickly.

For urgent matters, you can also call the general helpline: +1-555-123-4567"""
    
    return response

#get the count of all the submitted complaints,solved,unsolved.
def counter(request):
        total=Complaint.objects.all().count()
        unsolved=Complaint.objects.all().exclude(status='1').count()
        solved=Complaint.objects.all().exclude(Q(status='3') | Q(status='2')).count()
        dataset=Complaint.objects.values('Type_of_complaint').annotate(total=Count('status'),solved=Count('status', filter=Q(status='1')),
                  notsolved=Count('status', filter=Q(status='3')),inprogress=Count('status',filter=Q(status='2'))).order_by('Type_of_complaint')
        args={'total':total,'unsolved':unsolved,'solved':solved,'dataset':dataset,}
        return render(request,"ComplaintMS/counter.html",args)

#changepassword for grievancemember.
def change_password_g(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password_g')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password_g.html', {
        'form': form
    })
    return render(request,"ComplaintMS/change_password_g.html")

#registration page.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form=UserProfileform(request.POST)
        if form.is_valid() and profile_form.is_valid() :
            
            new_user=form.save()
            profile=profile_form.save(commit=False)
            if profile.user_id is None:
                profile.user_id=new_user.id
            profile.save()
            messages.add_message(request,messages.SUCCESS, f' Registered Successfully ')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
        profile_form=UserProfileform()

    context={'form': form,'profile_form':profile_form }
    return render(request,'ComplaintMS/register.html',context)

@login_required(login_url='/signin/')
def login_redirect(request):
    if request.user.profile.type_user == 'student':
        return redirect('dashboard')
    else:
        return redirect('allcomplaints')

@login_required
def dashboard(request):
        
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,instance=request.user)
        profile_update_form=UserProfileUpdateform(request.POST,instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
                user=p_form.save()
                profile=profile_update_form.save(commit=False)
                profile.user=user
                profile.save()
                messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
                return render(request,'ComplaintMS/dashboard.html',)
    else:
        p_form=ProfileUpdateForm(instance=request.user)
        profile_update_form=UserProfileUpdateform(instance=request.user.profile)
    
    # Get complaint statistics for the current user
    user_complaints = Complaint.objects.filter(user=request.user)
    pending_count = user_complaints.filter(status=3).count()
    in_progress_count = user_complaints.filter(status=2).count()
    resolved_count = user_complaints.filter(status=1).count()
    total_count = user_complaints.count()
    
    context={
        'p_form':p_form,
        'profile_update_form':profile_update_form,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'total_count': total_count
        }
    return render(request, 'ComplaintMS/dashboard.html',context)

#change password for user.

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request,messages.SUCCESS, f'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ComplaintMS/change_password.html', {
        'form': form
    })

#complaints handling and submission section.
@login_required
def complaints(request):
  
    if request.method == 'POST':
           
        complaint_form=ComplaintForm(request.POST)
        if complaint_form.is_valid():
            
          
               instance=complaint_form.save(commit=False)
               instance.user=request.user
               
               # AI Analysis for priority assignment
               analyzer = ComplaintAnalyzer()
               analysis_result = analyzer.analyze_complaint(
                   subject=instance.Subject,
                   description=instance.Description,
                   complaint_type=instance.Type_of_complaint
               )
               
               # Set priority and analysis
               instance.priority = analysis_result['priority']
               instance.ai_analysis = analysis_result['analysis']
               
               instance.save()
               
               # Add success message with priority info
               priority_color = analyzer.get_priority_color(analysis_result['priority'])
               priority_icon = analyzer.get_priority_icon(analysis_result['priority'])
               
               messages.add_message(
                   request, 
                   messages.SUCCESS, 
                   f'Your complaint has been registered with {analysis_result["priority"].upper()} priority! AI Analysis: {analysis_result["reasoning"]}'
               )
               
               return render(request,'ComplaintMS/comptotal.html',)
    else:
        
        complaint_form=ComplaintForm(request.POST)
    context={'complaint_form':complaint_form,}
    return render(request,'ComplaintMS/comptotal.html',context)
        

@login_required
def list(request):
    # Get pending complaints (status=3) and in-progress complaints (status=2)
    c = Complaint.objects.filter(user=request.user).filter(Q(status='3') | Q(status='2'))
    # Get resolved complaints (status=1)
    result = Complaint.objects.filter(user=request.user).filter(status='1')
    args = {'c': c, 'result': result}
    return render(request, "ComplaintMS/Complaints.html", args)
@login_required
def slist(request):
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'result':result}
    return render(request,"ComplaintMS/solvedcomplaint.html",args)

@login_required
def download_complaint_pdf(request, complaint_id):
    """Download complaint details as PDF"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="complaint_{complaint_id}.pdf"'
    
    # Create the PDF object using ReportLab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    elements.append(Paragraph("Complaint Details", title_style))
    elements.append(Spacer(1, 20))
    
    # Create data for the table
    data = [
        ['Field', 'Details'],
        ['Subject', complaint.Subject],
        ['Type', complaint.Type_of_complaint],
        ['Status', get_status_display(complaint.status)],
        ['Priority', complaint.priority.upper() if complaint.priority else 'Not Assigned'],
        ['Date', complaint.Time.strftime('%B %d, %Y at %I:%M %p')],
        ['Description', complaint.Description],
    ]
    
    if complaint.ai_analysis:
        data.append(['AI Analysis', complaint.ai_analysis])
    
    # Create table
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.grey
    )
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
    
    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

def get_status_display(status):
    """Convert status code to display text"""
    status_map = {
        '1': 'Resolved',
        '2': 'In Progress',
        '3': 'Pending'
    }
    return status_map.get(str(status), 'Unknown')

@login_required
def allcomplaints(request):
      
        
        c=Complaint.objects.all().exclude(status='1')
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                uid=request.POST.get('uid')
                print(uid)
                project = Complaint.objects.get(id=cid)
                
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        mail = User.objects.filter(id=uid)
                        for i in mail:
                                m=i.email
                       
                      
                        print(m)
                        # send_mail('Hi, Complaint has been Resolved ', 'Thanks for letting us know of your concern, Hope we have solved your issue. Dont Reply to this mail', 'testerpython13@gmail.com', [m],fail_silently=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('allcomplaints'))
                else:
                        return render(request,'ComplaintMS/AllComplaints.html')
                 #testing

        else:
                forms=statusupdate()
        #c=Complaint.objects.all().exclude(status='1')
           
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/allcomplaints.html',args)

@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_complaint__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_complaint__icontains=comp)|Q(Description__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                print(cid)
                project = Complaint.objects.get(id=cid)
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'The complaint has been updated!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'ComplaintMS/solved.html')
                 #testing

        else:
                forms=statusupdate()
        #c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'ComplaintMS/solved.html',args)

#allcomplaints pdf viewer.
def pdf_viewer(request):
    detail_string={}
    #detailname={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Complaint_id.pdf'
    p = canvas.Canvas(response,pagesize=A4)
    
    cid=request.POST.get('cid')
    uid=request.POST.get('uid')
    #print(cid)
    
    details = Complaint.objects.filter(id=cid).values('Description')
    name = Complaint.objects.filter(id=cid).values('user_id')
    '''Branch = Complaint.objects.filter(id=cid).values('Branch')'''
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')
    #date_format1 = "%Y-%m-%d %H:%M:%S.%f%z"
   
    
    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
           detailname=("User: {}".format(val['user_id']))
    '''for val in Branch:
            detailbranch=("Branch: {}".format(val['Branch']))'''
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            ptime=("{}".format(val['Time']))
            detailtime=("Time of Issue/ Time of Solved: {}".format(val['Time']))
    #detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(ptime), date_format)
    delta = a - b
    print(b)
    print(a)
    print (delta.days )       
    if detailtype=='1':
            detailtype="Type of Complaint: ClassRoom"
    if detailtype=='3':
            detailtype="Type of Complaint: Management"
    if detailtype=='2':
            detailtype="Type of Complaint: Teacher"
    if detailtype=='4':
            detailtype="Type of Complaint: School"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    ''' p.drawString(30, 730,detailbranch)'''
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response

#complaints pdf view.
@login_required
def pdf_view(request):
    detail_string={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=complaint_id.pdf'
    
    p = canvas.Canvas(response,pagesize=A4)
    cid=request.POST.get('cid')
    #print(cid)
    details = Complaint.objects.filter(id=cid).values('Description')
    name = User.objects.filter(username=request.user.username).values('username')
    #Branch = Complaint.objects.filter(id=cid).values('Branch')
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_complaint')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')

    for val in details:
            detail_string=("{}".format(val['Description']))
    for val in name:
            detailname=("User: {}".format(val['username']))
    #for val in Branch:
            #detailbranch=("Branch: {}".format(val['Branch']))
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_complaint']))
            
    for val in Issuedate:
            detailtime=("Time of Issue: {}".format(val['Time']))
    #detail_string = u", ".join(("Desc={}".format(val['Description'])) for val in details) 

    if detailtype=='1':
            detailtype="Type of Complaint: ClassRoom"
    if detailtype=='3':
            detailtype="Type of Complaint: Management"
    if detailtype=='2':
            detailtype="Type of Complaint: Teacher"
    if detailtype=='4':
            detailtype="Type of Complaint: School"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    #p.drawString(30, 730,detailbranch)
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Description:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response




             

