from fastapi.testclient import TestClient
from unittest.case import TestCase

from main import app


class TestGameControllers(TestCase):

    def setUp(self):
        self.app = TestClient(app)

    def tearDown(self):
        # Delete all games between tests
        self.app.delete(f'/games')

    def test_create_random_game(self):
        payload = {
            "grid_dim": 50,
            "robots_count": 0,
            "robots": [],
            "dinosaurs_count": 0,
            "dinosaurs": []
        }

        res = self.app.post('/games/start', json=payload)
        self._check_ok_res(res)
        self.assertIn("game_id", res.json())
        self.assertIn("grid", res.json())
        self.assertIn("dinosaurs", res.json())
        self.assertIn("dinosaurs_position", res.json())
        self.assertIn("robots", res.json())
        self.assertIn("robots_position", res.json())

    def test_create_game(self):
        payload = {
            "grid_dim": 50,
            "robots_count": 0,
            "robots": [(35, 13), (3, 6)],
            "dinosaurs_count": 0,
            "dinosaurs": [(14, 14), (32, 32)]
        }

        res = self.app.post('/games/start', json=payload)
        self._check_ok_res(res)
        self.assertIn("game_id", res.json())
        self.assertIn("grid", res.json())
        self.assertIn("dinosaurs", res.json())
        self.assertIn("dinosaurs_position", res.json())
        self.assertIn("robots", res.json())
        self.assertIn("robots_position", res.json())

    def test_create_game_grid_not_enough(self):
        payload = {
            "grid_dim": 2,
            "robots_count": 0,
            "robots": [],
            "dinosaurs_count": 0,
            "dinosaurs": []
        }
        res = self.app.post('/games/start', json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['detail'], "You must create a bigger grid")

    def test_display_game(self):
        game_id = self._create_game()
        res = self.app.get(f"/games/{game_id}")
        self._check_ok_res(res)

    def test_get_game_not_found(self):
        fake_game_id = 65555
        res = self.app.get(f'/games/{fake_game_id}')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()['detail'], f"Game ID '{fake_game_id}' does not exist")

    def test_move_robot(self):
        game_id = self._create_game()

        payload = {
            "robot_id": 0,
            "command": 0
        }
        res = self.app.put(f"/games/{game_id}", json=payload)

        self.assertIn("game_id", res.json())
        self.assertIn("robot_id", res.json())
        self.assertIn("command", res.json())
        self.assertIn("new_position", res.json())
        self.assertIn("dinosaurs", res.json())
        self.assertIn("dinosaurs_position", res.json())
        self.assertIn("number_of_moves", res.json())
        self.assertIn("all_dinosaurs_has_been_terminated", res.json())

    def test_move_robot_wrong_command(self):
        game_id = self._create_game()

        payload = {
            "robot_id": 0,
            "command": 2435
        }
        res = self.app.put(f"/games/{game_id}", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['detail'], "You must insert the correct instructions as following \
                    0 -> forward, 1 -> backward, 2 -> right, 3 -> left, 4 -> attack")

    def test_remove_game(self):
        game_id = self._create_game()
        resp = self.app.delete(f'/games/{game_id}')
        self.assertEqual(resp.status_code, 204)

    def test_remove_all_games(self):
        game_id1 = self._create_game()
        game_id2 = self._create_game()
        resp = self.app.delete(f'/games')
        self.assertEqual(resp.status_code, 204)

    def _check_ok_res(self, res):
        self.assertEqual(res.status_code, 200)

    def _create_game(self):
        payload = {
            "grid_dim": 50,
            "robots_count": 0,
            "robots": [(0, 0)],
            "dinosaurs_count": 0,
            "dinosaurs": [(2, 2)]
        }

        res = self.app.post('/games/start', json=payload)
        self._check_ok_res(res)
        return res.json()['game_id']
