# ცვლილება: დასახელება და იმპორტი შესაბამისი გახდა
import unittest
from main import Hotel, Room, Customer

# ტესტების კლასი
class TestHotelSystem(unittest.TestCase):
    # ტესტისთვის საჭირო ობიექტების შექმნა
    def setUp(self):
        self.hotel = Hotel("სასტუმრო თბილისური სამოთხე")
        self.room = Room(1, "Single", 100, 1)
        self.hotel.add_room(self.room)
        self.customer = Customer("გიორგი", 500)

    # გადახდის ფუნქციის ტესტი
    def test_pay_for_booking(self):
        result = self.customer.pay_for_booking(200)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 300)
        self.assertEqual(self.customer.points, 20)  # ქულების დადასტურება

    # დაჯავშნა და გაუქმების ტესტი
    def test_book_and_cancel(self):
        booked = self.hotel.book_room_for_customer(self.customer, 1, 2)
        self.assertTrue(booked)
        self.assertFalse(self.room.is_available)

        canceled = self.hotel.cancel_booking(self.customer, 1)
        self.assertTrue(canceled)
        self.assertTrue(self.room.is_available)
        self.assertGreater(self.customer.budget, 0)
        self.assertEqual(self.customer.points, 0)  # ქულების კორექტირება

    # მომხმარებლის ინფორმაციის განახლების ტესტი
    def test_update_customer_info(self):
        self.hotel.update_customer_info(self.customer, new_name="ნიკა", new_budget=800)
        self.assertEqual(self.customer.name, "ნიკა")
        self.assertEqual(self.customer.budget, 800)


if __name__ == '__main__':
    unittest.main()


