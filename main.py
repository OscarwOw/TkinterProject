import tkinter as tk
from tkinter import ttk
import csv

def load_patients(filename):
    patients = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    patients.append(row)
    except FileNotFoundError:
        return []
    return patients

def save_patients(filename, patients):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for patient in patients:
            writer.writerow(patient)



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Pacient Documentation')
        self.geometry('800x600')

        self.patient_file = 'patients.csv'
        self.patient_data = load_patients(self.patient_file)

        style = ttk.Style()
        style.configure("MyButtonStyle.TButton", font=("Helvetica", 12), background="blue", foreground="black")


        self.nav_frame = ttk.Frame(self, height=50, relief=tk.RAISED, borderwidth=2)
        self.nav_frame.pack(side="top", fill="x")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.menubar = tk.Menu(self)
        filemenu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Súbor", menu=filemenu)


        filemenu.add_command(label="Zoznam pacientov", command=lambda: self.show_frame(HomePage))
        filemenu.add_command(label="Pridať pacienta", command=lambda: self.show_frame(AddPatient))
        filemenu.add_command(label="Tlačiť detail pacienta", command=self.show_print_message)
        filemenu.add_command(label="Koniec", command=self.quit_program)

        self.menubar.add_command(label="Autor", command=self.show_author_info)
        self.menubar.add_command(label="Pomoc", command=self.show_help_info)

        self.config(menu=self.menubar)

        self.pages = {}
        for F in (HomePage, UpdatePatient, AddPatient):
            page = F(self.main_frame, self)
            self.pages[F] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Button(self.nav_frame, text="Zoznam pacientov", command=lambda: self.show_frame(HomePage), style="MyButtonStyle.TButton").pack(side="left")
        ttk.Button(self.nav_frame, text="Uprav pacienta", command=lambda: self.show_frame(UpdatePatient), style="MyButtonStyle.TButton").pack(side="left")
        ttk.Button(self.nav_frame, text="Pridat pacienta", command=lambda: self.show_frame(AddPatient), style="MyButtonStyle.TButton").pack(side="left")



        self.show_frame(HomePage)

    def show_frame(self, context):
        frame = self.pages[context]
        frame.tkraise()

    def show_frame_with_data(self, context, data):
        frame = self.pages[context]
        if hasattr(frame, 'populate_form'):
            frame.populate_form(data)
        frame.tkraise()

    def on_patient_select(self, patient_details):
        if len(patient_details) < 7:
            patient_details += [''] * (7 - len(patient_details))
        self.show_frame_with_data(UpdatePatient, patient_details)

    def load_patient_data(self):
        return load_patients(self.patient_file)

    def save_patient_data(self):
        save_patients(self.patient_file, self.patient_data)

    def show_print_message(self):
        print_window = tk.Toplevel(self)
        print_window.title("Tlačenie")
        print_window.geometry("300x100")
        tk.Label(print_window, text="Tlačenie spustené", font=('Helvetica', 12)).pack(pady=20)
        ttk.Button(print_window, text="OK", command=print_window.destroy, style="MyButtonStyle.TButton").pack()

    def quit_program(self):
        self.destroy()

    def show_author_info(self):
        author_window = tk.Toplevel(self)
        author_window.title("Autor")
        author_window.geometry("500x100")
        tk.Label(author_window, text="Program napísaný na predmet uživateľské rozhrania Adamom Belošom", font=('Helvetica', 12)).pack(pady=20)
        ttk.Button(author_window, text="Zavrieť", command=author_window.destroy, style="MyButtonStyle.TButton").pack()

    def show_help_info(self):
        help_window = tk.Toplevel(self)
        help_window.title("Pomoc")
        help_window.geometry("300x100")
        tk.Label(help_window, text="program na správu pacientov", font=('Helvetica', 12)).pack(pady=20)
        ttk.Button(help_window, text="Zavrieť", command=help_window.destroy, style="MyButtonStyle.TButton").pack()

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Zoznam pacientov", font=('Helvetica', 16)).pack(pady=10)

        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5, padx=10, fill='x')

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)

        search_button = ttk.Button(search_frame, text="vyhladat paientov", command=self.search_patient, style="MyButtonStyle.TButton")
        search_button.pack(side='left')

        delete_button = ttk.Button(search_frame, text="vymazat pacienta", command=self.delete_patient, style="MyButtonStyle.TButton")
        delete_button.pack(side='right', padx=(10, 0))

        self.tree = ttk.Treeview(self, columns=('Full Name', 'Age', 'Weight', 'Height', 'Diagnosis'), show='headings')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        self.tree.heading('Full Name', text='Cele meno')
        self.tree.heading('Age', text='Vek')
        self.tree.heading('Weight', text='Váha(kg)')
        self.tree.heading('Height', text='Výška(cm)')
        self.tree.heading('Diagnosis', text='Diagnozy')

        self.tree.column('Full Name', width=120)
        self.tree.column('Age', width=80)
        self.tree.column('Weight', width=80)
        self.tree.column('Height', width=80)
        self.tree.column('Diagnosis', width=120)

        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.controller = controller

        self.populate_tree()

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        item = self.tree.item(item_id)
        patient_details = item['values']

        self.controller.on_patient_select(patient_details)

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for patient in self.controller.patient_data:
            self.tree.insert('', tk.END, values=patient)

    def search_patient(self):
        search_term = self.search_var.get().lower()
        filtered_patients = [patient for patient in self.controller.patient_data if search_term in patient[0].lower()]
        for i in self.tree.get_children():
            self.tree.delete(i)
        for patient in filtered_patients:
            self.tree.insert('', tk.END, values=patient)

    def delete_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_index = self.tree.index(selected_item[0])
        del self.controller.patient_data[item_index]
        self.tree.delete(selected_item[0])
        self.controller.save_patient_data()

