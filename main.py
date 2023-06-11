import tkinter
import customtkinter
from todo import Todo
from database import insert_todo, get_all_todos, complete_task, reopen_task, delete_todo, edit_task, edit_price, edit_note


class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()

        self.title('Tasks - v1.0.0')
        self.geometry('960x600')  
        
        self.scrollable_frm()
        self.objects_frm()
        self.tasks_frm()
        self.light_switch()


    def scrollable_frm(self):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill='both', expand=True, padx=0, pady=0)


    def objects_frm(self):
        self.objects_frame = customtkinter.CTkFrame(self.scrollable_frame)
        self.objects_frame.grid(row=0, column=0, padx=(10,0), pady=(10), sticky='nsw')
        self.objects_label_frm()
        self.object_insert_frm()
        self.objects_buttons_frm()


    def objects_label_frm(self):
        objects_label_frame = customtkinter.CTkFrame(self.objects_frame)
        objects_label_frame.grid(row=0, column=0, padx=10, pady=(10), sticky='ew')
        self.objects_label = customtkinter.CTkLabel(objects_label_frame, text='Groups')
        self.objects_label.grid(row=0, column=0, padx=10, pady=(10), sticky='we')
        self.objects_label.configure(width=150)


    def object_insert_frm(self):
        self.objects_insert_frame = customtkinter.CTkFrame(self.objects_frame)
        self.objects_insert_frame.grid(row=1, column=0, padx=10, pady=(10), sticky='ew')
        self.insert_btn()


    def insert_btn(self):
        insert_button = customtkinter.CTkButton(self.objects_insert_frame, text='Insert New Object', command=lambda :self.insert_new_object())
        insert_button.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        insert_button.configure(fg_color='green', width=150)


    def objects_buttons_frm(self):
        self.objects_buttons_frame = customtkinter.CTkFrame(self.objects_frame)
        self.objects_buttons_frame.grid(row=2, column=0, padx=10, pady=(10), sticky='ew')
        self.objects_list()


    def objects_list(self, object=None):
        self.results = get_all_todos()
        results_list = []

        for i, result in enumerate(self.results):
            if result.object not in results_list:                    
                button = customtkinter.CTkButton(self.objects_buttons_frame, text=result.object)
                button.grid(row=i, column=0, padx=10, pady=10, sticky='we')
                button.configure(width=150, command=lambda btn=button, var=result.object: self.tasks_list(var, btn))
                results_list.append(result.object)


    def tasks_frm(self):
        self.tasks_frame = customtkinter.CTkFrame(self.scrollable_frame)
        self.tasks_frame.grid(row=0, column=1, padx=(5,10), pady=(10, 0), sticky='nw')
        self.tasks_titles_frm()


    def tasks_titles_frm(self):
        tasks_titles_frame = customtkinter.CTkFrame(self.tasks_frame)
        tasks_titles_frame.grid(row=0, column=0, padx=(10), pady=(10), sticky='nw')
        tasks_task_label = customtkinter.CTkLabel(tasks_titles_frame, text='Task')
        tasks_task_label.grid(row=0, column=0, padx=10, pady=(10), sticky='we')
        tasks_task_label.configure(width=150)
        tasks_price_label = customtkinter.CTkLabel(tasks_titles_frame, text='$$$')
        tasks_price_label.grid(row=0, column=1, padx=10, pady=(10), sticky='we')
        tasks_price_label.configure(width=150)
        tasks_status_label = customtkinter.CTkLabel(tasks_titles_frame, text='Status')
        tasks_status_label.grid(row=0, column=2, padx=10, pady=(10), sticky='e')
        tasks_status_label.configure(width=150)


    def tasks_list(self, object, button=None):
        try:
            self.row_frame.destroy()
        except Exception:
            pass
        self.row_frm()
        self.insert_row(object)
        self.__reset_btn_color(self.objects_buttons_frame, object)
        if button:
            button.configure(border_color='#00FFFF', text_color='#00FFFF', border_width=2, hover=False)

        total_price_text = 0.0
        for i, self.result in enumerate(self.results):
            if self.result.object == object:
                if self.result.price is not None:
                    total_price_text +=self.result.price
                self.row(i+1)

        self.total_price_frm(total_price=total_price_text)


    def insert_row(self, object):
        validation_command = self.register(self.__entry_limit)

        taskentry = customtkinter.StringVar()
        self.taskinsert = customtkinter.CTkEntry(self.row_frame, textvariable=taskentry)
        self.taskinsert.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.taskinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'task'))

        pricentry = customtkinter.StringVar()
        self.priceinsert = customtkinter.CTkEntry(self.row_frame, textvariable=pricentry)
        self.priceinsert.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        self.priceinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'price'))

        buttoninsert = customtkinter.CTkButton(self.row_frame, text='Insert', command=lambda :self.insert(object=object, task=self.taskinsert.get(), price=self.priceinsert.get()))
        buttoninsert.grid(row=0, column=2, padx=10, pady=10, sticky='e')


    def row_frm(self):
        self.row_frame = customtkinter.CTkFrame(self.tasks_frame)
        self.row_frame.grid(row=1, column=0, padx=10, pady=10, sticky='new')


    def row(self, i):
        task_label = customtkinter.CTkLabel(self.row_frame)
        task_label.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
        task_label.configure(text=self.result.task, width=150)
        price_label = customtkinter.CTkLabel(self.row_frame)
        price_label.grid(row=i+1, column=1, padx=10, pady=10, sticky='we')
        price_label.configure(text=self.result.price if self.result.price != 0.0 else '', width=150)
        
        status_check = customtkinter.CTkCheckBox(self.row_frame,text='', command=lambda value=self.result: self.checkbox(value))
        status_check.grid(row=i+1, column=2, padx=(10,0), pady=10, sticky='we')
        status_check.configure(text='')
        status_check.grid_columnconfigure(0, weight=1)
        if self.result.note:
            color = '#00FFFF'
            n = 2
        else:
            color = None
            n = None
        note_button = customtkinter.CTkButton(self.row_frame,text='Note', border_width=n, text_color=color, border_color=color, command=lambda value=self.result.id, note=self.result.note, object=self.result.object: self.note(value, note, object))
        note_button.grid(row=i+1, column=3, padx=(10,5), pady=10, sticky='w')
        note_button.configure(width=50)
        edit_button = customtkinter.CTkButton(self.row_frame,text='Edit', command=lambda value=self.result.id, task=self.result.task, price=self.result.price, object=self.result.object: self.edit(value, task, price, object))
        edit_button.grid(row=i+1, column=4, padx=5, pady=10, sticky='w')
        edit_button.configure(width=50)
        delete_button = customtkinter.CTkButton(self.row_frame,text='Delete', command=lambda value=self.result.id, object=self.result.object: self.delete(value, object))
        delete_button.grid(row=i+1, column=5, padx=(5,10), pady=10, sticky='we')
        delete_button.configure(fg_color='red', width=50)

        if self.result.status == 1:
            status_check.select()
        else:
            status_check.deselect()


    def total_price_frm(self, total_price):
        if total_price > 0.0:
            if  hasattr(app, 'total_price_frame'):
                self.total_price_text_label.configure(text=total_price)
            else:
                self.total_price_frame = customtkinter.CTkFrame(self.tasks_frame)
                self.total_price_frame.grid(row=2, column=0, padx=(180,0), pady=10, sticky='wn')
                self.total_price_label = customtkinter.CTkLabel(self.total_price_frame, width=150, text='Total Price')
                self.total_price_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')
                self.total_price_text_label = customtkinter.CTkLabel(self.total_price_frame, width=150, text=total_price)
                self.total_price_text_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')
        else:
            try:
                self.total_price_frame.destroy()
                delattr(app, 'total_price_frame')
            except Exception:
                pass


    def light_switch(self):
        
        self.switchvar = customtkinter.StringVar(value='off')
        self.switch = customtkinter.CTkSwitch(self.scrollable_frame, command=self.switch_event, text='Light Mode', onvalue='on', offvalue='off', variable=self.switchvar)
        self.switch.grid(row=0, column=1, padx=(600), pady=30, sticky='nw')


    def switch_event(self):
        if self.switchvar.get() == 'on':
            customtkinter.set_appearance_mode('light')
        elif self.switchvar.get() == 'off':
            customtkinter.set_appearance_mode('dark')
        if self.switchvar.get() == 'off':
            text_mode = 'Light'
        elif self.switchvar.get() == 'on':
            text_mode = 'Dark'
        self.switch.configure(text=f'{text_mode} Mode')


    def checkbox(self, result):
        if result.status == 0:
            complete_task(result.id)
        elif result.status == 1:
            reopen_task(result.id)
        self.results = get_all_todos()


    def insert(self, object, task, price):

        if Services().isfloat(price):
            price = Services().floatpoint(price)
        else:
            price = 0
        insert_todo(Todo(object=object, task=task, price=price))
        self.results = get_all_todos()
        self.tasks_list(object)


    def insert_new_object(self):
        InsertNewObject()


    def delete(self, id, object):
        delete_todo(id)
        self.results = get_all_todos()
        count = 0
        for result in self.results:
            item = Todo(result)
            if item.id == object:
                count +=1
        if count == 0:
            self.objects_buttons_frame.destroy()
            self.objects_buttons_frm()
        self.tasks_list(self.results[0].object)


    def edit(self, id, task, price, object):
        EditWindow(id, task, price, object)   


    def note(self, id, text, object):
        InsertNote(id, text, object)


    def __reset_btn_color(self, item, object):
        for child in item.winfo_children():
            if child.cget('text') == object:
                child.configure(border_color='#00FFFF', text_color='#00FFFF', border_width=2, hover=False)
            else:
                child.configure(border_color=['#3E454A', '#949A9F'], border_width=0, text_color='#DCE4EE', fg_color=['#3B8ED0', '#1F6AA5'], hover=True)

    
    def __entry_limit(self, *args):
        font = self.objects_label.cget('font')
        if 'price' in args:
            entry = self.priceinsert
        elif 'task' in args:
            entry = self.taskinsert
        measure = font.measure(entry.get())
        if measure > 120:
            entry.configure(state='disabled')
        return True
            

