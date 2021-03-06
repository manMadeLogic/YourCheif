import unittest
from YourChef.menu import MenuHelper
from Test.SampleManageDish import manage_fail_dish, insert_dishes
# from Test.SampleManageDish import manage_fail_dish, insert_dishes, dishes


class TestManageDishCase(unittest.TestCase):
    def testServer(self):
        server = MenuHelper('test_dish2')
        assert server is not None

    def testFailAddDish(self):
        server = MenuHelper("test_dish2")
        for dish in manage_fail_dish:
            result, message = server.addDish(dish['restaurant'], dish)
            assert not result

    def testAddAndDeleteDish(self):
        server = MenuHelper("test_dish2")
        for dish in insert_dishes:
            result, message = server.addDish(dish['restaurant'], dish)
            assert result

        for dish in insert_dishes:
            assert server.deleteDish(dish['restaurant'], dish["dishname"])


    def testCart(self):
        server = MenuHelper("test_dish2")
        # server = MenuHelper()

        session = dict()
        session['dishes'] = [['a', 10, 1]]
        session['total_dishes'] = 1
        session['total'] = 1.0
        session['restaurant'] = 'a'

        assert server.add_to_cart(session, "a", "c", 1)
        # print(len(session['dishes']))
        # print(session['dishes'])
        assert len(session['dishes']) == 2 and session['total_dishes'] == 2
        assert server.add_to_cart(session, "a", "a", 1)
        assert server.add_to_cart(session, "a", "c", 1)
        # print(server.add_to_cart(session, "a", "zzzzz", 1))
        assert not server.add_to_cart(session, "a", "zzzzz", 1)
        # print(len(session['dishes']))
        # print(session['dishes'])
        assert len(session['dishes']) == 2 and session['total_dishes'] == 4
        assert server.add_to_cart(session, "a", "a", 1)
        assert server.add_to_cart(session, "a", "c", 1)
        assert server.add_to_cart(session, "a", "a", 1)
        assert server.add_to_cart(session, "a", "c", 1)
        assert server.add_to_cart(session, "a", "a", 1)
        assert server.add_to_cart(session, "a", "c", 1)
        assert session['total_dishes'] == 10
        assert not server.add_to_cart(session, "a", "a", 1)
        assert not server.add_to_cart(session, "a", "c", 1)
        assert session['total_dishes'] == 10


if __name__ == '__main__':
    unittest.main()
