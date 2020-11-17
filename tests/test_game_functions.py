from unittest.case import TestCase

from game import Game
from play import start_game, move_robot


class TestGameFunctions(TestCase):

    def setUp(self):
        self.dim = 10

    def test_initiate_game(self):
        print(f"<<< {self.test_initiate_game.__name__} start >>>")

        game = start_game(self.dim)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game.robots), 1)
        self.assertEqual(len(game.robots_position), 1)
        self.assertEqual(len(game.dinosaurs_position), 10)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_game_control_exception(self):
        print(f"<<< {self.test_game_control_exception.__name__} start >>>")

        game = start_game(self.dim)
        with self.assertRaises(Exception):
            move_robot(game, "exception")

        print("<<< test pass >>>\n\n\n")

    def test_move_forward(self):
        print(f"<<< {self.test_move_forward.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        uuid = list(game.robots.keys())[0]
        game.move_robot_forward(uuid)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_move_forward_exceptions(self):
        print(f"<<< {self.test_move_forward_exceptions.__name__} start >>>")

        game = Game(self.dim)
        game.set_dinosaurs(0, 1)
        # set the robot at the up-right corner
        game.set_robots(0, self.dim-1)
        game.set_robots(0, 0)
        game.initial_placement()
        uuid1 = list(game.robots.keys())[0]
        uuid2 = list(game.robots.keys())[1]

        with self.assertRaises(Exception):
            game.move_robot_forward(uuid1)

        with self.assertRaises(Exception):
            game.move_robot_forward(uuid2)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_move_backward(self):
        print(f"<<< {self.test_move_backward.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, self.dim-1)
        game.initial_placement()
        uuid = list(game.robots.keys())[0]
        game.move_robot_backward(uuid)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_move_backward_exceptions(self):
        print(f"<<< {self.test_move_backward_exceptions.__name__} start >>>")

        game = Game(self.dim)
        # set the robot at the up-left corner
        game.set_dinosaurs(0, self.dim-2)
        game.set_robots(0, 0)
        game.set_robots(0, self.dim-1)
        game.initial_placement()
        uuid1 = list(game.robots.keys())[0]
        uuid2 = list(game.robots.keys())[1]

        with self.assertRaises(Exception):
            game.move_robot_backward(uuid1)

        with self.assertRaises(Exception):
            game.move_robot_backward(uuid2)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_turn_right(self):
        print(f"<<< {self.test_turn_right.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        uuid = list(game.robots.keys())[0]

        self.assertEqual(game.robots[uuid]['direction'], "E")

        game.turn_robot_right(uuid)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[uuid]['direction'], "S")
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_turn_left(self):
        print(f"<<< {self.test_turn_left.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        uuid = list(game.robots.keys())[0]

        self.assertEqual(game.robots[uuid]['direction'], "E")

        game.turn_robot_left(uuid)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[uuid]['direction'], "N")
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_attack(self):
        print(f"<<< {self.test_attack.__name__} start >>>")

        game = Game(self.dim)
        game.set_dinosaurs(0, 1)
        game.set_dinosaurs(1, 0)
        game.set_dinosaurs(1, 2)
        game.set_dinosaurs(2, 1)
        game.set_robots(1, 1)
        game.initial_placement()
        uuid = list(game.robots.keys())[0]

        game.attack(uuid)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game.dinosaurs_position), 0)
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_invalid_setting(self):
        print(f"<<< {self.test_invalid_setting.__name__} start >>>")

        game = Game(self.dim)
        with self.assertRaises(Exception):
            game.set_dinosaurs(-1, self.dim)
        with self.assertRaises(Exception):
            game.set_robots(-1, self.dim)

        print("<<< test pass >>>\n\n\n")
