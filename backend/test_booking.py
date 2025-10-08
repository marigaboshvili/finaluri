import unittest
from hotel_backend import Hotel, Room, Customer


class TestHotelSystem(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel("სასტუმრო თბილისური სამოთხე")
        self.room = Room(1, "Single", 100, 1)
        self.hotel.add_room(self.room)
        self.customer = Customer("გიორგი", 500)

    def test_pay_for_booking(self):
        result = self.customer.pay_for_booking(200)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 300)

    def test_book_and_cancel(self):
        booked = self.hotel.book_room_for_customer(self.customer, 1, 2)
        self.assertTrue(booked)
        self.assertFalse(self.room.is_available)

        canceled = self.hotel.cancel_booking(self.customer, 1)
        self.assertTrue(canceled)
        self.assertTrue(self.room.is_available)
        self.assertGreater(self.customer.budget, 0)

    def test_update_customer_info(self):
        self.hotel.update_customer_info(self.customer, new_name="ნიკა", new_budget=800)
        self.assertEqual(self.customer.name, "ნიკა")
        self.assertEqual(self.customer.budget, 800)


if __name__ == '__main__':
    unittest.main()

