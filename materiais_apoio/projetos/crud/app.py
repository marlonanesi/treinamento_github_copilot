from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Protocol, Dict


# ============ Domínio ============

@dataclass(frozen=True)
class Person:
    id: int
    name: str
    age: int


# ============ Exceções ============

class PersonNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


# ============ Repositório (Port) ============

class IPersonRepository(Protocol):
    def next_id(self) -> int: ...
    def add(self, person: Person) -> Person: ...
    def get_by_id(self, person_id: int) -> Person: ...
    def list_all(self) -> List[Person]: ...
    def update(self, person: Person) -> Person: ...
    def delete(self, person_id: int) -> None: ...


# ============ Implementação InMemory (Adapter) ============

class InMemoryPersonRepository(IPersonRepository):
    def __init__(self) -> None:
        self._data: Dict[int, Person] = {}
        self._sequence: int = 0

    def next_id(self) -> int:
        self._sequence += 1
        return self._sequence

    def add(self, person: Person) -> Person:
        self._data[person.id] = person
        return person

    def get_by_id(self, person_id: int) -> Person:
        try:
            return self._data[person_id]
        except KeyError:
            raise PersonNotFoundError(f"Pessoa id={person_id} não encontrada")

    def list_all(self) -> List[Person]:
        return list(self._data.values())

    def update(self, person: Person) -> Person:
        if person.id not in self._data:
            raise PersonNotFoundError(f"Pessoa id={person.id} não encontrada")
        self._data[person.id] = person
        return person

    def delete(self, person_id: int) -> None:
        if person_id not in self._data:
            raise PersonNotFoundError(f"Pessoa id={person_id} não encontrada")
        del self._data[person_id]


# ============ Serviço (Aplicação) ============

class PersonService:
    def __init__(self, repo: IPersonRepository) -> None:
        self._repo = repo

    def create_person(self, name: str, age: int) -> Person:
        self._validate_name(name)
        self._validate_age(age)
        person = Person(id=self._repo.next_id(), name=name.strip(), age=age)
        return self._repo.add(person)

    def list_persons(self) -> List[Person]:
        return self._repo.list_all()

    def update_person(self, person_id: int, name: Optional[str] = None, age: Optional[int] = None) -> Person:
        current = self._repo.get_by_id(person_id)
        new_name = current.name if name is None else name.strip()
        new_age = current.age if age is None else age
        self._validate_name(new_name)
        self._validate_age(new_age)
        updated = Person(id=current.id, name=new_name, age=new_age)
        return self._repo.update(updated)

    def delete_person(self, person_id: int) -> None:
        self._repo.delete(person_id)

    @staticmethod
    def _validate_name(name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Nome não pode ser vazio")
        if len(name.strip()) < 2:
            raise ValidationError("Nome muito curto")

    @staticmethod
    def _validate_age(age: int) -> None:
        if not isinstance(age, int):
            raise ValidationError("Idade deve ser inteira")
        if age < 0 or age > 130:
            raise ValidationError("Idade inválida")


# ============ Camada de Interface (Console) ============

class ConsoleUI:
    def __init__(self, service: PersonService) -> None:
        self._service = service
        self._running = True

    def run(self) -> None:
        while self._running:
            self._print_menu()
            choice = input("Opção: ").strip()
            try:
                if choice == "1":
                    self._handle_create()
                elif choice == "2":
                    self._handle_list()
                elif choice == "3":
                    self._handle_update()
                elif choice == "4":
                    self._handle_delete()
                elif choice == "0":
                    self._running = False
                else:
                    print("Opção inválida.")
            except (ValidationError, PersonNotFoundError) as e:
                print(f"Erro: {e}")
            except ValueError:
                print("Entrada numérica inválida.")
            print()

    @staticmethod
    def _print_menu() -> None:
        print("==== CRUD Pessoa ====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Atualizar")
        print("4 - Remover")
        print("0 - Sair")

    def _handle_create(self) -> None:
        name = input("Nome: ")
        age = int(input("Idade: "))
        person = self._service.create_person(name, age)
        print(f"Cadastrado: {person}")

    def _handle_list(self) -> None:
        persons = self._service.list_persons()
        if not persons:
            print("Nenhuma pessoa cadastrada.")
            return
        for p in persons:
            print(f"[{p.id}] {p.name} - {p.age}")

    def _handle_update(self) -> None:
        pid = int(input("ID a atualizar: "))
        name = input("Novo nome (ENTER mantém): ").strip()
        age_raw = input("Nova idade (ENTER mantém): ").strip()
        name_arg = name if name else None
        age_arg = int(age_raw) if age_raw else None
        updated = self._service.update_person(pid, name=name_arg, age=age_arg)
        print(f"Atualizado: {updated}")

    def _handle_delete(self) -> None:
        pid = int(input("ID a remover: "))
        self._service.delete_person(pid)
        print("Removido com sucesso.")


# ============ Ponto de Entrada ============

def build_app() -> ConsoleUI:
    repo = InMemoryPersonRepository()
    service = PersonService(repo)
    return ConsoleUI(service)


def main() -> None:
    ui = build_app()
    ui.run()


if __name__ == "__main__":
    main()
