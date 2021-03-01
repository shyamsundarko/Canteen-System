import calendar #used to find the day of the week
import datetime #for system date and time
import tkinter as tk
from PIL import ImageTk, Image #for background image
from tkcalendar import Calendar #import Calendar which we use later to get Date input from user
from data import operating_hrs,id_to_store_mapping,full_operating_hrs  ##import dictionaries from data.py

current_hour= None

# The background images and the styling was done by Parthan
#======================================================================================================================================================================================================
# Author:Shyam
# Created:11/14/2019
# Purpose:Return a datetime object
def findDay(date):
    find_day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[find_day])
#======================================================================================================================================================================================================
# Author:Shyam
# Created:11/14/2019
# Purpose:Create a date and time label at the top left of a page
def Date_Time(win1):
    today = datetime.datetime.now()
    d_string = today.strftime("%d")
    justday = int(d_string)
    dt_string = today.strftime("%d/%m/%Y")
    current_time = today.strftime("%H:%M:%S")
    global current_hour
    current_hour = today.strftime("%H")
    label_date1 = tk.Label(win1, text="Date:",borderwidth=2, relief="solid").place(x=0,y=3)
    label_tm1 = tk.Label(win1, text="Time:",borderwidth=2, relief="solid").place(x=80, y=3)
    label_today1 = tk.Label(win1, text=dt_string,borderwidth=2, relief="solid").place(x=0, y=25)
    label_time1 = tk.Label(win1, text=current_time,borderwidth=2, relief="solid").place(x=80, y=25)
    
    return justday

