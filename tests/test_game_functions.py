from unittest.case import TestCase

from models.game import Game
from services.play import create_random_game, create_game, move_robot


class TestGameFunctions(TestCase):

    def setUp(self):
        self.dim = 10

    def test_initiate_random_game(self):
        print(f"<<< {self.test_initiate_random_game.__name__} start >>>")

        game = create_random_game(self.dim)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game.robots), 1)
        self.assertEqual(len(game.robots_position), 1)
        self.assertEqual(len(game.dinosaurs_position), 1)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_initiate_random_game_exception(self):
        print(f"<<< {self.test_initiate_random_game_exception.__name__} start >>>")

        with self.assertRaises(Exception):
            create_random_game(self.dim, robots_count=self.dim*self.dim+1, dinosaurs_count=0)

        with self.assertRaises(Exception):
            create_random_game(self.dim, robots_count=0, dinosaurs_count=self.dim*self.dim+1)

        with self.assertRaises(Exception):
            create_random_game(self.dim, robots_count=self.dim*self.dim//2, dinosaurs_count=self.dim*self.dim//2+1)

        print("<<< test pass >>>\n\n\n")

    def test_create_game(self):
        print(f"<<< {self.test_initiate_random_game_exception.__name__} start >>>")

        robots = [(0, 0)]
        dinosaurs = [(self.dim-1, self.dim-1)]
        game = create_game(self.dim, robots, dinosaurs)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game.robots), 1)
        self.assertEqual(len(game.robots_position), 1)
        self.assertIn((0, 0), game.robots_position)
        self.assertEqual(len(game.dinosaurs_position), 1)
        self.assertIn((self.dim-1, self.dim-1), game.dinosaurs_position)

        print("<<< test pass >>>\n\n\n")

    def test_game_control_exception(self):
        print(f"<<< {self.test_game_control_exception.__name__} start >>>")

        game = create_random_game(self.dim)
        robot_robot_id = list(game.robots.keys())[0]
        with self.assertRaises(Exception):
            move_robot(game, robot_robot_id, "exception")

        print("<<< test pass >>>\n\n\n")

    def test_move_forward(self):
        print(f"<<< {self.test_move_forward.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        robot_id = list(game.robots.keys())[0]
        game.move_robot_forward(robot_id)

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
        robot_id1 = list(game.robots.keys())[0]
        robot_id2 = list(game.robots.keys())[1]

        with self.assertRaises(Exception):
            game.move_robot_forward(robot_id1)

        with self.assertRaises(Exception):
            game.move_robot_forward(robot_id2)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_move_backward(self):
        print(f"<<< {self.test_move_backward.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, self.dim-1)
        game.initial_placement()
        robot_id = list(game.robots.keys())[0]
        game.move_robot_backward(robot_id)

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
        robot_id1 = list(game.robots.keys())[0]
        robot_id2 = list(game.robots.keys())[1]

        with self.assertRaises(Exception):
            game.move_robot_backward(robot_id1)

        with self.assertRaises(Exception):
            game.move_robot_backward(robot_id2)

        self.assertIsInstance(game, Game)
        self.assertEqual(game._moves, 0)

        print("<<< test pass >>>\n\n\n")

    def test_turn_right(self):
        print(f"<<< {self.test_turn_right.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        robot_id = list(game.robots.keys())[0]

        self.assertEqual(game.robots[robot_id]['direction'], "E")

        game.turn_robot_right(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "S")
        self.assertEqual(game._moves, 1)

        game.turn_robot_right(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "W")
        self.assertEqual(game._moves, 2)

        game.turn_robot_right(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "N")
        self.assertEqual(game._moves, 3)

        game.turn_robot_right(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "E")
        self.assertEqual(game._moves, 4)

        print("<<< test pass >>>\n\n\n")

    def test_turn_left(self):
        print(f"<<< {self.test_turn_left.__name__} start >>>")

        game = Game(self.dim)
        game.set_robots(0, 0)
        game.initial_placement()
        robot_id = list(game.robots.keys())[0]

        self.assertEqual(game.robots[robot_id]['direction'], "E")

        game.turn_robot_left(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "N")
        self.assertEqual(game._moves, 1)

        game.turn_robot_left(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "W")
        self.assertEqual(game._moves, 2)

        game.turn_robot_left(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "S")
        self.assertEqual(game._moves, 3)

        game.turn_robot_left(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.robots[robot_id]['direction'], "E")
        self.assertEqual(game._moves, 4)

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
        robot_id = list(game.robots.keys())[0]

        game.attack(robot_id)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game.dinosaurs_position), 0)
        self.assertEqual(game._moves, 1)

        print("<<< test pass >>>\n\n\n")

    def test_invalid_robot_id_setting(self):
        print(f"<<< {self.test_invalid_robot_id_setting.__name__} start >>>")

        game = Game(self.dim)
        with self.assertRaises(Exception):
            game.set_dinosaurs(-1, self.dim)
        with self.assertRaises(Exception):
            game.set_robots(-1, self.dim)

        print("<<< test pass >>>\n\n\n")
