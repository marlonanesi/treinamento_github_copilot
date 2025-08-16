import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
from dataclasses import FrozenInstanceError

from app import (
    PersonService,
    InMemoryPersonRepository,
    PersonNotFoundError,
    ValidationError,
    ConsoleUI,
    Person,
)


class TestInMemoryPersonRepository(unittest.TestCase):
    def test_next_id_increments(self):
        repo = InMemoryPersonRepository()
        first = repo.next_id()
        second = repo.next_id()
        self.assertEqual(first + 1, second)

    def test_add_and_get(self):
        repo = InMemoryPersonRepository()
        p = Person(id=1, name="Alice", age=20)
        repo.add(p)
        self.assertEqual(repo.get_by_id(1), p)

    def test_get_missing_raises(self):
        repo = InMemoryPersonRepository()
        with self.assertRaises(PersonNotFoundError):
            repo.get_by_id(99)

    def test_update_missing_raises(self):
        repo = InMemoryPersonRepository()
        with self.assertRaises(PersonNotFoundError):
            repo.update(Person(id=1, name="X", age=10))

    def test_delete(self):
        repo = InMemoryPersonRepository()
        p = Person(id=1, name="Alice", age=20)
        repo.add(p)
        repo.delete(1)
        with self.assertRaises(PersonNotFoundError):
            repo.get_by_id(1)


class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryPersonRepository()
        self.service = PersonService(self.repo)

    def test_create_person_success(self):
        p = self.service.create_person(" Alice ", 30)
        self.assertEqual(p.id, 1)
        self.assertEqual(p.name, "Alice")
        self.assertEqual(p.age, 30)

    def test_list_persons(self):
        self.service.create_person("Ana", 10)
        self.service.create_person("Bruno", 20)
        lst = self.service.list_persons()
        self.assertEqual(len(lst), 2)
        self.assertEqual([p.name for p in lst], ["Ana", "Bruno"])

    def test_create_invalid_name_empty(self):
        with self.assertRaises(ValidationError):
            self.service.create_person("  ", 10)

    def test_create_invalid_name_short(self):
        with self.assertRaises(ValidationError):
            self.service.create_person("A", 10)

    def test_create_invalid_age_negative(self):
        with self.assertRaises(ValidationError):
            self.service.create_person("Ana", -1)

    def test_create_invalid_age_too_big(self):
        with self.assertRaises(ValidationError):
            self.service.create_person("Ana", 131)

    def test_update_person_partial(self):
        p = self.service.create_person("Ana", 10)
        updated = self.service.update_person(p.id, name="Ana Maria")
        self.assertEqual(updated.name, "Ana Maria")
        self.assertEqual(updated.age, 10)

    def test_update_person_full(self):
        p = self.service.create_person("Ana", 10)
        updated = self.service.update_person(p.id, name="Bea", age=22)
        self.assertEqual(updated.name, "Bea")
        self.assertEqual(updated.age, 22)

    def test_update_missing_raises(self):
        with self.assertRaises(PersonNotFoundError):
            self.service.update_person(999, name="X")

    def test_delete_person(self):
        p = self.service.create_person("Ana", 10)
        self.service.delete_person(p.id)
        with self.assertRaises(PersonNotFoundError):
            self.repo.get_by_id(p.id)

    def test_person_is_immutable(self):
        p = self.service.create_person("Ana", 10)
        with self.assertRaises(FrozenInstanceError):
            p.name = "Outra"  # atribuição direta deve falhar em dataclass frozen


class TestConsoleUI(unittest.TestCase):
    def _run_ui_with_inputs(self, inputs):
        repo = InMemoryPersonRepository()
        service = PersonService(repo)
        ui = ConsoleUI(service)
        inputs_iter = iter(inputs)

        def side_effect(_prompt=""):
            try:
                return next(inputs_iter)
            except StopIteration:
                raise AssertionError("Entradas insuficientes fornecidas ao teste")

        out = StringIO()
        with patch("builtins.input", side_effect=side_effect), redirect_stdout(out):
            ui.run()
        return out.getvalue()

    def test_console_create_and_list(self):
        # Sequência:
        # 1 (create) -> Nome -> Idade
        # 2 (list)
        # 0 (exit)
        output = self._run_ui_with_inputs([
            "1", "Alice", "30",
            "2",
            "0"
        ])
        self.assertIn("[1] Alice - 30", output)

    def test_console_invalid_option_then_exit(self):
        output = self._run_ui_with_inputs([
            "9",
            "0"
        ])
        self.assertIn("Opção inválida", output)

    def test_console_delete_flow(self):
        # create, delete, list, exit
        output = self._run_ui_with_inputs([
            "1", "Bob", "40",
            "4", "1",
            "2",
            "0"
        ])
        self.assertIn("Removido com sucesso.", output)
        self.assertIn("Nenhuma pessoa cadastrada", output)

if __name__ == "__main__":
    unittest.main()
