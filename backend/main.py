import logging
from datetime import datetime

logging.basicConfig(filename='hotel_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


class Room:
    def __init__(self, room_number, room_type, price_per_night, max_guests):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.is_available = True

    def book_room(self):
        self.is_available = False

    def release_room(self):
        self.is_available = True

    def calculate_price(self, nights):
        return round(self.price_per_night * nights, 2)

    def __str__(self):
        status = "თავისუფალია" if self.is_available else "დაკავებულია"
        return f"#{self.room_number} | ტიპი: {self.room_type} | ღამე: {self.price_per_night}₾ | {status}"


class Customer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.booked_rooms = {}

    def pay_for_booking(self, total_price):
        if self.budget >= total_price:
            self.budget -= total_price
            return True
        return False

    def add_room(self, room, total_price):
        self.booked_rooms[room.room_number] = {"room": room, "price": total_price}

    def remove_room(self, room_number):
        if room_number in self.booked_rooms:
            self.booked_rooms.pop(room_number)

    def refund(self, amount):
        self.budget += amount

    def summary(self):
        if not self.booked_rooms:
            return f"{self.name}-ს ჯერ არაფერი დაუჯავშნია.\n"
        text = f"\n{self.name}-ის აქტიური დაჯავშნები:\n"
        for data in self.booked_rooms.values():
            room = data["room"]
            text += f" - #{room.room_number} ({room.room_type}) – {data['price']}₾\n"
        text += f"დარჩენილი ბიუჯეტი: {self.budget}₾\n"
        return text


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.log = []

    def add_room(self, room):
        self.rooms.append(room)

    def show_available(self):
        free = [r for r in self.rooms if r.is_available]
        if not free:
            print("\nამჟამად თავისუფალი ოთახები არ გვაქვს.\n")
        else:
            print("\nხელმისაწვდომი ოთახები:")
            for r in free:
                print(" ", r)

    def find_room(self, number):
        for r in self.rooms:
            if r.room_number == number:
                return r
        return None

    def log_booking(self, customer, room, price):
        line = f"{customer.name} დაჯავშნა #{room.room_number} ({room.room_type}) – {price}₾"
        logging.info(line)
        self.log.append(line)

    def book_room_for_customer(self, customer, number, nights):
        room = self.find_room(number)
        if not room:
            print("ასეთი ოთახი ვერ მოიძებნა.")
            return False
        if not room.is_available:
            print("ეს ოთახი უკვე დაკავებულია.")
            return False

        total = room.calculate_price(nights)
        if customer.pay_for_booking(total):
            room.book_room()
            customer.add_room(room, total)
            self.log_booking(customer, room, total)
            print(f"დაჯავშნა წარმატებით დასრულდა! ღირებულება: {total}₾")
            return True
        else:
            print("ბიუჯეტი არ არის საკმარისი ამ ოთახისთვის.")
            return False

    def cancel_booking(self, customer, room_number):
        room = self.find_room(room_number)
        if not room:
            print("ასეთი ოთახი არ მოიძებნა.")
            return False
        if room_number not in customer.booked_rooms:
            print("ეს ოთახი თქვენზე არ არის დაჯავშნილი.")
            return False

        refund_amount = customer.booked_rooms[room_number]["price"]
        customer.refund(refund_amount)
        customer.remove_room(room_number)
        room.release_room()

        line = f"{customer.name}-მ გააუქმა დაჯავშნა #{room.room_number} ({room.room_type}) – თანხა დაბრუნდა: {refund_amount}₾"
        logging.info(line)
        print(f"დაჯავშნა გაუქმდა. თანხა დაბრუნდა: {refund_amount}₾")
        return True

    def update_customer_info(self, customer, new_name=None, new_budget=None):
        if new_name:
            customer.name = new_name
        if new_budget is not None:
            customer.budget = new_budget
        print("მომხმარებლის მონაცემები განახლდა წარმატებით.")


if __name__ == "__main__":
    hotel = Hotel("სასტუმრო")
    hotel.add_room(Room(5, "Single", 80, 1))
    hotel.add_room(Room(10, "Double", 160, 2))
    hotel.add_room(Room(15, "Family", 300, 4))

    print("მოგესალმებით სასტუმროში!\n")

    name = input("შეიყვანეთ თქვენი სახელი: ").strip()
    budget = float(input("შეიყვანეთ ბიუჯეტი (₾): "))
    user = Customer(name, budget)

    while True:
        print("\n--- მენიუ ---")
        print("1. ხელმისაწვდომი ოთახების ნახვა")
        print("2. ოთახის დაჯავშნა")
        print("3. დაჯავშნის გაუქმება")
        print("4. მომხმარებლის მონაცემების განახლება")
        print("5. ჩემი დაჯავშნები")
        print("6. გამოსვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        if choice == "1":
            hotel.show_available()
        elif choice == "2":
            try:
                num = int(input("შეიყვანეთ ოთახის ნომერი: "))
                nights = int(input("რამდენი ღამე გსურთ დარჩენა: "))
                hotel.book_room_for_customer(user, num, nights)
            except ValueError:
                print("გთხოვთ შეიყვანოთ სწორი რიცხვები.")
        elif choice == "3":
            try:
                num = int(input("შეიყვანეთ გასაუქმებელი ოთახის ნომერი: "))
                hotel.cancel_booking(user, num)
            except ValueError:
                print("გთხოვთ შეიყვანოთ სწორი ნომერი.")
        elif choice == "4":
            new_name = input("ახალი სახელი (ან დააჭირეთ Enter-ს გასატოვებლად): ").strip()
            new_budget = input("ახალი ბიუჯეტი (ან Enter): ").strip()
            if new_budget:
                try:
                    new_budget = float(new_budget)
                except ValueError:
                    print("ბიუჯეტი უნდა იყოს რიცხვი.")
                    continue
            else:
                new_budget = None
            hotel.update_customer_info(user, new_name or None, new_budget)
        elif choice == "5":
            print(user.summary())
        elif choice == "6":
            print("\nმადლობა, რომ ესტუმრეთ ჩვენს სასტუმროს!\n")
            break
        else:
            print("გთხოვთ აირჩიოთ სწორი ოპცია (1-6).")

