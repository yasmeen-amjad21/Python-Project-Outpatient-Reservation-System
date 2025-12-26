import sys
import os
import shutil
from datetime import datetime
#patient menue
def patient_menu():
    print("Patient services:")
    print("\nChoose a service:")
    print("\n1. Register as new patient:")
    print("\n2. View appointment history:")
    print("\n3. Cancel appointment:")
    print("\n4. Book appointment:")

    ans =int(input("\nSelect a number: "))

    match ans:
        case 1:
            patient_register()
        case 2:
            appointment_view()
        case 3:
            cancel_appointment()
        case 4:
            book_appointment()
        case _:
            print("\nInvalid option. Please select 1-3.")

#main menu and log in system 
def log_in():
    ans = input("Select your role (patient or admin) .or Enter exit : ").strip().lower()

    if ans =="patient":
        patient_menu()
    elif ans== "admin":
        admin_menu()
    elif ans== "exit":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid option, please enter 'patient', 'admin', or 'exit'.")
#generate id for patient based in the id in th e patient.txt file
def generating_id(filename,first_ch):
    #filename= "project_2.py/patient.txt"
    dirpath = os.path.dirname(filename)
    if dirpath:

      os.makedirs(os.path.dirname(filename), exist_ok=True)

    max_id= 0
    if os.path.exists(filename):
        with open(filename, "r") as f: 
            for line in f:
                first_part = line.strip().split("|")[0]
                if first_part.startswith(first_ch) and first_part[1:].isdigit():
                    num = int(first_part[1:])
                    if num > max_id:
                        max_id = num

    new_id = f"{first_ch}{max_id+1:03d}"
    print("Generated new ID: " + new_id)
    return new_id

def patient_register():
    name =input("\nEnter your name: ")
    if not name.isalpha():
        print("\nInvalid name. You should enter characters only.")
        return

    print("\nValid name is saved.")

    phone= input("\nEnter your phone number: ")
    if not phone.isdigit():
        print("\nInvalid phone number. Please enter digits only.")
        return
    #check if file exists, if not create one
    if not os.path.exists("patient.txt"):   
     print("Error: patient.txt file is missing!")
     with open("patient.txt", "w") as f:
      pass
     
    print("\nValid phone number.")
    pid = generating_id("patient.txt","P")

    filename ="patient.txt"
    with open(filename, "a") as f: 
     f.write ( pid + "|" + name +"|" + phone + "\n")

    with open("system.log", "a") as x:
     timestamp = str(datetime.now())
     x.write(f"{timestamp} | patient registration | ID={pid}, Name={name}, Phone={phone}\n")
    print("\n registered successfully")

def appointment_view():
    
    if not os.path.exists("patient.txt"):   
       print("Error: patient.txt file is missing!")
       with open("patient.txt", "w") as f:
        pass
       
    f = open("patient.txt", "r")
    patients_lines = f.readlines()
    f.close()

    while True:
        patient_id = input("enter your id: ").strip() #strip to remove any extar spaces or \n
        found = False
        for line in patients_lines:
            parts = line.strip().split("|")
            if parts[0] == patient_id:
                found = True
                break

        if not found:
            print("you entered invalid id")
            continue 
        if not os.path.exists("appointments.txt"):   
         print("Error: file is missing!")
         with open("appointments.txt", "w") as f:
          pass
        f =open("appointments.txt", "r")
        appointments_lines = f.readlines() #saving lines
        f.close()

        booked= []
        for line in appointments_lines:
            parts= line.strip().split("|")
            if len(parts) > 1 and parts[1] == patient_id: #use len(parts) to avoid error if the line was empty
                booked.append(line.strip())

        if len(booked) == 0:
            print("You haven't booked any appointments")
            break 

        for appt in booked:
            print(appt)
        break  

