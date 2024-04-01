import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3

# Продукт
class Car:
    def __init__(self):
        self.engine = None
        self.wheels = None
        self.bodywork = None
        self.gear_shift_box = None

    def __str__(self):
        return f"Car: Engine={self.engine}, Wheels={self.wheels}, Bodywork={self.bodywork}, GearShiftBox={self.gear_shift_box}"

# Строитель
class CarAssembler:
    def __init__(self, builder_gui):
        self.car = Car()
        self.builder_gui = builder_gui

    def set_engine(self, engine):
        self.car.engine = engine

    def set_wheels(self, wheels):
        self.car.wheels = wheels

    def set_bodywork(self, bodywork):
        self.car.bodywork = bodywork

    def set_gear_shift_box(self, gear_shift_box):
        self.car.gear_shift_box = gear_shift_box

# Конкретные строители
class SportCarAssembler(CarAssembler):
    def __init__(self, builder_gui):
        super().__init__(builder_gui)

    def set_engine(self):
        engine_choice = self.show_choice_dialog("Выберите двигатель", ["Toyota 2JZ", "Ferrari V8", "Ford V6"])
        self.car.engine = engine_choice

    def set_wheels(self):
        wheels_choice = self.show_choice_dialog("Выберите колеса", ["Michelin Sports", "Pirelli P Zero", "Dunlop Sport"])
        self.car.wheels = wheels_choice

    def set_bodywork(self):
        self.car.bodywork = "Coupe"

    def set_gear_shift_box(self):
        gear_shift_box_choice = self.show_choice_dialog("Выберите коробку передач", ["Manual", "Automatic"])
        self.car.gear_shift_box = gear_shift_box_choice

    def show_choice_dialog(self, title, choices):
        choice = simpledialog.askstring(title, "Выберите:", initialvalue=choices[0], parent=self.builder_gui)
        if choice and choice in choices:
            return choice
        else:
            return choices[0]

class FamilyCarAssembler(CarAssembler):
    def __init__(self, builder_gui):
        super().__init__(builder_gui)

    def set_engine(self):
        engine_choice = self.show_choice_dialog("Выберите двигатель", ["Volvo V4X", "Honda i-VTEC", "Ford EcoBoost"])
        self.car.engine = engine_choice

    def set_wheels(self):
        wheels_choice = self.show_choice_dialog("Выберите колеса", ["Yokohama Basic", "Bridgestone Turanza", "Goodyear Assurance"])
        self.car.wheels = wheels_choice

    def set_bodywork(self):
        bodywork_choice = self.show_choice_dialog("Выберите тип кузова", ["Hatchback", "Sedan", "SUV"])
        self.car.bodywork = bodywork_choice

    def set_gear_shift_box(self):
        gear_shift_box_choice = self.show_choice_dialog("Выберите коробку передач", ["Manual", "Automatic"])
        self.car.gear_shift_box = gear_shift_box_choice

    def show_choice_dialog(self, title, choices):
        choice = simpledialog.askstring(title, "Выберите:", initialvalue=choices[0], parent=self.builder_gui)
        if choice and choice in choices:
            return choice
        else:
            return choices[0]

# Директор
class CarDirector:
    def __init__(self, builder, builder_gui):
        self.builder = builder
        self.builder_gui = builder_gui

    def build_car(self):
        self.builder.set_engine()
        self.builder.set_wheels()
        self.builder.set_bodywork()
        self.builder.set_gear_shift_box()

    def get_car(self):
        return self.builder.car

# Гараж
class Garage(tk.Toplevel):
    def __init__(self, master, cars):
        super().__init__(master)
        self.title("Гараж")
        self.geometry("300x200")

        self.cars_listbox = tk.Listbox(self)
        self.cars_listbox.pack(expand=True, fill=tk.BOTH)

        self.populate_cars_list(cars)

        view_button = ttk.Button(self, text="Посмотреть", command=self.view_car)
        view_button.pack(pady=5)

        delete_button = ttk.Button(self, text="Удалить", command=self.delete_car)
        delete_button.pack(pady=5)

    def populate_cars_list(self, cars):
        for car in cars:
            self.cars_listbox.insert(tk.END, str(car))

    def view_car(self):
        selected_index = self.cars_listbox.curselection()
        if selected_index:
            selected_car = self.cars_listbox.get(selected_index)
            messagebox.showinfo("Просмотр машины", selected_car)

    def delete_car(self):
        selected_index = self.cars_listbox.curselection()
        if selected_index:
            self.cars_listbox.delete(selected_index)

# Графический интерфейс пользователя
class CarBuilderGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Car Builder")
        self.geometry("400x300")

        self.builder_type_var = tk.StringVar()
        self.builder_type_var.set("")
        self.cars = []

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Выберите тип машины:")
        label.pack(pady=10)

        sport_car_button = ttk.Button(self, text="Спортивная машина", command=self.build_sport_car)
        sport_car_button.pack(pady=5)

        family_car_button = ttk.Button(self, text="Семейная машина", command=self.build_family_car)
        family_car_button.pack(pady=5)

        view_garage_button = ttk.Button(self, text="Гараж", command=self.view_garage)
        view_garage_button.pack(pady=5)

        exit_button = ttk.Button(self, text="Завершить", command=self.destroy)
        exit_button.pack(pady=5)

    def build_sport_car(self):
        self.builder_type_var.set("1")
        builder_gui = tk.Toplevel(self)
        builder = SportCarAssembler(builder_gui)
        director = CarDirector(builder, builder_gui)
        director.build_car()

        car = director.get_car()
        self.cars.append(car)
        result_label = ttk.Label(self, text=f"Собрана машина: {car}")
        result_label.pack(pady=10)

        # Сохранение информации в базу данных
        save_to_database(car)

    def build_family_car(self):
        self.builder_type_var.set("2")
        builder_gui = tk.Toplevel(self)
        builder = FamilyCarAssembler(builder_gui)
        director = CarDirector(builder, builder_gui)
        director.build_car()

        car = director.get_car()
        self.cars.append(car)
        result_label = ttk.Label(self, text=f"Собрана машина: {car}")
        result_label.pack(pady=10)

        # Сохранение информации в базу данных
        save_to_database(car)

    def view_garage(self):
        garage_window = Garage(self, self.cars)
        garage_window.mainloop()

# Функция для сохранения информации о машине в базу данных
def save_to_database(car):
    connection = sqlite3.connect('cars_database.db')
    cursor = connection.cursor()

    # Создание таблицы, если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine TEXT,
            wheels TEXT,
            bodywork TEXT,
            gear_shift_box TEXT
        )
    ''')

    # Вставка данных о машине
    cursor.execute('''
        INSERT INTO cars (engine, wheels, bodywork, gear_shift_box)
        VALUES (?, ?, ?, ?)
    ''', (car.engine, car.wheels, car.bodywork, car.gear_shift_box))

    # Сохранение изменений и закрытие соединения
    connection.commit()
    connection.close()

if __name__ == "__main__":
    app = CarBuilderGUI()
    app.mainloop()
