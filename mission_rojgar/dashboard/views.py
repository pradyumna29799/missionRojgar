from django.shortcuts import render
from django.template import loader
from django.db import connection
from django.http import HttpResponse

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

import pyttsx3  

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os
import tempfile

engine = pyttsx3.init()  


def index(request):
    template = loader.get_template('index.html')
    
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT count(applicant_att_id) FROM applicant_attendance")
    app_count = cursor.fetchall()
    
    cursor.execute("SELECT count(floor_att_id) FROM floorattendance where floor_no='floor_1' and status='in' ")
    first_floor = cursor.fetchall()
    
    cursor.execute("SELECT count(floor_att_id) FROM floorattendance where floor_no='floor_2' and status='in' ")
    second_floor = cursor.fetchall()
    
    cursor.execute("SELECT count(floor_att_id) FROM floorattendance where floor_no='floor_3' and status='in' ")
    third_floor = cursor.fetchall()
    
    cursor.execute("SELECT count(floor_att_id) FROM floorattendance where floor_no='floor_4' and status='in' ")
    fourth_floor = cursor.fetchall()
    
    cursor.execute("SELECT count(floor_att_id) FROM floorattendance where status='in' ")
    total_in_count = cursor.fetchall()
    
    main_waiting_area = app_count[0][0] - total_in_count[0][0]
    
    context = {'app_count': app_count,
               'main_waiting_area':main_waiting_area,
               'first_floor':first_floor,
               'second_floor':second_floor,
               'third_floor':third_floor,
               'fourth_floor':fourth_floor
               }   # Create an empty dictionary as the context
    return HttpResponse(template.render(context, request))

def candidate(request):
    template = loader.get_template('cards.html')
    cursor = connection.cursor()
   
    cursor.execute("SELECT tad.career_id,tad.fullName,tad.email,tad.mobileNumber,tad.Address from applicant_attendance aa inner join tdtl_applicant_details tad on tad.career_id=aa.job_id ")
    candidate_details = cursor.fetchall()
    
    context = {'candidate_details':candidate_details}  # Create an empty dictionary as the context
    return HttpResponse(template.render(context, request))

def employee(request):
   
    template = loader.get_template('buttons.html')
    
    cursor = connection.cursor()
   
    cursor.execute("SELECT * from final_company_list ")
    employee_list = cursor.fetchall()
    
    context = {'employee_list':employee_list}
      # Create an empty dictionary as the context
    return HttpResponse(template.render(context, request))

def first_floor(request):
    template = loader.get_template('first_floor.html')
    cursor = connection.cursor()
    cursor.execute("SELECT tad.career_id,tad.fullName,tad.email,tad.mobileNumber,tad.Qualification,tad.Region FROM tdtl_applicant_details tad inner join floorattendance fa  on tad.career_id=fa.applicant_id where fa.floor_no='floor_1' and fa.status='in' ")
    first_floor = cursor.fetchall()
    context = {
        'first_floor':first_floor
    }
    return HttpResponse(template.render(context, request))

def second_floor(request):
    template = loader.get_template('second_floor.html')
    cursor = connection.cursor()
    cursor.execute("SELECT tad.career_id,tad.fullName,tad.email,tad.mobileNumber,tad.Qualification,tad.Region FROM tdtl_applicant_details tad inner join floorattendance fa  on tad.career_id=fa.applicant_id where fa.floor_no='floor_2' and fa.status='in' ")
    second_floor = cursor.fetchall()
    context = {
        'second_floor':second_floor
    }
    return HttpResponse(template.render(context, request))

def third_floor(request):
    template = loader.get_template('third_floor.html')
    cursor = connection.cursor()
    cursor.execute("SELECT tad.career_id,tad.fullName,tad.email,tad.mobileNumber,tad.Qualification,tad.Region FROM tdtl_applicant_details tad inner join floorattendance fa  on tad.career_id=fa.applicant_id where fa.floor_no='floor_3' and fa.status='in' ")
    third_floor = cursor.fetchall()
    context = {
        'third_floor':third_floor
    }
    return HttpResponse(template.render(context, request))

def fourth_floor(request):
    template = loader.get_template('fourth_floor.html')
    cursor = connection.cursor()
    cursor.execute("SELECT tad.career_id,tad.fullName,tad.email,tad.mobileNumber,tad.Qualification,tad.Region FROM tdtl_applicant_details tad inner join floorattendance fa  on tad.career_id=fa.applicant_id where fa.floor_no='floor_4' and fa.status='in' ")
    fourth_floor = cursor.fetchall()
    context = {
        'fourth_floor':fourth_floor
    }
    return HttpResponse(template.render(context, request))


def notifyButton(request):
    template = loader.get_template('notifyButton.html')
    
    context = {
        
    }
    return HttpResponse(template.render(context, request))

def screen(request):
    template = loader.get_template('screen.html')
    cursor = connection.cursor()
    cursor.execute("SELECT tad.career_id, tad.fullName, tad.email, tad.mobileNumber FROM applied_applicants aa INNER JOIN tdtl_applicant_details tad ON aa.applicant_id = tad.career_id WHERE aa.notify = 'YES' ORDER BY aa.created_date DESC LIMIT 1")
    notify = cursor.fetchall()

    #text = "harshada kabadi"

   

    context = {
        'notify': notify
    }

    return HttpResponse(template.render(context, request))


def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text)

    # Convert the gTTS audio to an AudioSegment
    audio = AudioSegment.from_file(tts.save("output.mp3"))

    # Play the audio
    play(audio)


def speak_text(text):
    engine = pyttsx3.init()  
    engine.say(text)  
    engine.runAndWait()