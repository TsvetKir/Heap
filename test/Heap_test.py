from unittest import TestCase
from py.Heap import Heap, Student
from io import StringIO
import sys

class TestHeap(TestCase):
    def test_init(self):
        heap = Heap()
        self.assertEqual(heap.is_empty(), True)

    def test_get_size(self):
        heap = Heap()
        self.assertEqual(heap.get_size(), 0)

    def test_get(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        self.assertEqual(heap._get(0).key(), 7)
        self.assertEqual(heap._get(3).key(), 1)

    def test_set(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        heap._set(0, Student('AAMM', 1, 2, 5, 10))
        self.assertEqual(heap._get(0).key(), 10)

    def test_insert_trickle_up(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        heap.insert(Student('AALLL', 1, 2, 5, 14))
        self.assertEqual(heap.get_size(), 5)

    def test_is_empty(self):
        heap = Heap()
        self.assertEqual(heap.is_empty(), True)
        heap.insert(Student('AAA', 1, 2, 3, 4))
        self.assertEqual(heap.is_empty(), False)

    def test_pop_trickle_down(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        self.assertEqual(heap.get_size(), 4)
        heap.pop()
        self.assertEqual(heap.get_size(), 3)

    def test_check_range(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        self.assertEqual(heap._check_range(1), True)
        self.assertEqual(heap._check_range(100), False)

    # def test_change(self):
    #     heap = Heap()
    #     heap.insert(Student('AAA', 1, 2, 3, 4))
    #     heap.insert(Student('AA<', 1, 2, 4, 5))
    #     heap.insert(Student('AAMM', 1, 2, 5, 7))
    #     heap.insert(Student('AAMTT', 1, 2, 5, 1))
    #     self.assertEqual(heap._get(0).key(), 7)
    #     heap.change(0, Student('AAMM', 1, 2, 5, 10))
    #     self.assertEqual(heap._get(0).key(), 10)

    def test_find_and_contains(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        self.assertEqual(heap.find(5), True)
        self.assertEqual(heap.find(100), False)
        self.assertEqual(7 in heap, True)
        self.assertEqual(99 in heap, False)

    def test_save_and_loading(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        heap.save('111.txt')
        heap2 = Heap()
        heap2.loading('111.txt')
        self.assertEqual(heap2.get_size(), 4)

    def test_str(self):
        heap = Heap()
        heap.insert(Student('AAA', 1, 2, 3, 4))
        heap.insert(Student('AA<', 1, 2, 4, 5))
        heap.insert(Student('AAMM', 1, 2, 5, 7))
        heap.insert(Student('AAMTT', 1, 2, 5, 1))
        capturedOutput = StringIO()          
        sys.stdout = capturedOutput                   
        heap.print_heap()                                 
        sys.stdout = sys.__stdout__                   
        self.assertEqual(
"""heapArray: 
7 4 5 1 
................................................................
                                7 
                4                               5 
        1 
................................................................
""", capturedOutput.getvalue())
