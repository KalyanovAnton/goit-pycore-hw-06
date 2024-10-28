from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту. Є обов'язковим полем.
		pass

class Phone(Field):
    def __init__(self, value):
         self.value = None
         self.set_value(value)

    def set_value(self, value):
        # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
        if re.fullmatch(r'\d{10}', value):
            self.value = value
        else:
             raise ValueError("Телефон повинен містити рівно 10 цифр.")
        
    def __str__(self):
         return self.value    

class Record:
    # Клас для зберігання інформації про контакт.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
         self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
             if p.value == phone:
                  self.phones.remove(p)
                  return
        raise ValueError(f"Телефон {phone} не знайдено у списку контактів {self.name.value}.")
    
    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Телефон {old_phone} не знайдено у списку контактів {self.name.value}.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        raise ValueError(f"Телефон {phone} не знайдено у списку контактів {self.name.value}.")     

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # Клас для зберігання та управління записами контактів.
    def add_record(self, record):
        self.data[record.name.value] = record

    def fiind(self, name):
        if name in self.data:
            return self.data[name] 
        raise KeyError(f"Контакт з ім'ям {name} не знайдено.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        raise KeyError(f"Контакт з ім'ям {name} не знайдено.")

        
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return"ПОМИЛКА: Неправильний формат. Будь ласка, введіть ім'я і номер телефону."
        except IndexError:
            return "ПОМИЛКА: Недостатньо аргументів для команди."
        except KeyError:
            return "ПОМИЛКА: Контакт не знайдено."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, new_phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = new_phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name in contacts:
        return f"Мобільний телефон для {name}: {contacts[name]}"
    else:
        raise KeyError
    
    
@input_error
def show_all(args, contacts):
    if not contacts:
        return("Немає збережених контактів")
    resoult = ("Всі збережені контакти:\n")
    for name, phone in contacts.items():
        resoult += f"{name} {phone}\n"
    return resoult.strip()
 
    

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))  
        elif command == "phone":
            print(show_phone(args, contacts))  
        elif command == "all":
            print(show_all(args, contacts))        
        else:
            print("Invalid command.")    
if __name__ == "__main__":
   main()            