#=======================================================================================================================================================================================================
# Author:Shyam & Kai Kiat
# Created: 11/14/2019
# Purpose: Create a frame with a calendar widget and datetime spinbox to allow user to key in desired datetime 
def showOptionsOtherDays(win1):
    frame=tk.Frame(win1)
    frame.place(relx=0,rely=0,relwidth=1,relheight=1)
    #-------------- Background Image--------------------------
    img = Image.open("./images/background3.png")
    img = img.resize((500,500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(win1, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #---------------------------------------------------------
    to_display_date_and_time = Date_Time(win1)
    label_month = tk.Label(win1, text="SELECT DATE:", width=12, font=("Times", 15, "bold"),borderwidth=2,relief="solid")
    label_month.place(x=150, y=50)
    cal = Calendar(win1,
                   font="Arial 14", selectmode='day',
                   cursor="hand1",
                   year=datetime.datetime.now().year,
                   month=datetime.datetime.now().month,
                   day=datetime.datetime.now().day,
                   mindate=datetime.date(2018, 11, 1),
                   maxdate=datetime.date(2020, 11, 1)
                   )
    cal.place(x=50, y=90)

    def getDate():
        try:
            finalday = " ".join([elem for elem in reversed(str(cal.selection_get()).split('-'))])# convert i.e 2019-11-12 to 12 11 2019
            which_day = findDay(finalday)#convert i.e 12 11 2019 to Tuesday
            if int(spinbox_hr.get()) not in range (1,13) or int(spinbox_min.get()) not in range(0,61):#validate user input for time 
                print('time out of range')
                raise ValueError
            finaltime=convert_to_24hr(
                                      minutes=spinbox_min.get(),
                                      hours=spinbox_hr.get(),
                                      AM_PM=AM_PM_str.get()
                                     )# convert i.e 4.30PM to 16:30
            ## check if any stores are open and then create a window with the list of stores
            ids,no_of_available_stores=[],0  # a list that will contain the ids of stores available in that time frame, no_of_available_stores is to keep track of the available stores
            for id,operating_hours in operating_hrs.items():
                for day_of_the_week,time in operating_hours.items():
                    if day_of_the_week==which_day:
                        start_time = datetime.datetime.strptime(time.split('-')[0], '%H:%M').time()#convert i.e 09:00 to 09:00:00
                        end_time = datetime.datetime.strptime(time.split('-')[1], '%H:%M').time()#convert i.e 09:00 to 09:00:00
                        final_time = datetime.datetime.strptime(finaltime,'%H:%M').time()#convert i.e 09:00 to 09:00:00
                        if final_time>end_time or final_time<start_time:
                            continue
                        else:
                            no_of_available_stores+=1
                            ids.append(id)
            
            if no_of_available_stores==0:#means no stores are available
                raise Exception
            show_list_of_avalble_store(final_time,ids,win1)#if there are available stores we proceed to the nxt frame
        except ValueError as e:
            print(e)
            win_error = tk.Tk()
            win_error.resizable(False, False)
            win_error.geometry('150x150')
            win_error.title('Error Message')
            error_msg = tk.Label(win_error, text="PLEASE KEY IN \nVALID INPUTS", width=16, font=("Times", 12, "bold"),fg="red")
            error_msg.place(x=0, y=25)
            Back_button = tk.Button(win_error,text="BACK", width=10, font=("Times", 15),borderwidth=2, relief="solid" ,command=win_error.destroy)
            Back_button.place(x=15, y=100)
        except Exception as e:
            print(e)
            win_error = tk.Tk()
            win_error.resizable(False, False)
            win_error.title('Error Message')
            win_error.geometry('150x150')
            error_msg = tk.Label(win_error, text="NO STORES ARE \nAVAILABLE", width=16, font=("Times", 12, "bold"),fg="red")
            error_msg.place(x=0, y=25)
            Back_button = tk.Button(win_error,borderwidth=2, relief="solid",text="BACK", width=10, font=("Times", 15), command=win_error.destroy)
            Back_button.place(x=15, y=100)
            

    label_month = tk.Label(win1, text="SELECT TIME:", width=12, font=("Times", 15, "bold"),borderwidth=2,relief="solid")
    label_month.place(x=150, y=340)
    spinbox_hr = tk.Spinbox(win1, from_=1, to=12, width=6)
    spinbox_hr.place(x=120, y=385)
    colon = tk.Label(win1, text=":", width=1, font=("Times", 9, "bold"))
    colon.place(x=176, y=383)
    spinbox_min = tk.Spinbox(win1, from_=00, to=59, width=6)
    spinbox_min.place(x=195, y=385)
    AM_PM_optionlist=['AM','PM']
    AM_PM_str = tk.StringVar(win1)
    AM_PM_str.set(AM_PM_optionlist[0])
    AM_PM_option = tk.OptionMenu(win1, AM_PM_str, *AM_PM_optionlist)
    AM_PM_option.place(x=250,y=377)

    confirm_button = tk.Button(win1, text="ENTER",borderwidth=2, relief="solid",width=20, font=("Times", 15), command=lambda: getDate())
    confirm_button.place(x=100, y=415)

    Back_button = tk.Button(win1, text="BACK",borderwidth=2, relief="solid",width=20, font=("Times", 15), command=lambda:landing_page(win1))
    Back_button.place(x=100, y=460)
#======================================================================================================================================================================================================
# Author:Kai Kiat
# Created:11/14/2019
# Purpose:Shows a list of stores available at a specific datetime
def show_list_of_avalble_store(final_time,ids,win1):
    frame=tk.Frame(win1)
    frame.place(relx=0,rely=0,relwidth=1,relheight=1)
    #-------------- Background Image--------------------------
    img = Image.open("./images/background4.png")
    img = img.resize((500,500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(win1, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #---------------------------------------------------------
    win1.title('NTU Canteen System')
    to_display_date_and_time = Date_Time(win1)
    TitleLabel = tk.Label(win1, text="AVAILABLE STORES", width=20, font=("Times", 20, "bold", "underline"), borderwidth=2, relief="solid")
    TitleLabel.place(x=90, y=50)
    y_increment=120
    for key,values in id_to_store_mapping.items():  #loop id_to_store_mapping menu   
        if key in ids:#since ids is a list that contains the id of store that is operational at final_time, we will print the store_name,store_name is a button which links to the menu of the store
            store_name_button = tk.Button(win1,borderwidth=2, relief="solid", text=values['store_name'], width=20, font=("Times", 15),command=lambda key=key:Today_Chosen(win1,key,ids,final_time))
            store_name_button.place(x=130, y=y_increment)
            y_increment += 50  #y value must increase so that the button can appear like a 'drop-down' list

    Back_button = tk.Button(win1,borderwidth=2, relief="solid", text="BACK", width=20, font=("Times", 15), command=lambda:showOptionsOtherDays(win1))
    Back_button.place(x=130, y=400)
#======================================================================================================================================================================================================
# Author:Kai Kiat
# Created:11/14/2019
# Purpose:Convert time to 24hr format e.g convert i.e 4.30PM to 16:30
def convert_to_24hr(minutes,hours,AM_PM):
    if len(minutes) == 1:#pad minutes with a 0, i.e if user input 1,it will become 01 
        minutes = "0" + minutes
    if len(hours) == 1:#pad hours with a 0,so if user enters 2,it will become 02
        hours = "0" + hours
    time=hours+':'+minutes+AM_PM#so the end result is transforming 1:1 to 01:01AM or 01:01PM depending on which option is chosen
    # the if elif statement converts i.e 01.01AM to 01:10 or converts 01.01PM to 13:01
    if time[:2]=='12' and time[-2:]=='AM':
        return '00'+':'+minutes
    elif time[:2]=='12' and time[-2:]=='PM':
        return time[:-2]
    elif time[-2:]=='PM':
        return str(int(hours)+12)+':'+minutes
    elif time[-2:]=='AM':
        return time[:-2]
#======================================================================================================================================================================================================
# Author:Shyam
# Created:11/14/2019
# Purpose:Caculate the waiting time as well as creating a label to show the waiting time
def calculate(win1):
    pplNum=tk.StringVar()
    timeTaken=tk.StringVar()
    label_pax = tk.Label(win1, text="Enter the number of pax queuing:", width=25, font=("Times", 11),borderwidth=2, relief="solid")
    label_pax.place(x=90, y=260)
    entry_1 = tk.Entry(win1, textvariable=pplNum, width=10)
    entry_1.place(x=300, y=262)
    label_calc1 = tk.Label(win1, text="The approximate waiting time in minutes:", width=30, font=("Times", 11),borderwidth=2, relief="solid")
    label_calc1.place(x=65, y=300)

    def show_answer():
        try: #multiply user input by 3 and returning it as a label text
            num = int(entry_1.get())
            if num <0:
                raise Exception
            timeTaken.set(num * 3)
            print(timeTaken.get())
            label_calc2["text"] = timeTaken.get()
        except: #if there is a error, say the user input a string,an error window will pop up
            win_error = tk.Tk()
            win_error.resizable(False, False)
            win_error.geometry('150x150')
            win_error.title('Error Message')
            error_msg = tk.Label(win_error, text="INVALID \n INPUT", width=10, font=("Times", 15, "bold"),borderwidth=2,
                                 fg="red")
            error_msg.place(x=12, y=30)
            Back_button = tk.Button(win_error,borderwidth=2, relief="solid",text="BACK", width=10, font=("Times", 15), command=win_error.destroy)
            Back_button.place(x=15, y=100)
    button_calc = tk.Button(win1,borderwidth=2, relief="solid",text="Calculate", width=12, font=("Times", 10, "bold"), command=show_answer)
    button_calc.place(x=195, y=350)
    label_calc2 = tk.Label(win1,width=9, font=("Times", 10, "bold"))  # will print calculated answer
    label_calc2.place(x=320, y=301)
#======================================================================================================================================================================================================
# Author:Shyam and Kai Kiat
# Created:11/14/2019
# Purpose:Create the menu of the store

#id=id of the store 
#ids=list of store with ids for stores operating in a particular time
#time=refers to the time
def Today_Chosen(win1,id,ids,time):   
    frame=tk.Frame(win1)
    frame.place(relx=0,rely=0,relwidth=1,relheight=1)
    #-------------- Background Image--------------------------
    img = Image.open("./images/background1.png")
    img = img.resize((500,500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(win1, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    if(id==1):
        myfile = open('Menu/MCD_MonThuSatSun.txt', 'r')
        label_1 = tk.Label(win1, text="MCDONALDS", width=13, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=130, y=53)
    elif(id==2):
        myfile = open('Menu/KFC_MonThuSatSun.txt', 'r')
        label_1 = tk.Label(win1, text="KFC", width=10, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=160, y=53)
    elif(id==3):
        myfile = open('Menu/PH_MonThuSatSun.txt', 'r')
        label_1 = tk.Label(win1, text="PIZZAHUT", width=20, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=90, y=53)
    elif(id==4):
        myfile = open('Menu/MCD_TueWedFri.txt', 'r')
        label_1 = tk.Label(win1, text="MCDONALDS", width=13, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=130, y=53)
    elif(id==5):
        myfile = open('Menu/KFC_TueWedFri.txt', 'r')
        label_1 = tk.Label(win1, text="KFC", width=10, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=160, y=53)
    elif(id==6):
        myfile = open('Menu/LJS_TueWedFri.txt', 'r')
        label_1 = tk.Label(win1, text="LONG JOHN'S SILVER", width=20, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=90, y=53)
    elif(id==7):
        myfile = open('Menu/PH_TueWedFri.txt', 'r')
        label_1 = tk.Label(win1, text="PIZZA HUT", width=15, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=140, y=53)
    elif(id==8):
        myfile = open('Menu/LJS_MonThuSatSun.txt', 'r')
        label_1 = tk.Label(win1, text="LONG JOHN'S SILVER", width=20, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=90, y=53)
    elif(id==9):
        myfile = open('Menu/Starbucks_MonThuSatSun.txt', 'r')
        label_1 = tk.Label(win1, text="STARBUCKS", width=20, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=90, y=53)
    elif(id==10):
        myfile = open('Menu/Starbucks_TueWedFri.txt', 'r')
        label_1 = tk.Label(win1, text="STARBUCKS", width=20, font=("Times", 20, "bold","underline"),borderwidth=2,relief="solid")
        label_1.place(x=90, y=53)
        
    if int(str(time)[:2])<12:#morning menu 
        breakfast_section,line_number=0,1
        line_str=''
        for line in myfile:
            line=line.rstrip('\n')
            if line=='':
                line_str,line_number='',1
            else:#only print the menu items after the line break
                line_str+=str(line_number)+') '+line+'\n'
                line_number+=1
                
    else: #afternoon menu
        line_str=''
        line_number=1
        for line in myfile:
            line=line.rstrip('\n')
            if line=='':#stops printing the menu when there is a line break
                break
            else:
                line_str+=str(line_number)+') '+line+'\n'
                line_number+=1
                
    label_2 = tk.Label(win1, text=line_str, width=40, font=("Times", 14, "bold"),borderwidth=2, relief="solid")
    label_2.place(x=25, y=100)
    
    def previous_page(win1,ids,time):
       if(ids==None):
        showOptionsToday(win1)
       else:
        if (time):
         show_list_of_avalble_store(time,ids,win1)

    show_operating_hrs(id,win1)
    calculate(win1)
    Back_button = tk.Button(win1,borderwidth=2, relief="solid", text="BACK", width=20, font=("Times", 15), command=lambda:previous_page(win1,ids,time))
    Back_button.place(x=120, y=400)

#======================================================================================================================================================================================================
# Author:Kai Kiat
# Created:11/14/2019
# Purpose:Create the operating hours window
def show_operating_hrs(id,win1):
    def operating_hrs_window():
        op_hr_win = tk.Tk()
        op_hr_win.geometry('350x350')
        op_hr_win.title("Operating Hours Window")
        Exit_button = tk.Button(op_hr_win, text="BACK", width=20, font=("Times", 15),borderwidth=2,relief="solid", command=op_hr_win.destroy)
        Exit_button.place(x=50, y=250)
        y_increment = 20

        for key, value in full_operating_hrs[id].items():
            operating_day = tk.Label(op_hr_win, text=key + ' : ' + value, width=20, font=("Times", 13, "bold"))
            operating_day.place(x=55, y=y_increment)
            y_increment += 25

    operating_hrs_btn = tk.Button(win1, text="Operating Hours", width=15, font=("Times", 10, "bold"), command=operating_hrs_window)
    operating_hrs_btn.place(x=0, y=2)
#======================================================================================================================================================================================================
# Author:Shyam
# Created:11/14/2019
# Purpose:Creates the page that shows the restaurants available for the day
def showOptionsToday(win1):
    frame=tk.Frame(win1)
    frame.place(relx=0,rely=0,relwidth=1,relheight=1)
    win1.title("NTU Canteen System")
    to_display_date_and_time = Date_Time(win1)
     #-------------- Background Image--------------------------
    img = Image.open("./images/background2.png")
    img = img.resize((500,500), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(win1, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #---------------------------------------------------------
    to_display_date_and_time = Date_Time(win1)
    List_someDays1 = ["Monday", "Thursday", "Saturday", "Sunday"]
    List_someDays2 = ["Tuesday", "Wednesday", "Friday"]
    now = datetime.datetime.now()
    str_day = now.strftime("%A")# get today's day i.e Tuesday
    TitleLabel= tk.Label(win1,text="AVAILABLE STORES",width=20,font=("Times",20,"bold","underline"), borderwidth=2, relief="solid")
    TitleLabel.place(x=90,y=50)
    if (str_day in List_someDays1):  #create these buttons if str_days in List_someDays1

        button1 = tk.Button(win1, text="MCDONALDS", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,1,None,current_hour))
        button1.place(x=150, y=100)
        button2 = tk.Button(win1, text="KFC", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,2,None,current_hour))
        button2.place(x=150, y=150)
        button3 = tk.Button(win1, text="PIZZA HUT", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,3,None,current_hour))
        button3.place(x=150, y=200)
        button8 = tk.Button(win1, text="LONG JOHN'S", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,8,None,current_hour))
        button8.place(x=150, y=250)
        button10 = tk.Button(win1, text="STARBUCKS", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,9,None,current_hour))
        button10.place(x=150, y=300)

    elif (str_day in List_someDays2): #create these buttons if str_days in List_someDays2

        button4 = tk.Button(win1, text="MCDONALDS", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,4,None,current_hour))
        button4.place(x=150, y=100)
        button5 = tk.Button(win1, text="KFC", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,5,None,current_hour))
        button5.place(x=150, y=150)
        button6 = tk.Button(win1, text="LONG JOHN'S", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,6,None,current_hour))
        button6.place(x=150, y=200)
        button7 = tk.Button(win1, text="PIZZA HUT", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,7,None,current_hour))
        button7.place(x=150, y=250)
        button9 = tk.Button(win1, text="STARBUCKS", width=15, font=("Times", 15),borderwidth=2, relief="solid", command=lambda:Today_Chosen(win1,10,None,current_hour))
        button9.place(x=150, y=300)

    Back_button = tk.Button(win1,borderwidth=2, relief="solid", text="BACK", width=15, font=("Times", 15), command=lambda:landing_page(win1))
    Back_button.place(x=150, y=400)
#=====================================================================================================================================================================================================
# Author:Shyam
# Created:11/14/2019
# Purpose:Shows the first page of the program
def landing_page(win1):
    #-------------- Background Image--------------------------
    img = Image.open("./images/background.png")
    img = img.resize((550,550), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(win1, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #---------------------------------------------------------
    win1.title("NTU Canteen System")
    to_display_date_and_time = Date_Time(win1)

    label_1 = tk.Label(win1, text="WELCOME TO NTU CANTEEN SYSTEM", width=34, font=("Times", 19,"bold italic"),borderwidth=2, relief="solid")
    label_1.place(x=10, y=80)
    Exit_button = tk.Button(win1,borderwidth=2, relief="solid", text="EXIT", width=20, font=("Times", 15),command=win1.destroy)
    Exit_button.place(x=120, y=400)
    Opt1_button = tk.Button(win1,borderwidth=2, relief="solid", text="Show Today's Options", width=20, font=("Times", 15),command=lambda:showOptionsToday(win1))
    Opt1_button.place(x=120, y=200)
    Opt2_button = tk.Button(win1,borderwidth=2, relief="solid", text="Show Options by Date", width=20, font=("Times",15),command=lambda:showOptionsOtherDays(win1))
    Opt2_button.place(x=120,y=250)
#===================================================================================================================================================================================================== 
# Author:Kai Kiat
# Created:11/14/2019
# Purpose:Starts the app as well create an unresizable window
def main():
    win1=tk.Tk()
    win1.resizable(False, False)
    canvas=tk.Canvas(win1,height=500,width=500)
    canvas.pack()
    landing_page(win1)
    win1.mainloop()
    
if __name__=="__main__":
    main()
    