class InsertNote(customtkinter.CTkToplevel):

    def __init__(self, id, text, object):
        super().__init__()
        self.title('Notepad')
        self.id = id  
        self.text = text
        self.object = object
        self.notepad_frm()  


    def notepad_frm(self):
        self.notepad_frame = customtkinter.CTkFrame(self)
        self.notepad_frame.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        self.notepad()


    def notepad(self):
        self.pad = customtkinter.CTkTextbox(self.notepad_frame, width=400, height=100)
        if self.text is not None:
            self.pad.insert(index='0.0',text=self.text)
        self.pad.grid(row=0, column=0, padx=10, pady=10, sticky='new', columnspan=2)

        ok_button = customtkinter.CTkButton(self.notepad_frame, text='Save', command=lambda :self.edit())
        ok_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        cancel_button = customtkinter.CTkButton(self.notepad_frame, text='Cancel', command=lambda :self.cancel())
        cancel_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')


    def edit(self):
        edit_note(self.id, self.pad.get(index1='0.0', index2=customtkinter.CURRENT))
        app.results = get_all_todos()
        app.tasks_list(self.object)
        self.grab_release()
        self.destroy()


    def cancel(self):
        self.grab_release()
        self.destroy()


class EditWindow(customtkinter.CTkToplevel):

    def __init__(self, id, task, price, object):
        super().__init__()
        self.title('Edit Task')

        self.id = id
        self.task = task
        self.price = price
        self.object = object
        self.insert_frm()
        self.labels()
        self.edit_task()


    def insert_frm(self):
        self.insert_frame = customtkinter.CTkFrame(self)
        self.insert_frame.grid(row=0, column=0, padx=10, pady=10, sticky='new')
        

    def labels(self):
        task_label = customtkinter.CTkLabel(self.insert_frame)
        task_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        task_label.configure(text='Task', width=150)
        price_label = customtkinter.CTkLabel(self.insert_frame)
        price_label.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        price_label.configure(text='Price', width=150)


    def edit_task(self):

        validation_command = self.register(self.__entry_limit)

        taskentry = customtkinter.StringVar()
        self.taskinsert = customtkinter.CTkEntry(self.insert_frame, textvariable=taskentry)
        self.taskinsert.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.taskinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'task'))
        self.taskinsert.insert(0, self.task)

        pricentry = customtkinter.StringVar()
        self.priceinsert = customtkinter.CTkEntry(self.insert_frame, textvariable=pricentry)
        self.priceinsert.grid(row=1, column=1, padx=10, pady=10, sticky='we')
        self.priceinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'price'))
        self.priceinsert.insert(0, self.price)

        buttoninsert = customtkinter.CTkButton(self.insert_frame, text='Confirm', command=lambda :self.confirm_edit())
        buttoninsert.grid(row=1, column=2, padx=10, pady=10, sticky='e')


    def confirm_edit(self):
        if self.taskinsert.get() != self.task and self.taskinsert.get() != '':
            edit_task(self.id, self.taskinsert.get())
        if self.priceinsert.get() != self.price and Services().isfloat(self.priceinsert.get()):
            edit_price(self.id, Services().floatpoint(self.priceinsert.get()))
        app.results = get_all_todos()
        app.tasks_list(self.object)

        self.grab_release()
        self.destroy()


    def __entry_limit(self, *args):
        font = app.objects_label.cget('font')
        if 'price' in args:
            entry = self.priceinsert
        elif 'task' in args:
            entry = self.taskinsert
        measure = font.measure(entry.get())
        if measure > 120:
            entry.configure(state='disabled')
        return True



