import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Callable


class IKey(ABC):

    @abstractmethod
    def key() -> int:
        ...


T = TypeVar('T', bound=IKey)


@dataclass
class Student(IKey):
    full_name: str
    group_number: int
    year: int
    age: int
    average_rating: float

    def key(self) -> float:
        return self.average_rating


@dataclass
class Node(Generic[T], IKey):
    data: T
    prev_ptr: Optional['Node[T]'] = None
    next_ptr: Optional['Node[T]'] = None

    def key(self) -> int:
        return self.data.key()
    

class IndexOutRangeException(Exception):
    pass

class EmptyHeapException(Exception):
    pass


class Heap(Generic[T]):
    def __init__(self, comp: Callable[[T, T], bool] = lambda a, b: a.key() < b.key()) -> None:
        self._length: int = 0
        self._comp: Callable[[T, T], bool] = comp
        self._head: Optional['Node[T]'] = None
        self._tail: Optional['Node[T]'] = None

    def _get(self, index: int) -> T:
        ok: bool = self._check_range(index)
        if not ok: 
            raise IndexOutRangeException('Index Out Range')
        
        if index == 0:
            return self._head.data
        
        elif index == self._length - 1:
            return self._tail.data
        
        elif self._length // 2 >= index:
            node = self._head
            for i in range(index):
                node = node.next_ptr
            return node.data
        
        elif self._length // 2 < index:
            node = self._tail
            for i in range(index, self._length - 1):
                node = node.prev_ptr
            return node.data
        
    def _set(self, index: int, value: T) -> None:
        ok: bool = self._check_range(index)
        if not ok: 
            raise IndexOutRangeException('Index Out Range')
        
        if index == 0:
            self._head.data = value
        
        elif index == self._length - 1:
            self._tail.data = value
        
        elif self._length // 2 >= index:
            node = self._head
            for i in range(index):
                node = node.next_ptr
            node.data = value
        
        elif self._length // 2 < index:
            node = self._tail
            for i in range(index, self._length - 1):
                node = node.prev_ptr
            node.data = value
    
    def _check_range(self, index: int) -> bool:
        if index >= self._length or index < 0:
            return False
        return True
    
    def is_empty(self) -> bool: 
        return self._length == 0
    
    def get_size(self) -> int:
        return self._length
    
    def trickle_up(self, index: int) -> None:
        parent: int = (index - 1) // 2
        bottom: T = self._get(index)

        while index > 0 and self._comp(self._get(parent), bottom):
            self._set(index, self._get(parent))
            index = parent
            parent = (parent - 1) // 2

        self._set(index, bottom)

    def trickle_down(self, index: int) -> None:
        large_child: int = 0
        top: T = self._get(index)
        while index < self._length // 2:
            left_child: int = 2 * index + 1
            right_child: int = left_child + 1
            if (right_child < self._length and
                    self._comp(self._get(left_child), self._get(right_child))):
                large_child = right_child
            else:
                large_child = left_child

            if not self._comp(top, self._get(large_child)):
                break

            self._set(index, self._get(large_child))
            index = large_child

        self._set(index, top)

    # def change(self, index: int, new_value: T) -> None:
    #     ok: bool = self._check_range(index)
    #     if not ok:
    #         raise IndexOutRangeException('Index Out Range')
        
    #     old_value: T = self._get(index)
    #     self._set(index, new_value)
    #     if self._comp(old_value, new_value):
    #         self.trickle_up(index)
    #     else:
    #         self.trickle_down(index)

    def find(self, value) -> bool:
        if self.is_empty():
            raise EmptyHeapException('Empty')
        node = self._head
        while node is not None:
            if node.data.key() == value:
                return True
            node = node.next_ptr
        return False
    
    def __contains__(self, value) -> bool:
        if self.is_empty():
            raise EmptyHeapException('Empty')
        node = self._head
        while node is not None:
            if node.data.key() == value:
                return True
            node = node.next_ptr
        return False

    def insert(self, value: T) -> None:
        node = Node[T](data=value)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
        else:
            self._tail.next_ptr = node
            node.prev_ptr = self._tail
            self._tail = node
            self._length += 1

        self.trickle_up(self._length - 1)

    def pop(self) -> T:
        if self.is_empty():
            raise EmptyHeapException('Empty')
        
        root: T = self._get(0)
        self._length -= 1
        self._set(0, self._get(self._length - 1))
        self._tail.prev_ptr.next_ptr = None
        self._tail = self._tail.prev_ptr
        self.trickle_down(0)
        return root
    
    def loading(self, file: str) -> None:
        with open(file, 'rb') as dump_in:
            m = pickle.load(dump_in)
        self._head = m._head
        self._tail = m._tail
        self._length = m._length

    def save(self, file: str) -> None:
        with open(file, 'wb') as dump_out:
            comp = self._comp
            self._comp = None
            pickle.dump(self, dump_out)
            self._comp = comp

    def print_heap(self) -> None:
        print("heapArray: ")
        for it in range(0, self._length):
            if self._get(it) is not None:
                print(f"{self._get(it).key()} ", end='')
            else:
                print("-- ", end='')

        print("")

        n_blanks, items_per_row, column, j = (32, 1, 0, 0)
        dots: str = 32 * "."
        print(dots * 2)
        while self._length > 0:
            if column == 0:
                for it in range(0, n_blanks):
                    print(" ", end='')

            print(f"{self._get(j).key()} ", end='')
            j += 1
            if j >= self._length:
                break

            column += 1
            if column == items_per_row:
                # Конец строки
                n_blanks //= 2  # Половина пробелов
                items_per_row *= 2  # Вдвое больше элементов
                column = 0  # Начать заново
                print("")  # Переход на новую строку
            else:
                for it in range(0, n_blanks * 2 - 2):
                    print(" ", end='')
        print("\n" + dots * 2)
