import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Create database connection
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS bmi_data
             (id INTEGER PRIMARY KEY, 
              name TEXT, 
              weight REAL, 
              height REAL, 
              bmi REAL, 
              date TEXT)''')
conn.commit()

# BMI Calculator class
class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Create GUI components
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.weight_label = tk.Label(root, text="Weight (kg):")
        self.weight_label.pack()
        self.weight_entry = tk.Entry(root)
        self.weight_entry.pack()

        self.height_label = tk.Label(root, text="Height (m):")
        self.height_label.pack()
        self.height_entry = tk.Entry(root)
        self.height_entry.pack()

        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.history_button = tk.Button(root, text="View History", command=self.view_history)
        self.history_button.pack()

        self.trend_button = tk.Button(root, text="View Trends", command=self.view_trends)
        self.trend_button.pack()

    def calculate_bmi(self):
        name = self.name_entry.get()
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError

            bmi = weight / (height ** 2)
            self.result_label.config(text=f"Hello {name}, your BMI is {bmi:.2f}")

            # Save to database
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO bmi_data (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                      (name, weight, height, bmi, date))
            conn.commit()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for weight and height.")

    def view_history(self):
        name = self.name_entry.get()
        c.execute("SELECT * FROM bmi_data WHERE name=?", (name,))
        rows = c.fetchall()
        history_text = "\n".join([f"Date: {row[5]}, BMI: {row[4]:.2f}" for row in rows])
        messagebox.showinfo("History", history_text)

    def view_trends(self):
        name = self.name_entry.get()
        c.execute("SELECT date, bmi FROM bmi_data WHERE name=?", (name,))
        rows = c.fetchall()

        if not rows:
            messagebox.showinfo("No data", "No data available for the user.")
            return

        dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in rows]
        bmis = [row[1] for row in rows]

        # Plotting the trends
        plt.figure(figsize=(10, 5))
        plt.plot(dates, bmis, marker='o', linestyle='-', color='b')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.title(f'BMI Trends for {name}')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