class UpdatePatient(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.patient_data = None
        ttk.Label(self, text="Uprav pacienta", font=('Helvetica', 16)).pack(pady=10)

        self.entries = {}
        labels = ["Cele Meno", "Vek", "Váha(kg)", "Výška(cm)", "Diagnóza", "Alergie", "Užívané lieky"]
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)

        self.sex_var = tk.StringVar()
        ttk.Label(form_frame, text="Pohlavie").grid(row=len(labels), column=0, sticky="W", padx=10, pady=5)
        ttk.Radiobutton(form_frame, text='Muž', variable=self.sex_var, value='Muž').grid(row=len(labels), column=1,
                                                                                         sticky="W")
        ttk.Radiobutton(form_frame, text='Žena', variable=self.sex_var, value='Žena').grid(row=len(labels), column=1,
                                                                                           sticky="E")

        for i, text in enumerate(labels):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky="W", padx=10, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky="EW", padx=10, pady=5)
            self.entries[text] = entry

        submit_button = ttk.Button(self, text="Uložiť zmeny", command=self.save_changes, style="MyButtonStyle.TButton")
        submit_button.pack(pady=10)

    def populate_form(self, patient_data):
        for i, key in enumerate(list(self.entries.keys()) + ["Pohlavie"]):
            if key == "Pohlavie":
                self.sex_var.set(patient_data[i])
            else:
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, patient_data[i])

    def save_changes(self):
        updated_data = [self.entries[label].get() for label in self.entries]
        updated_data.append(self.sex_var.get())

        selected_id = self.controller.pages[HomePage].tree.selection()[0]
        selected_index = self.controller.pages[HomePage].tree.index(selected_id)

        self.controller.patient_data[selected_index] = updated_data

        self.controller.save_patient_data()

        self.controller.pages[HomePage].populate_tree()

        print("Saved changes for:", updated_data)
        self.show_submit_info()

    def show_submit_info(self):
        help_window = tk.Toplevel(self)
        help_window.title("Pomoc")
        help_window.geometry("300x100")
        tk.Label(help_window, text="Údaje uložené", font=('Helvetica', 12)).pack(pady=20)
        tk.Button(help_window, text="Zavrieť", command=help_window.destroy, style="MyButtonStyle.TButton").pack()


class AddPatient(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Pridaj pacienta", font=('Helvetica', 16)).pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)

        labels = ["Cele Meno", "Vek", "Váha(kg)", "Výška(cm)", "Diagnóza", "Alergie", "Užívané lieky"]
        self.entries = {}
        for i, text in enumerate(labels):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky="W", padx=10, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky="EW", padx=10, pady=5)
            self.entries[text] = entry

        self.sex_var = tk.StringVar()
        ttk.Label(form_frame, text="Pohlavie").grid(row=len(labels), column=0, sticky="W", padx=10, pady=5)
        ttk.Radiobutton(form_frame, text='Muž', variable=self.sex_var, value='Muž').grid(row=len(labels), column=1,
                                                                                         sticky="W")
        ttk.Radiobutton(form_frame, text='Žena', variable=self.sex_var, value='Žena').grid(row=len(labels), column=1,
                                                                                           sticky="E")

        submit_button = ttk.Button(self, text="Pridať pacienta", command=self.submit_form, style="MyButtonStyle.TButton")
        submit_button.pack(pady=10)

    def submit_form(self):
        form_data = [self.entries[label].get() for label in self.entries] + [self.sex_var.get()]
        with open(self.controller.patient_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(form_data)
        print("New patient added:", form_data)
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.sex_var.set('')

        self.controller.patient_data.append(form_data)
        self.controller.pages[HomePage].populate_tree()
        self.show_submit_info()

    def show_submit_info(self):
        help_window = tk.Toplevel(self)
        help_window.title("Pomoc")
        help_window.geometry("300x100")
        tk.Label(help_window, text="Údaje uložené", font=('Helvetica', 12)).pack(pady=20)
        tk.Button(help_window, text="Zavrieť", command=help_window.destroy, style="MyButtonStyle.TButton").pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()