def time_validation(time):
    try:
        return datetime.strptime(time.strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        return None
    
def cancel_appointment():
    if not os.path.exists("appointments.txt"):   
       print("Error: file is missing!")
       with open("appointments.txt", "w") as f:
        pass
    appointment_view()
    f=open("appointments.txt","r")
    appointments_lines= f.readlines()
    f.close()
    while True:
        pat_id=input("renter your  id: ").strip()
        appoin_id = input("enter appointment id: ").strip() #strip to remove any extar spaces or \n
        found = False
        for line in range(len(appointments_lines)):
            parts = appointments_lines[line].strip().split("|")

            if parts[0] == appoin_id and parts[1]==pat_id:
                found = True
                if parts[5]== "cancelled":
                 print("this appointment is already cancelled")
                
                else:
                    parts[5]= "cancelled"
                    appointments_lines[line] = "|".join(parts) + "\n"  
                    with open("appointments.txt","w") as f:
                     f.writelines(appointments_lines)
                    print("your appointment was cancelled")
                break

        if not found:
            print("you entered invalid id")
            continue 
    
        break

from datetime import datetime  # needed for date and time validation

def book_appointment():
    #Load all patient IDs from the file
    try:
        with open("patient.txt", "r") as f:
            patients = [line.strip().split("|")[0] for line in f.readlines()]
    except FileNotFoundError:
        print("file is not found")
        return

    while True:
        #ask the user to enter their id
        id = input("enter your id: ").strip()
        # If the user entered nothing
        if not id:
            ans = input("No such id. Enter 1) to register\n 2) to re-enter id: ")
            match ans:
                case "1":
                    patient_register()  # call registration function
                case "2":
                    continue  # restart loop to enter ID again
                case _:
                    print("invalid option")
                    return

        # check if id exists in patients
        if id not in patients:
            print("patient id not found, you should register first")
            return

        # load doctors from file
        try:
            with open("doctors.txt", "r") as f:
                doc_lines = f.readlines()
        except FileNotFoundError:
            print("file is not found!")
            return

        while True:
            # ask user for doctor's speciality
            spec = input("enter the doctor's speciality: ").strip()
            found = False  # flag to check if any doctor matches
            chosen = None  # will store the selected doctor's info

            # search all doctors
            for line in doc_lines:
                parts = line.strip().split("|")
                if parts[2].lower() == spec.lower():
                    found = True
                    chosen = parts
                    # display doctor info
                    print("Doctor id: %s, Doctor name %s , doctor's working days: %s, working hours: start time: %s - end time:%s" % (parts[0], parts[1], parts[3], parts[4], parts[5]))

            if not found:
                print("you entered invalid speciality")
                continue  # ask speciality again

            # ask user to enter doc id
            doc_id = input("\nenter doctor id you want to book an appointment with: ")
            flag = False
            for line in doc_lines:
                parts = line.strip().split("|")
                if parts[0] == doc_id and parts[2].lower()==spec.lower():
                    flag = True
                    chosen = parts  # store selected doctor
                    break
            if not flag:
                print("invalid doctor id!")
                continue  # ask again

            # ask for appointment date and time
            print("doctor available time: %s-%s and available days: %s" % (chosen[4],chosen[5], chosen[3]))
            timee = input("choose time (e.g. 09:00): ")
            datee = input("choose date (use yyyy-mm-dd format): ")

            # validate time format
            if ":" not in timee:
                print("invalid time format, use HH:MM")
                return
            hour, minute = timee.split(":", 1)
            if not (hour.isdigit() and minute.isdigit()):
                print("invalid time, must be numbers")
                return
            if not (len(hour) in [1, 2] and "00" <= hour.zfill(2) <= "23"):
                print("invalid hour")
                return
            if not (len(minute) == 2 and "00" <= minute <= "59"):
                print("invalid minutes")
                return

            # validate date format
            try:
                datetime.strptime(datee, "%Y-%m-%d")
            except ValueError:
                print("invalid date format or date doesn't exist")
                return
            #check dr working days
            days_field = (chosen[3] if len(chosen) > 3 else "").replace(" ", "")  # remove spaces
            day_abbv = datetime.strptime(datee, "%Y-%m-%d").strftime("%a")  # e.g., Mon, Tue
            available_days = days_field.split(",")  # list of working days
            if day_abbv not in available_days:
                print(f"doctor is not available on {day_abbv}, available: {chosen[3]}")
                return

            # check dr working hiours
            start_time = chosen[4] if len(chosen) > 4 else ""
            end_time = chosen[5] if len(chosen) > 5 else ""
            if start_time and end_time:
                if not (start_time <= timee < end_time):
                    print(f"Time {timee} unavailable, working hours: ({start_time}-{end_time})")
                    return

            #check for double booking
            try:
                with open("appointments.txt", "r") as f:
                    appointments_lines = f.readlines()
            except FileNotFoundError:
                print("file is missing!")
                appointments_lines = []  # no appointments yet

            booking = False
            for line in appointments_lines:
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                appt_id, pat_id, doc_id2, date2, time2, status = parts

                # check if patient already has an appointment at that time
                if pat_id == id and date2 == datee and time2 == timee and status != "cancelled":
                    print("you already have an appointment at this time")
                    booking = True
                    break

                # check if doc already has an appointment at that time
                if doc_id2 == doc_id and date2 == datee and time2 == timee and status != "cancelled":
                    print("the doctor already has an appointment at this time")
                    booking = True
                    break

            if booking:
                return
            # generate a new AppointmentID and save app in appointments.txt
            new_id = f"A{len(appointments_lines)+1:03d}"
            new_appointment = f"{new_id}|{id}|{doc_id}|{datee}|{timee}|confirmed\n"
            with open("appointments.txt", "a") as f:
                f.write(new_appointment)
            print(f"Appointment booked successfully with ID: {new_id}")
            return

      
####################################################################
#admin services 
def admin_menu():
  while True:
    print("Admin sevices:\n")
    print("1. Add a new doctor.\n")
    print("2. View doctor's schedual.\n")
    print("3. Backup the system data.\n")
    print("4.exit\n")
    option= int(input("please choose a service(1-3):"))

    match option:
        case 1:
            Add_doctor()
        case 2:
            doctor_schedule()
        case 3:
            backup_data()
        case 4:
          print("exiting...")
          break
        case _:
            print("\nInvalid option. Please select 1-3.")


# case 1 : add a new doctor:
def Add_doctor():
    while True:
     name =input("\nenter your name: ")

     if not name.isalpha():
        print("\ninvalid name! enter characters only")
        
     else:
      print("\nvalid name is saved")
      break

    while True:
     spec=input("\nenter doctor's speciality:")
     if not spec.isalpha():
         print("invalid speciality! enter characters only")
     else:
      print("\nspeciality is valid.")
      break
    valid_days = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}
    while True:
     days= input("\nenter available days (e.g., Sun,Mon,Wed): ")
     tokens = [day.strip() for day in days.split(",")]
     if not tokens:
         print ("enter at least one day")
         continue
     is_valid = True  

     for day in tokens:
      if not day.isalpha() or day not in valid_days:
        is_valid = False
        break  

     if is_valid:
      print("accepted:", ",".join(tokens))
      break
     else:
       print("invalid days!")


