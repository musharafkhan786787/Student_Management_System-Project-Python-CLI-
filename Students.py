import csv
import os

class Pupil:
    def __init__(self, roll, name, age, grade):
        self.roll = roll
        self.name = name
        self.age = age
        self.grade = grade

    def as_row(self):
        return [self.roll, self.name, self.age, self.grade]

class PupilDirectory:
    def __init__(self, filepath='students.csv'):
        self.filepath = filepath
        self.records = []
        self._initialize_data()

    def _initialize_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                next(csv_reader, None)  # skip header
                self.records = [Pupil(*line) for line in csv_reader if len(line) == 4]
                print(f"✅ {len(self.records)} records loaded.")
        else:
            with open(self.filepath, 'w', newline='') as file:
                csv.writer(file).writerow(['Roll', 'Name', 'Age', 'Grade'])
            print("🆕 File created successfully.")

    def _persist_data(self):
        with open(self.filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Roll', 'Name', 'Age', 'Grade'])
            for pupil in self.records:
                writer.writerow(pupil.as_row())
        print(f"💾 Saved {len(self.records)} records.")

    def insert(self):
        print("\n✏️ New Entry")
        roll = input("Roll No: ")
        name = input("Name: ")
        age = input("Age: ")
        grade = input("Grade: ")
        self.records.append(Pupil(roll, name, age, grade))
        self._persist_data()

    def show_all(self):
        if not self.records:
            print("\n⚠️ No data found.\n")
            return
        print("\n📘 Student Records")
        print("-" * 50)
        print(f"{'Roll':<10} {'Name':<15} {'Age':<5} {'Grade':<6}")
        print("-" * 50)
        for entry in self.records:
            print(f"{entry.roll:<10} {entry.name:<15} {entry.age:<5} {entry.grade:<6}")
        print("-" * 50)

    def modify(self):
        roll = input("Enter Roll No to edit: ")
        found = next((s for s in self.records if s.roll == roll), None)
        if found:
            print(f"Editing record of {found.name}")
            found.name = input("New Name: ")
            found.age = input("New Age: ")
            found.grade = input("New Grade: ")
            self._persist_data()
            print("🔁 Record updated.")
        else:
            print("❌ No record found.")

    def remove(self):
        roll = input("Enter Roll No to delete: ")
        original_len = len(self.records)
        self.records = [s for s in self.records if s.roll != roll]
        if len(self.records) < original_len:
            self._persist_data()
            print("🗑️ Record deleted.")
        else:
            print("❌ Record not found.")

    def load_external_csv(self, file_path):
        if not os.path.isfile(file_path):
            print("❌ File does not exist.")
            return

        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if not headers:
                print("⚠️ Invalid file format.")
                return

            print("🧾 Headers found:", ', '.join(headers))
            full = input("View full file? (yes/no): ").strip().lower()

            if full == 'yes':
                print("\n🧾 Complete Data")
                print('-' * 50)
                print('\t'.join(headers))
                for row in reader:
                    print('\t'.join(row))
                print('-' * 50)
            else:
                cols = input("Enter desired columns (comma separated): ").lower().split(',')
                cols = [col.strip() for col in cols]
                indices = [i for i, h in enumerate(headers) if h.lower() in cols]

                if not indices:
                    print("⚠️ No valid columns selected.")
                    return

                print("\n🔍 Selected Columns")
                print('-' * 50)
                print('\t'.join([headers[i] for i in indices]))
                for row in reader:
                    print('\t'.join([row[i] for i in indices]))
                print('-' * 50)

def run_program():
    book = PupilDirectory()

    while True:
        print("\n📚 STUDENT DIRECTORY MENU")
        print("1. Add New Student")
        print("2. Modify Existing Record")
        print("3. Delete Record")
        print("4. Show All Students")
        print("5. Import from CSV")
        print("6. Exit")
        print("----------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            book.insert()
        elif choice == '2':
            book.modify()
        elif choice == '3':
            book.remove()
        elif choice == '4':
            book.show_all()
        elif choice == '5':
            filepath = input("Enter path of external CSV: ")
            book.load_external_csv(filepath)
        elif choice == '6':
            print("👋 Exiting... Thank you!")
            break
        else:
            print("⚠️ Invalid selection.")

if __name__ == "__main__":
    run_program()