class InsertNewObject(customtkinter.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title('Insert New Object')
        self.insert_frm()
        self.insert_labels()
        self.insert_object()


    def insert_frm(self):
        self.insert_frame = customtkinter.CTkFrame(self)
        self.insert_frame.grid(row=0, column=0, padx=10, pady=10, sticky='new')


    def insert_labels(self):
        object_label = customtkinter.CTkLabel(self.insert_frame, text='Object')
        object_label.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        task_label = customtkinter.CTkLabel(self.insert_frame, text='Task')
        task_label.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        price_label = customtkinter.CTkLabel(self.insert_frame, text='$$$')
        price_label.grid(row=0, column=2, padx=10, pady=10, sticky='n')


    def insert_object(self):

        validation_command = self.register(self.__entry_limit)

        objectentry = customtkinter.StringVar()
        self.objectinsert = customtkinter.CTkEntry(self.insert_frame, textvariable=objectentry)
        self.objectinsert.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.objectinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'object'))

        taskentry = customtkinter.StringVar()
        self.taskinsert = customtkinter.CTkEntry(self.insert_frame, textvariable=taskentry)
        self.taskinsert.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.taskinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'task'))

        pricentry = customtkinter.StringVar()
        self.priceinsert = customtkinter.CTkEntry(self.insert_frame, textvariable=pricentry)
        self.priceinsert.grid(row=1, column=2, padx=10, pady=10, sticky='we')
        self.priceinsert.configure(validate='key', validatecommand=(validation_command, "%P", 'price'))

        buttoninsert = customtkinter.CTkButton(self.insert_frame, text='Insert', command=lambda :self.insert_new())
        buttoninsert.grid(row=2, column=0, padx=10, pady=10, sticky='we', columnspan=3)
        cancel_button = customtkinter.CTkButton(self.insert_frame, text='Cancel', command=lambda :self.cancel())
        cancel_button.grid(row=3, column=0, padx=10, pady=10, sticky='ew', columnspan=3)


    def cancel(self):
        self.grab_release()
        self.destroy()


    def insert_new(self):
        if Services().isfloat(self.priceinsert.get()):
            price = Services().floatpoint(self.priceinsert.get())
        else:
            price = 0
        insert_todo(Todo(object=self.objectinsert.get(), task=self.taskinsert.get(), price=price))
        app.objects_buttons_frame.destroy()
        app.objects_buttons_frm()
        app.tasks_list(self.objectinsert.get())

        self.grab_release()
        self.destroy()


    def __entry_limit(self, *args):
        font = app.objects_label.cget('font')
        if 'price' in args:
            entry = self.priceinsert
        elif 'task' in args:
            entry = self.taskinsert
        elif 'object':
            entry = self.objectinsert
        measure = font.measure(entry.get())
        if measure > 120:
            entry.configure(state='disabled')
        return True
           

class Services:

    def __init__(self):
        pass


    def isfloat(self, num:str):

        num = num.replace(',', '.')
        try:
            num = float(num)
            return True
        except ValueError:
            return False


    def floatpoint(self, num:str):
        num = num.replace(',', '.')
        return num



if __name__ == '__main__':
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('blue')
    app = App()
    app.mainloop()