#check for valid hours:
    while True:
     start_time=input ("\nenter working hours(eg:start time : HH:MM)")
     end_time=input("\nenter end time:")

#checks for time validaton
     time_validation(start_time)
     time_validation(end_time)
     if not (time_validation(start_time) and time_validation(end_time)):
      print("invalid time!")
      continue
     break

#generate an id for the new doctor
    doc_id=generating_id("doctors.txt","D")

    filename ="doctors.txt"
    with open(filename, "a") as f: 
      f.write ( doc_id + "|" + name +"|" + spec + "|" + days+ "|" + start_time + "|" + end_time + "\n")
      print("doctor is added")

    from datetime import datetime
    with open("system.log", "a") as x:
     timestamp = str(datetime.now())
     x.write(f"{timestamp} | Adding doctor | ID={doc_id}, Name={name}, speciality={spec}\n")
    print("\n registered successfully")

#case 2: view doctor's schedule

def doctor_schedule():
     f=open("doctors.txt","r")
     lines=f.readlines()

    
     doc_id=input("\nEnter doctor's id :").strip()
     found=False
     for line in lines:
        parts=line.strip().split("|")
        if(parts[0]==doc_id):
           found=True
           break
     if not found:
           print("\nthis id is not exist.")
           return

     f2=open("appointments.txt","r")
     app_lines=f2.readlines()
     flag=False
     print("\nAppointments for %s :"%doc_id)
     for l in app_lines:
        sec=l.strip().split("|")
        if(sec[2]==doc_id):
           flag=True
           
           
           
           f3=open("patient.txt","r")
           pat_line=f3.readlines()
           for l2 in pat_line:
              elem=l2.strip().split("|")
              if(elem[0]==sec[1]):
                 print("\nPatient name :%s\t day:%s\t time: %s\t status :%s"%(elem[1],sec[3],sec[4],sec[5]))
                
           
     if not flag:
           print("no appoiontments.")
                 



def backup_data():
    if not os.path.exists("backups"):
        os.makedirs("backups")

   
    files = ["patient.txt", "doctors.txt", "appointments.txt", "system.log"]

    for file in files:
        if os.path.exists(file):
            shutil.copy(file, "backups")
            print(f"{file} copied successfully ")
        else:
            print(f"{file} not found ")

    print("Backup completed")

log_in()